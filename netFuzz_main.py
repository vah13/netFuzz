#!/usr/bin/python
from interruptingcow import timeout

import getopt
from mako.exceptions import RuntimeException
import os
import random
import socket
from threading import Thread
from time import sleep

__version__ = "0.1"
__author__ = "vah_13"
import sys


def load_packages_row(file_path):
    row_dump_file = open(file_path, 'r')
    return row_dump_file.readlines()

def connect_with_socket(adress, port):
    _socket = socket.socket()
    _socket.connect((adress, int(port)))
    return _socket

def send_data(_socket, row, timeout=0.1):
    _socket.send(row)
    _socket.settimeout(timeout)

def close_socket(_socket):
    _socket.close()

def recieve_data(_socket):
    _socket.recv(1024*1024)

def fuzz_single_package(address, port, raw, loop, seed):
    _generate_mutated_files(seed, raw, loop)

    for loop_step in range(loop):
        try:
            print(address+":"+str(port) + " " + str(loop_step))
            with open('/tmp/'+str(loop)+"_1313/"+str(seed)+str(loop_step)+'.rdm', 'r') as file:
                raw = file.read().replace('\n', '')
            try:
                with timeout(1, exception=RuntimeException):
                    __socket = connect_with_socket(address, port)
                    send_data(__socket, raw)
                    recieve_data(__socket)
                    close_socket(__socket)
            except RuntimeException, ex:
                print("exception 1" + ex.message)
        except Exception, ex:
            print("exception 2" + ex.message)
    os.system('rm -r /tmp/'+str(loop)+"_1313")

def _generate_mutated_files(seed, raw, loop):
    os.system('rm -r /tmp/'+str(loop)+"_1313")
    with open('/tmp/vah13_fuzz.bin','wb') as f2:
        f2.write(raw)
    os.system('mkdir /tmp/'+str(loop)+"_1313")
    os.system('cat /tmp/vah13_fuzz.bin | radamsa -n '+str(loop)+' -s '+str(seed)+' -o /tmp/'+str(loop)+"_1313/"+str(seed)+'%n.rdm')


def main(argv):
    dump_file = ''
    loop_count = 50000
    address = "172.16.10.91"
    port = "3300"
    mode = 0
    seed = random.randint(0,999999999999999999999999)

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["dfile=", "n=", "o=", "p="])
    except getopt.GetoptError:
        print 'netFuzz_main.py --dfile <inputfile> -n <loop_count> -o <remote_address> -p <port>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'netFuzz_main.py --dfile <inputfile> -n <loop_count> -o <remote_address> -p <port>'
            sys.exit()

        elif opt in ("-d", "--dfile"):
            dump_file = arg

        elif opt in "-n":
            loop_count = arg

        elif opt in "-o":
            address = arg

        elif opt in "-p":
            port = arg

        elif opt in "-m":
            mode = int(arg)

        elif opt in "-s":
            seed = arg

    print 'Fuzz input file is ', dump_file
    print 'Fuzz loop count ', loop_count
    print 'Fuzz address:port ', address + ":" + str(port)
    print 'Fuzz mode -m=1 step-by-step fuzzing,  -m=0 dumb fuzzing'
    print 'Fuzz seed ', str(seed)

    package_list = load_packages_row(dump_file)
    if mode == 0:
        for _single_package_ in package_list:
            fuzz_single_package(address,port,_single_package_.replace('\n',''),loop_count, seed)

if __name__ == "__main__":
    main(sys.argv[1:])
