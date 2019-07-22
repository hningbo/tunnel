#!/usr/bin/env python
# encoding: utf-8

"""
@author: rylynn 
@file: pcap_reader.py
@time: 2019-07-19 13:26
@discription: 
"""
import hashlib

from scapy.all import *

PCAP_FILE_PATH = "pcap_data"


def get_file_md5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()

    return myhash.hexdigest()


def file_check(md5, file):
    recombining_file_md5 = get_file_md5(file)
    print("origin file md5 : " + md5)
    print("recombining file md5 : " + recombining_file_md5)
    if md5 == recombining_file_md5:
        os.rename(file, md5 + '.dat')
        return True
    else:
        return False


def file_from_pcap(md5, pcap_file, dest_file):
    with PcapReader(pcap_file) as packets:
        now_offset = 0
        # content_temp用以存储乱序或提前到达的UDP数据报
        content_temp = {}
        for data in packets:
            if 'UDP' in data and data['UDP'].dport in [40420, 40421, 40422, 40423, 40424, 40425]:
                file_md5, offset, file_size = struct.unpack('>32sll', data['UDP'].load[:40])
                if md5 == file_md5.decode('utf-8'):
                    content = data['UDP'].load[40:]
                    if offset == now_offset:
                        dest_file.write(content)
                        now_offset += 1024
                    else:
                        # 如果有乱序提前到达的，加入字典中
                        content_temp[offset] = content

                    while True:
                        if now_offset in content_temp.keys():
                            dest_file.write(content_temp[now_offset])
                            now_offset += 1024
                            content_temp.pop(now_offset)
                            continue
                        else:
                            break

    dest_file.flush()


def main():
    print("Scanning file in pacp data dir...")

    for file in os.listdir(PCAP_FILE_PATH):
        print("Scanning file : " + file)

        file_md5_set = set()

        with PcapReader(PCAP_FILE_PATH + '/' + file) as packets:
            for data in packets:
                if 'UDP' in data and data['UDP'].dport in [40420, 40421, 40422, 40423, 40424, 40425]:
                    file_md5, offset, file_size = struct.unpack('>32sll', data['UDP'].load[:40])
                    file_md5 = file_md5.decode('utf-8')

                    if file_md5 not in file_md5_set:
                        print("Detecting new file with md5 : " + file_md5)
                        print("Detecting file from port {0}...".format(data['UDP'].dport))
                        file_md5_set.add(file_md5)

        for file_md5 in file_md5_set:
            with open(str(time.time()) + '.temp', 'wb') as dest_file:
                print("Recombining file from pcap, md5 : " + file_md5)
                file_from_pcap(file_md5, PCAP_FILE_PATH + '/' + file, dest_file)
                if file_check(file_md5, dest_file.name):
                    print("====================================")
                    print("File CORRECT!!!")
                    print("====================================")

                else:
                    print("====================================")
                    print("File FAIL!!!")
                    print("====================================")


if __name__ == '__main__':
    main()
