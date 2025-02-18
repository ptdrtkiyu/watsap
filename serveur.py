import socket
import threading

# Paramètres du serveur
HOST = '127.0.0.1'
PORT = 12345
clients = []

def broadcast(message, sender_socket):
    """Envoie le message à tous les clients sauf l'expéditeur"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    """Gère la communication avec un client"""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Message reçu : {message.decode()}")
            broadcast(message, client_socket)
        except:
            break

    clients.remove(client_socket)
    client_socket.close()

# Démarrer le serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Serveur en écoute sur {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Nouvelle connexion : {addr}")
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,)).start()
