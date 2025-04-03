import socket
server_address = ('127.0.0.1', 12345) # Indirizzo IP e porta del server
message = b'Ciao dal client TCP!'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(server_address)
    print(f"Connesso a {server_address}:{server_address[1]}")
    client_socket.sendall(message)
    print(f"Inviato: {message.decode()}")
    data = client_socket.recv(4096)
    print(f"Ricevuto dal server: {data.decode()}")
finally:
    client_socket.close()