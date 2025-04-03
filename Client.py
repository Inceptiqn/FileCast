import socket


def receive_file(connection, filename):
    """Riceve un file dal server e lo salva in locale."""
    with open(filename, "wb") as file:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            file.write(data)
    print(f"File '{filename}' ricevuto e salvato.")


# Configurazione del client
server_address = ('127.0.0.1', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(server_address)
    print(f"Connesso al server {server_address[0]}:{server_address[1]}")

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        if data.startswith("FILE_INCOMING"):
            filename = data.split(" ", 1)[1]  # Estrarre il nome del file
            print(f"Ricevendo file: {filename}")
            receive_file(client_socket, filename)
        else:
            print(f"Messaggio dal server: {data}")

except ConnectionError:
    print("Connessione al server persa.")
finally:
    client_socket.close()
    print("Connessione chiusa.")
