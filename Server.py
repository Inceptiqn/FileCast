import socket
import threading
import os

class FileServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.file_path = None
        self.ready_to_send = threading.Event()
        self.running = False
        self.accept_thread = None
        self.status_callback = None
        self.client_callback = None

    def set_callbacks(self, status_callback=None, client_callback=None):
        self.status_callback = status_callback
        self.client_callback = client_callback

    def set_file(self, file_path):
        self.file_path = file_path
        self.ready_to_send.set()

    def start(self):
        try:
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            # Start accept thread
            self.accept_thread = threading.Thread(target=self.accept_clients)
            self.accept_thread.daemon = True
            self.accept_thread.start()
            
            return True
        except OSError as e:
            if self.status_callback:
                self.status_callback(f"Failed to start server: {e}")
            self.server_socket.close()
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return False

    def stop(self):
        self.running = False
        for client in self.clients[:]:  # Copy list to avoid modification during iteration
            client.close()
        self.clients.clear()
        self.server_socket.close()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                self.clients.append(client_socket)
                if self.client_callback:
                    self.client_callback(f"{address[0]}:{address[1]}")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
            except:
                if self.running:
                    if self.status_callback:
                        self.status_callback("Error accepting client")

    def handle_client(self, client_socket, address):
        try:
            while True:
                # Wait for client to be ready
                client_socket.recv(1024)
                
                # Wait for file selection
                self.ready_to_send.wait()
                
                if self.file_path:
                    file_size = os.path.getsize(self.file_path)
                    file_name = os.path.basename(self.file_path)

                    try:
                        # Send file info
                        client_socket.send(f"{file_name}|{file_size}".encode())

                        # Send file data
                        with open(self.file_path, 'rb') as f:
                            while True:
                                data = f.read(1024)
                                if not data:
                                    break
                                client_socket.send(data)
                    except Exception as e:
                        if self.status_callback:
                            self.status_callback(f"Error sending to client: {e}")

                # Wait for next file
                self.ready_to_send.clear()

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"Error handling client: {e}")
        finally:
            self.clients.remove(client_socket)
            if self.client_callback:
                self.client_callback(f"{address[0]}:{address[1]}", remove=True)
            client_socket.close()

if __name__ == "__main__":
    server = FileServer()
    server.start()