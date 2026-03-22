import socket
import sys
import time

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
        data = client.recv(4096).decode()
        if not data: break
        
        cmd, payload = data.split(':', 1)
        
        if cmd == "PRINT":
            print(payload, end="", flush=True)
        elif cmd == "READ":
            resp = input(payload)
            client.sendall(resp.encode())
        elif cmd == "EXIT":
            break
finally:
    client.close()

while(True):
    time.sleep(1)