import socket
import threading
import os

clients = []
def send_file(connection, filename):
    """invia un file al client."""
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            connection.sendall(file.read())
        print(f"File '{filename}' inviato con successo!")
    else:
        connection.sendall(b"ERROR: File non trovato")
        print(f"Errore: File '{filename}' non trovato.")

def handle_client(connection, address):
    """Gestisce un client connesso."""
    print(f"\nNuovo client connesso: {address}")
    clients.append(connection)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break  # Se il client si disconnette, esce dal loop
    finally:
        clients.remove(connection)
        connection.close()
        print(f"Connessione chiusa con il client: {address}")

def send_file_to_all(filename):
    """Chiede conferma e invia il file a tutti i client connessi."""
    conferma = input(f"Inviare il file '{filename}' a tutti i client? (s/n): ").strip().lower()
    if conferma == "s":
        for client in clients:
            try:
                client.sendall(f"FILE_IN_ARRIVO {filename}".encode())
                send_file(client, filename)  # Invia il file
            except Exception as e:
                print(f"Errore nell'invio al client: {e}")
    else:
        print("Invio annullato.")

server_address = ('127.0.0.1', 12345)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print(f"Server in ascolto su {server_address[0]}:{server_address[1]}")
def accept_clients():
    while True:
        connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()

threading.Thread(target=accept_clients, daemon=True).start()

while True:
    filename = input("Inserisci il nome del file da inviare (o 'exit' per uscire): ").strip()
    if filename.lower() == "exit":
        break
    send_file_to_all(filename)

server_socket.close()
