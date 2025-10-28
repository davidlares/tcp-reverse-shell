## TCP Reverse Shell

This repository contains a full outline example of how to perform `TCP` Reverse Shell using only built-in commands from the Python core language.

The bigger picture here is that usually a victim is protected by a certain network infrastructure (firewall rules mostly) and any anti-malware software installed, so the attacker should try to find a particular legitimate way of creating a direct channel between the victim and the attacker's machine.

So, in a few words. An attacker should bypass the built-in or host-based firewall on the OS (the default will block non-legitimate incoming traffic) and find a way to send a malicious file to a client

## Scenario

I used a Win7 VM with a `bridged network` adapter as the target machine and a Ubuntu 18.04 machine as the attacker. Both machines should be present on the same network subnet, in order to be visible to each other.

For a full understanding of this script, you should be able to work with the socket implementation in Python

## The TCP Shell

Let me summarize this into a single step.

1. This will initialize (on target) a TCP connection to the attacker.
2. The attacker will be the `TCP Server` and the victim is serving as the `TCP client` (mostly a shell connection)
3. The `TCP shell` will have the ability to start a CMD process on the target machine (like using `cmd.exe`). This will bind a network socket connection to the Attacker on a certain port (destination port).

4. Once the victim opens the file, it expects to receive a reverse TCP connection on [X] port, where
  - The destination port will be X
  - The attacker must be listening to the X port set (must be open)
  - After completing the 3-way handshake. We send a command to the client, execute, and the standard output will be prompted to the attacker

## How to use

First, the attacker should be listening to client connections by specifying a common IP and port for the `TCP` connection, both are hard-coded in the `client.py` and `server.py` files. So, you should start running the `server.py` file before listening to client connections with the right network values (IP and ports).

Once the reverse `TCP tunnel` is made, we get the user input that is sent to the target machine. Once received, the `client.py` will process that command with the help of the `subprocess` python-mode and send back the `stdout` or `stderr` of the resulting execution.

The `setup.py` file is needed for creating the `client.exe` binary. You will need to download the `py2exe 0.6.9 exe` file from the internet (Python 2.x is required) and run it inside a Windows machine. Important: you should have both files (`client.py` and `setup.py`) at the same level as the installer.

There's an example of the `client.exe` with the log in the `dist` directory.

## Code actions

Once the connection is made, we have 3 particular actions that we can perform.

1. `Shell> [Type your command]`. This action will output the result of executing something.
2. `Shell> grab -f [file]`. the `grab -f` command will transfer or extract data from the target by setting a placeholder for the file. This is handled by looping a file if it exists, and reading the file (pieces) with 1kb top, which until reaching `EoF`, after that will the written in the attacker machine
3. `Shell> terminate`. Will close the socket connections

## Credits
[David Lares S](https://davidlares.com)

## License
[MIT](https://opensource.org/licenses/MIT)
