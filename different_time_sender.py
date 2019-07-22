#!/usr/bin/env python
# encoding: utf-8

"""
@author: rylynn 
@file: different_time_sender.py
@time: 2019-07-22 13:33
@discription: 将同一文件往不同端口分别发送1，2，3，4，5次，查看不同端口中的丢包率
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
    size = 1
    unit = 'MB'
    ip = '31.13.65.17'
    resend_time = [1, 2, 3, 4, 5]
    port = [40421, 40422, 40423, 40424, 40425]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:

        for rt, p in zip(resend_time, port):
            # 目前发送的次数
            now_t = 1
            print("Generating file with size " + str(size) + unit)

            if unit == 'KB':
                file_size = size * 1024
            if unit == 'MB':
                file_size = size * 1024 * 1024
            if unit == 'GB':
                file_size = size * 1024 * 1024 * 1024

            file_name = file_gen.create_file(file_size)

            file_md5 = file_gen.get_file_md5(file_name)
            os.rename(file_name, file_md5 + '.dat')

            file_name = file_md5 + '.dat'

            print('==================================')
            print('Generating file : ' + file_md5 + '.dat finish. ')


            while now_t <= rt:
                print('Sending file {0} to {3}:{4}, now is the {1}/{2} times...'.format(file_name, now_t, rt, ip, p))
                packet_sender(s, ip, p, file_name)
                now_t = now_t + 1

            os.remove(file_name)

            print('==================================')
            print()
            time.sleep(20)


if __name__ == '__main__':
    main()
