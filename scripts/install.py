#!/bin/python
# -*- coding: utf-8-*-

import sys
import os
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)

ROOT = os.path.split(os.path.realpath(__file__))[0]

def execute_commands(command_list, cache_list):
    cache_length = len(cache_list)    
    cwd = os.path.join(ROOT, os.pardir)
    pwd = cwd
    new_cache_list = []
    stop_cache = False
    try:
        for i in range(len(command_list)):
            command = command_list[i].strip()
            if i < len(cache_list) and \
               command == cache_list[i] and \
               not stop_cache:
                if command.startswith('WORKDIR '):
                    cwd = command[8:].strip().replace('$PWD', pwd).replace('${PWD}', pwd)
                else:
                    logging.info("Cached command {}".format(command))
                new_cache_list.append(command)
            else:
                stop_cache = True
                logging.info("Executing command {}".format(command))
                if command.startswith('RUN '):
                    cmd = command[4:].strip().replace('$PWD', pwd).replace('${PWD}', pwd)
                    res = subprocess.call([cmd], shell=True, cwd=cwd)
                    if res != 0:
                        logging.error("Error: command {} execution failed!".format(command))
                        # write cache
                        with open(os.path.join(ROOT, '.install_cache'), 'w') as f:
                            f.write('\n'.join(new_cache_list))
                        return False
                    else:
                        new_cache_list.append(command)
                elif command.startswith('WORKDIR '):
                    cwd = command[8:].strip().replace('$PWD', pwd).replace('${PWD}', pwd)
                    new_cache_list.append(command)
                else:
                    new_cache_list.append(command)
        return True
    except Exception as e:
        logging.error('Error: {}'.format(e))
    finally:
        # write cache
        with open(os.path.join(ROOT, '.install_cache'), 'w') as f:
            f.write('\n'.join(new_cache_list))

def install():
    if len(sys.argv) <= 1:
        logging.critical("Invalid arguments")
        return False
    t = sys.argv[1]
    cache = ""
    if os.path.exists(os.path.join(ROOT, '.install_cache')):
        with open(os.path.join(ROOT, '.install_cache'), 'r') as f:
            cache = f.read()
    cache_list = cache.split('\n')
    if str(t) == '0':
        with open(os.path.join(ROOT, 'linux.txt'), 'r') as f:
            command_list = f.read().split('\n')    
    elif str(t) == '1':
        with open(os.path.join(ROOT, 'mac.txt'), 'r') as f:
            command_list = f.read().split('\n')
    elif str(t) == '2':
        with open(os.path.join(ROOT, 'win.txt'), 'r') as f:
            command_list = f.read().split('\n')
    else:
        logging.critical("Error: unsupported system type")
        return False
    return execute_commands(command_list, cache_list)

if __name__ == '__main__':
    if install():
        logging.info("wukong-starter installed successfully!")
        exit(0)
    else:
        logging.error("wukong-starter installation failed!")
        exit(1)
