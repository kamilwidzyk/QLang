import subprocess
import socket
import time
import os
import sys

class Console:
    def __init__(self, title="Process Console"):
        self.process = None
        self.conn = None
        self.title = title
        # Get the absolute path to the child script to avoid "File Not Found" errors
        self.child_path = "int\console_worker.py"
        self.port = self._find_free_port()
        self.FLAGS = 0x00000010 

    def _find_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    def launch(self):
        # We use 'cmd /k' so if it crashes, the window stays open to show the error
        # We use double quotes around paths in case your folder name has spaces
        python_exe = sys.executable
        command = f'title {self.title} && cls && python {self.child_path} {self.port}'
        
        self.process = subprocess.Popen(
            ['cmd', '/c', command], 
            creationflags=self.FLAGS
        )
        
        # Setup listener
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.settimeout(10.0) # Increased timeout for slow system starts
        listener.bind(('localhost', self.port))
        listener.listen(1)
        
        try:
            self.conn, _ = listener.accept()
            self.conn.settimeout(None)
        except socket.timeout:
            print(f"FAILED: {self.title} timed out.")
        finally:
            listener.close()

    def write(self, text):
        if self.conn:
            self.conn.sendall(f"PRINT:{text}".encode())

    def read(self, prompt="> "):
        if self.conn:
            self.conn.sendall(f"READ:{prompt}".encode())
            return self.conn.recv(4096).decode()
        return None

# --- TESTING MULTIPLE WINDOWS ---
if __name__ == "__main__":
    # Create them
    c1 = ConsoleController("Logger Alpha")
    c2 = ConsoleController("Input Beta")

    # Launch them
    print("Launching Window 1...")
    c1.launch()
    
    print("Launching Window 2...")
    c2.launch()

    # Interaction
    c1.write("Alpha is online.")
    c2.write("Beta is online.")
    
    val = c2.read("Type something for Beta: ")
    c1.write(f"Beta sent us: {val}")