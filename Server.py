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

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input)
        input_thread.daemon = True
        input_thread.start()

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Client connected from {address}")
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_input(self):
        while True:
            cmd = input("Press Enter to send a file to clients (or 'q' to quit): ").strip()
            if cmd.lower() == 'q':
                break
                
            # Get file path from user input
            self.file_path = input("Enter file path to send: ")
            if not os.path.exists(self.file_path):
                print("File does not exist!")
                continue
                
            self.ready_to_send.set()

    def handle_client(self, client_socket):
        try:
            while True:
                # Wait for client to be ready
                client_socket.recv(1024)
                
                # Wait for server confirmation
                self.ready_to_send.wait()
                
                if self.file_path:
                    # Get file size
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
                        print(f"File {file_name} sent successfully to client")
                    except Exception as e:
                        print(f"Error sending to client: {e}")

                # Wait for next file
                self.ready_to_send.clear()

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast_file(self, file_path):
        if not self.clients:
            print("No clients connected!")
            return
        
        if not os.path.exists(file_path):
            print("File does not exist!")
            return

        for client in self.clients:
            try:
                # Notify client
                client.send("FILE_INCOMING".encode())
            except:
                self.clients.remove(client)

if __name__ == "__main__":
    server = FileServer()
    server.start()