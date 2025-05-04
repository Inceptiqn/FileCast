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
        self.running = True

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            
            # Start download worker thread
            download_thread = threading.Thread(target=self.download_worker)
            download_thread.daemon = True
            download_thread.start()
            
            # Main thread handles receiving file info
            self.receive_files()
            
        except Exception as e:
            print(f"Connection failed: {e}")

    def download_worker(self):
        while self.running:
            try:
                file_info = self.download_queue.get()
                if file_info is None:
                    break
                    
                file_name, file_size, data = file_info
                
                # Create downloads directory if it doesn't exist
                if not os.path.exists('downloads'):
                    os.makedirs('downloads')

                # Write file
                with open(os.path.join('downloads', file_name), 'wb') as f:
                    f.write(data)
                print(f"File {file_name} received successfully")
                
            except Exception as e:
                print(f"Error in download worker: {e}")
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

                # Add to download queue
                self.download_queue.put((file_name, file_size, data))

            except Exception as e:
                print(f"Error receiving file: {e}")
                break

        self.running = False
        self.download_queue.put(None)  # Signal worker to stop
        self.socket.close()

if __name__ == "__main__":
    client = FileClient()
    client.connect()