import socket
import os
import threading
import queue

class FileClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.download_queue = queue.Queue()
        self.running = False
        self.status_callback = None
        self.progress_callback = None
        self.file_callback = None
        self.connection_thread = None
        self.download_dir = os.path.join(os.getcwd(), 'downloads')

    def set_callbacks(self, status_callback=None, progress_callback=None, file_callback=None):
        self.status_callback = status_callback
        self.progress_callback = progress_callback
        self.file_callback = file_callback

    def set_download_directory(self, directory):
        self.download_dir = directory
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def start_connection(self):
        self.running = True
        self.connection_thread = threading.Thread(target=self.connect)
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def disconnect(self):
        self.running = False
        self.download_queue.put(None)  # Signal worker to stop
        if self.socket:
            self.socket.close()

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            if self.status_callback:
                self.status_callback("Connected")
            
            # Start download worker thread
            download_thread = threading.Thread(target=self.download_worker)
            download_thread.daemon = True
            download_thread.start()
            
            # Main thread handles receiving file info
            self.receive_files()
            
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"Connection failed: {e}")

    def download_worker(self):
        while self.running:
            try:
                file_info = self.download_queue.get()
                if file_info is None:
                    break
                    
                file_name, file_size, data = file_info
                
                # Create downloads directory if it doesn't exist
                if not os.path.exists(self.download_dir):
                    os.makedirs(self.download_dir)

                # Write file
                file_path = os.path.join(self.download_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(data)
                
                if self.file_callback:
                    self.file_callback(file_path)  # Now passing full path
                
            except Exception as e:
                if self.status_callback:
                    self.status_callback(f"Error in download: {e}")
            finally:
                self.download_queue.task_done()

    def receive_files(self):
        while self.running:
            try:
                # Tell server we're ready
                self.socket.send("READY".encode())

                # Receive file info
                file_info = self.socket.recv(1024).decode()
                file_name, file_size = file_info.split('|')
                file_size = int(file_size)

                # Receive file data
                received_size = 0
                data = bytearray()
                while received_size < file_size:
                    chunk = self.socket.recv(1024)
                    if not chunk:
                        break
                    data.extend(chunk)
                    received_size += len(chunk)
                    
                    if self.progress_callback:
                        self.progress_callback(received_size, file_size)

                # Add to download queue
                self.download_queue.put((file_name, file_size, data))

            except Exception as e:
                if self.status_callback:
                    self.status_callback(f"Error receiving file: {e}")
                break

        self.running = False
        self.download_queue.put(None)  # Signal worker to stop
        self.socket.close()

if __name__ == "__main__":
    client = FileClient()
    client.start_connection()