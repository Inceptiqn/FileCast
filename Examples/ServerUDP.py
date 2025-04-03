import socket
server_address = ('127.0.0.1', 12345) # Indirizzo IP e porta del server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)
print(f"Server UDP in ascolto su {server_address}:{server_address[1]}")
while True:
    data, client_address = server_socket.recvfrom(4096)
    print(f"Ricevuto da {client_address}: {data.decode()}")
 # Elaborazione dei dati (qui semplicemente si risponde con lo stesso messaggio in maiuscolo)
    response = data.upper()
    server_socket.sendto(response, client_address)
    print(f"Inviato a {client_address}: {response.decode()}")
# server_socket.close() # In un server reale, la chiusura potrebbe non essere necessaria