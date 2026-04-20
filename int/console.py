import subprocess
import socket
import time
import os
import sys

from .logger import log, IN_OUT, ERROR, log_test, INFO, DEBUG

class Console:
    """
    Allows a process to open a console window in a separate process
    Basic write and read operations supported
    """
    test_mode: bool = False

    def __init__(self, title="Process Console"):
        self.process = None
        self.conn = None
        self.title = title
        self.child_path = "int\\console_worker.py"
        self.port = self.find_free_port()
        self.FLAGS = 0x00000010 
        self.SEP = "\x1f"

        self.log_dir = "logs"
        log_test(f"CON_INIT_TITLE={self.title}")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            log(IN_OUT, INFO, f"Log directory created at {self.log_dir}")
            log_test(f"CON LOG_DIR_CREATED={self.log_dir}")

        # remove all chars that are not allowed in file names
        safe_title = "".join([c for c in self.title if c.isalnum() or c in (' ', '.', '_')]).rstrip()
        self.log_file_path = os.path.join(self.log_dir, f"{safe_title}.log")

        # open log file
        self.log_file = open(self.log_file_path, "w", encoding="utf-8", buffering=1)
        log(IN_OUT, DEBUG, f"Log file for {title} console created at {self.log_file_path}")
        log_test(f"LOG_FILE_CREATED={self.log_file_path}")

    def enable_test_mode(self):
        self.test_mode = True

    def log_to_file(self, msg: str) -> bool:
        """
        Write a message to the console's log file

        Parameters:
            msg (str): Message to write to the log file
        
        Returns:
            bool: True if message was written, False if log file is not available
        """
        if self.log_file and not self.log_file.closed:
            self.log_file.write(msg)
            self.log_file.flush()  
            return True
        return False

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
        if self.test_mode:
            return

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
        if self.test_mode:
            self.log_to_file(text)
            return

        if self.conn:
            self.conn.sendall(f"PRINT:{text}{self.SEP}".encode('utf-8'))

    def read(self, prompt="") -> str | None:
        """
        Read a line from the console and return it
        (ignore the prompt parameter for now)

        Returns:
            str: User entered input
            None: Connection lost
        """
        if self.test_mode:
            return "" # read not supported in test mode

        try:
            if self.conn:
                self.conn.sendall(f"READ:{prompt}{self.SEP}".encode('utf-8'))
                
                resp_buffer = ""
                while self.SEP not in resp_buffer:
                    chunk = self.conn.recv(4096).decode('utf-8')
                    if not chunk:
                        return None
                    resp_buffer += chunk
                
                return resp_buffer.split(self.SEP)[0]
            return None
        except (ConnectionResetError, BrokenPipeError):
            log(IN_OUT, ERROR, f"Console '{self.title}' closed or connection lost. Interrupting this place.")
            exit()