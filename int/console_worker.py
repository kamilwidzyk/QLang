import socket
import sys
import time

"""
Worker script for opening a console window and performing basic
input and output functions. Connects via localhost socket to the process
that spawned it. Every terminal needs to be spawned with different port
"""

# Get the unique port from the command line argument
if len(sys.argv) < 2:
    sys.exit("No port provided.")

PORT = int(sys.argv[1])

# Connect back to the parent manager
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Retry connection until the parent listener is ready
while True:
    try:
        client.connect(('localhost', PORT))
        break
    except ConnectionRefusedError:
        time.sleep(0.1)

try:
    while True:
        # one packet of max 4KB, should good for now
        # if it will not be, then the master will split the packets
        # and send the message in parts
        data = client.recv(4096).decode()
        if not data: break
        
        cmd, payload = data.split(':', 1)
        # run 1 of 3 available commands
        if cmd == "PRINT":
            print(payload, end="", flush=True)
        elif cmd == "READ":
            resp = input(payload)
            client.sendall(resp.encode())
        elif cmd == "EXIT":
            break
finally:
    client.close()

# do not exit(this will show the default cmd prompt)
while(True):
    time.sleep(1)