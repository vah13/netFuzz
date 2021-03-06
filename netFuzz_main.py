#!/usr/bin/python
from multiprocessing import Pool
import threading

__version__ = "0.5"
__author__ = "vah_13"

from interruptingcow import timeout
from mako.exceptions import RuntimeException
import sys
import getopt
import os
import random
import socket
from timeout import timeout
##
### 1. need add multiple file / package support , 1 file, 1 package
### 2. fix split function in send operation
##

def load_packages_row(file_path):
    raw_dump_file = open(file_path, 'r')
    list = raw_dump_file.readlines()
    ret = []
    for _list in list:
        ret.append(_list.strip().decode('hex'))
    #return row_dump_file.readlines()
    return ret


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
    _socket.recv(1024 * 1024)


def fuzz_dumb_mode(address, port, raw, loop, seed):
    _generate_mutated_package(seed, raw, loop)

    for loop_step in range(loop):
        try:
            print(address + ":" + str(port) + " " + str(loop_step))
            with open(tmp_fuzz_folder + "/" + str(seed) + str(loop_step) + '.rdm', 'r') as file:
                raw = file.read().replace('\n', '')
            try:
                with timeout(1, exception=RuntimeException):
                    __socket = connect_with_socket(address, port)
                    send_data(__socket, raw)
                    recieve_data(__socket)
                    close_socket(__socket)
            except RuntimeException as ex:
                print("exception 1" + ex.message)
        except Exception as ex:
            print("exception 2" + ex.message)
    os.system('rm -r ' + tmp_fuzz_folder + '/*')


def _generate_mutated_package(seed, raw, loop):
    os.system('rm -r ' + tmp_fuzz_folder)
    with open('/tmp/vah13_fuzz.bin', 'wb') as f2:
        f2.write(raw)
    os.system('mkdir ' + tmp_fuzz_folder)
    os.system(
        'cat /tmp/vah13_fuzz.bin | radamsa -n ' + str(loop) + ' -s ' + str(
            seed) + ' -o ' + tmp_fuzz_folder + "/" + str(
            seed) + '%n.rdm')
    os.system('rm /tmp/vah13_fuzz.bin')


#@timeout(1)
def send_recieve(__socket, raw):
    try:
        send_data(__socket, raw)
        recieve_data(__socket)
    except Exception, ex:
        print("new timeout " + ex.message)


def start_fuzz_thread(_address, _port, _seed, _package_list, __package, _bypass, _thread_id):
    for __loop_step in range(_thread_id*2000, (_thread_id+1)*2000):
            try:
                        print(_address + ":" + str(_port) + " " + str(__loop_step))
                        # get mutade package raw
                        with open(tmp_fuzz_folder + "/" + str(_seed) + str(__loop_step + 1) + '.rdm', 'r') as file:
                            raw = file.read().strip()
                        try:
                            __socket = connect_with_socket(_address, _port)
                            for __package_ in _package_list:
                                if _package_list.index(__package_) == _package_list.index(__package) and _package_list.index(
                                        __package) != _bypass:
                                    send_recieve(__socket, raw)  # send mutate package
                                else:
                                    send_recieve(__socket, __package_.strip())  # send package
                            close_socket(__socket)

                        except RuntimeException as ex:
                            print("exception 1 thread " + ex.message)
            except Exception as ex:
                print("exception 2 thread " + ex.message)


def intelectual_fuzz_thread(_address, _port, _package_list, _loop_count, _seed, _bypass):
    for __package in _package_list:
        # start generate package
        if _package_list.index(__package) == _bypass:
            continue
        _generate_mutated_package(_seed, __package.strip(), _loop_count)
        # start fuzz loop
        for _thread_id in range(5):
            t = threading.Thread(target=start_fuzz_thread, args=(_address, _port, _seed, _package_list, __package, _bypass, _thread_id,))
            t.start()


def intelectual_fuzz(_address, _port, _package_list, _loop_count, _seed, _bypass):
        for __package in _package_list:
        # start generate package
            if _package_list.index(__package) == _bypass:
                continue
        _generate_mutated_package(_seed, __package.strip(), _loop_count)

        for __loop_step in range(_loop_count):
                try:
                            print(_address + ":" + str(_port) + " " + str(__loop_step))
                            # get mutade package raw
                            with open(tmp_fuzz_folder + "/" + str(_seed) + str(__loop_step + 1) + '.rdm', 'r') as file:
                                raw = file.read().strip()
                            try:
                                __socket = connect_with_socket(_address, _port)
                                for __package_ in _package_list:
                                    if _package_list.index(__package_) == _package_list.index(__package) and _package_list.index(
                                            __package) != _bypass:
                                        send_recieve(__socket, raw)  # send mutate package
                                    else:
                                        send_recieve(__socket, __package_.strip())  # send package
                                close_socket(__socket)

                            except RuntimeException as ex:
                                print("exception 1" + ex.message)
                except Exception as ex:
                    print("exception 2 " + ex.message)




def main(argv):
    dump_file = ''
    loop_count = 50000
    address = "172.16.10.65"
    port = "4901"
    mode = 1
    seed = random.randint(0, 999999999999999999999999)
    bypass = 0
    thread = 1 # 1 -> thread ;;;; 0 - single thread
    global tmp_fuzz_folder
    tmp_fuzz_folder = "/tmp/netFuzz"
    try:

        print(argv)
        opts, args = getopt.getopt(argv, "hi:o:", ["dump=", "loop=", "address=", "port=", "seed=", "bypass=", "mode=", "thread="])
    except getopt.GetoptError:
        print('netFuzz_main.py --dump <inputfile> --loop <loop_count> --address <remote_address> --port <port> ' \
              '--mode <fuzz_mode_dumb_0> --seed <fuzz_seed> --bypass <bypass_fuzz_pkg> --thread <fuzz_thread_count>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print
            "netFuzz_main.py --dump <inputfile> --loop <loop_count> --address <remote_address> --port <port> " \
            "--mode <fuzz_mode_dumb_0> --seed <fuzz_seed> --bypass <bypass_fuzz_pkg> --thread <fuzz_thread_count>"
            sys.exit()

        elif opt in "--dump":
            dump_file = arg

        elif opt in "--loop":
            loop_count = arg

        elif opt in "--address":
            address = arg

        elif opt in "--port":
            port = arg

        elif opt in "--mode":
            mode = int(arg)

        elif opt in "--seed":
            seed = arg

        elif opt in "--bypass":
            bypass = arg

        elif opt in "--thread":
            thread = arg

    print('Fuzz input file is ', dump_file)
    print('Fuzz loop count ', loop_count)
    print('Fuzz address:port ', address + ":" + str(port))
    print('Fuzz mode -m=1 step-by-step fuzzing,  -m=0 dumb fuzzing')
    print('Fuzz seed ', str(seed))
    print('Fuzz bypass package (experimental)', str(bypass))

    package_list = load_packages_row(dump_file)
    if mode == 0:
        fuzz_dumb_mode(address, port, package_list[0].replace('\n', ''), loop_count, seed)

    if mode == 1:
        if thread==1:
            intelectual_fuzz_thread(address, port, package_list, loop_count, seed, bypass)
        else:
            intelectual_fuzz(address, port, package_list, loop_count, seed, bypass)

if __name__ == "__main__":
    main(sys.argv[1:])