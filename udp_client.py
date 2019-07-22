#!/usr/bin/env python
# encoding: utf-8

"""
@author: rylynn 
@file: udp_client.py
@time: 2019-07-19 09:39
@discription: 
"""
import datetime
import socket
import struct
import time
import os

buffer = 1024
#可以多发几次，增加文件发送成功的概率


def packet_sender(socket, file_name):

    file_size = os.path.getsize(file_name)

    header = {'md5': r'...', 'filesize': None, 'offset': 0}
    header['md5'] =  bytes(file_name.split(".")[0], encoding='utf-8')
    header['filesize'] = file_size
    header['offset'] = 0

    packet_count = 0
    start_time = datetime.datetime.now()
    with open(file_name, 'rb') as f:
        while file_size:
            content = f.read(buffer)
            pack = struct.pack('>32sll', header['md5'], header['offset'], header['filesize'])

            print(header)
            socket.sendto(pack+content, ('31.13.65.17', 40420))
            header['offset'] += buffer
            file_size -= buffer
            packet_count += 1
            time.sleep(0.01)

    end_time = datetime.datetime.now()
    print("File sending finish, Total {0} packet send in {1} ms...".format(packet_count, end_time - start_time))


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#while True:
#packet_sender(s, "02c964739cec648c62966bbbce791686.dat")
packet_sender(s, "61160269ec6de7a1fd9cc67fffb41289.dat")
packet_sender(s, "f317b5891c9d151cd64b981aff51a29f.dat")
time.sleep(3)

#测试不同大小发包成功率和与重发次数的关系
def experiment():
    pass


if __name__ == '__main__':
    experiment()