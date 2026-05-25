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



SEP = "\x1f"
buffer = ""

try:
    while True:
        # Receive up to 4KB
        data = client.recv(4096).decode('utf-8', errors='ignore')
        if not data:
            break
        
        # Add new data to the persistent buffer
        buffer += data

        # Process the buffer as long as it contains our separator
        while SEP in buffer:
            # Split the first complete message out
            message, buffer = buffer.split(SEP, 1)
            
            if not message:
                continue

            if message.startswith("PRINT:"):
                print(message[6:], end="", flush=True)
            elif message.startswith("READ:"):
                # Note: input() still blocks the thread until Enter is pressed
                resp = input(message[5:])
                # Send response back with the same separator
                client.sendall((resp + SEP).encode('utf-8'))
            elif message.startswith("EXIT:"):
                sys.exit(0)
finally:
    client.close()
    sys.exit(0)