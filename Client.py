import socket
import os
import threading
import queue

class FileClient:
    def __init__(self, host='localhost', port=5000):
        # Inizializzazione del client
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
        # Impostazione delle funzioni di callback
        self.status_callback = status_callback
        self.progress_callback = progress_callback
        self.file_callback = file_callback

    def set_download_directory(self, directory):
        # Imposta la cartella di download
        self.download_dir = directory
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def start_connection(self):
        # Avvia la connessione al server
        self.running = True
        self.connection_thread = threading.Thread(target=self.connect)
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def disconnect(self):
        # Disconnette dal server
        self.running = False
        self.download_queue.put(None)
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.socket.close()

    def connect(self):
        # Gestisce la connessione al server
        try:
            self.socket.connect((self.host, self.port))
            if self.status_callback:
                self.status_callback("Connected")
            
            download_thread = threading.Thread(target=self.download_worker)
            download_thread.daemon = True
            download_thread.start()
            
            self.receive_files()
            
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"Connection failed: {e}")

    def download_worker(self):
        # Gestisce il download dei file
        while self.running:
            try:
                file_info = self.download_queue.get()
                if file_info is None:
                    break
                    
                file_name, file_size, data = file_info
                
                if not os.path.exists(self.download_dir):
                    os.makedirs(self.download_dir)

                file_path = os.path.join(self.download_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(data)
                
                if self.file_callback:
                    self.file_callback(file_path)
                
            except Exception as e:
                if self.status_callback:
                    self.status_callback(f"Error in download: {e}")
            finally:
                self.download_queue.task_done()

    def receive_files(self):
        # Riceve i file dal server
        while self.running:
            try:
                self.socket.send("READY".encode())

                file_info = self.socket.recv(1024).decode()
                file_name, file_size = file_info.split('|')
                file_size = int(file_size)

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

                self.download_queue.put((file_name, file_size, data))

            except Exception as e:
                if self.status_callback:
                    self.status_callback(f"Error receiving file: {e}")
                break

        self.running = False
        self.download_queue.put(None)
        self.socket.close()

if __name__ == "__main__":
    client = FileClient()
    client.start_connection()