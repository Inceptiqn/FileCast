import socket
import threading
def handle_client(connection, address):
    try:
        print(f"Thread avviato per il client: {address}")
        while True:
            data = connection.recv(4096)
            if data:
                print(f"Ricevuto dal client {address}: {data.decode()}")
                response = data.upper()
                connection.sendall(response)
                print(f"Inviato al client {address}: {response.decode()}")
            else:
                print(f"Nessun altro dato dal client {address}")
                break
    finally:
        connection.close()
        print(f"Connessione chiusa con il client: {address}")


server_address = ('127.0.0.1', 12345)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print(f"Server multithread TCP in ascolto su {server_address}:{server_address[1]} ")
while True:
    connection, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()