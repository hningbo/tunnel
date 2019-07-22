#!/usr/bin/env python
# encoding: utf-8

"""
@author: rylynn 
@file: different_size_sender.py
@time: 2019-07-22 13:32
@discription: 将不同大小的文件分别发往不同的几个IP，查看不同文件大小下的丢包率
"""

import datetime
import os
import socket
import struct
import time

import file_gen

buffer = 1024


def packet_sender(socket, ip, port, file_name):
    file_size = os.path.getsize(file_name)

    header = {'md5': r'...', 'filesize': None, 'offset': 0}
    header['md5'] = bytes(file_name.split(".")[0], encoding='utf-8')
    header['filesize'] = file_size
    header['offset'] = 0

    packet_count = 0
    start_time = datetime.datetime.now()
    with open(file_name, 'rb') as f:
        while file_size:
            content = f.read(buffer)
            pack = struct.pack('>32sll', header['md5'], header['offset'], header['filesize'])

            if packet_count % 1000 == 0:
                print(str(packet_count) + ' packets send....')
            socket.sendto(pack + content, (ip, port))
            header['offset'] += buffer
            file_size -= buffer
            packet_count += 1
            time.sleep(0.01)

    end_time = datetime.datetime.now()
    print("File sending finish, Total {0} packet send in {1} ms...".format(packet_count, end_time - start_time))


time.sleep(3)


def main():
    file_size = 0
    unit = 'MB'
    ip = '31.13.65.17'
    size = [1, 2, 3, 5, 10]
    port = [40421, 40422, 40423, 40424, 40425]

    while True:
        for s, p in zip(size, port):

            print('==================================')
            print("Generating file with size " + str(s) + unit)

            if unit == 'KB':
                file_size = s * 1024
            if unit == 'MB':
                file_size = s * 1024 * 1024
            if unit == 'GB':
                file_size = s * 1024 * 1024 * 1024

            file_name = file_gen.create_file(file_size)

            file_md5 = file_gen.get_file_md5(file_name)
            os.rename(file_name, file_md5 + '.dat')

            file_name = file_md5 + '.dat'

            print('Generating file : ' + file_md5 + '.dat finish. ')

            print('Sending file with size {0} {1} to {2}:{3}'.format(s, unit, ip, p))
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            packet_sender(s, ip, p, file_name)
            os.remove(file_name)
            print('==================================')
            print()
            time.sleep(20)


if __name__ == '__main__':
    main()