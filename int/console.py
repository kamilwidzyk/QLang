import subprocess
import socket
import time
import os
import sys

class Console:
    """
    Allows a process to open a console window in a separate process
    Basic write and read operations supported
    """
    def __init__(self, title="Process Console"):
        self.process = None
        self.conn = None
        self.title = title
        self.child_path = "int\console_worker.py"
        self.port = self.find_free_port()
        self.FLAGS = 0x00000010 

    def find_free_port(self):
        """
        Weird windows way to get any free port.

        Returns:
            int: any port number that is currently free
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    def launch(self):
        """
        Starts the console_worker.py script and connects to it via a socket
        """
        python_exe = sys.executable
        command = f'title {self.title} && cls && python {self.child_path} {self.port}'
        
        # Start it
        self.process = subprocess.Popen(
            ['cmd', '/c', command], 
            creationflags=self.FLAGS
        )
        
        # Connect to it
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.settimeout(10.0) 
        listener.bind(('localhost', self.port))
        listener.listen(1)
        
        # Handle timeout
        try:
            self.conn, _ = listener.accept()
            self.conn.settimeout(None)
        except socket.timeout:
            print(f"FAILED: {self.title} timed out.")
        finally:
            listener.close()

    def write(self, text: str):
        """
        Write to the console

        Parameters:
            text (str): Text to write
        """
        if self.conn:
            self.conn.sendall(f"PRINT:{text}".encode())

    def read(self, prompt="") -> str | None:
        """
        Read a line from the console and return it
        (ignore the prompt parameter for now)

        Returns:
            str: User entered input
            None: Connection lost
        """
        if self.conn:
            self.conn.sendall(f"READ:{prompt}".encode())
            return self.conn.recv(4096).decode()
        return None
