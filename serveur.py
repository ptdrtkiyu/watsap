import socket
import threading

# Paramètres du serveur
HOST = '127.0.0.1'
PORT = 12345
clients = {}  # Stocke les clients avec leur username

def broadcast(message):
    """Envoie un message à tous les clients"""
    for client_socket in list(clients.keys()):
        try:
            client_socket.send(message.encode())
        except:
            client_socket.close()
            del clients[client_socket]

def handle_client(client_socket):
    """Gère la communication avec un client"""
    try:
        # Récupère le nom d'utilisateur
        username = client_socket.recv(1024).decode()
        clients[client_socket] = username
        print(f"{username} a rejoint le chat.")
        broadcast(f"{username} a rejoint le chat.")

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            full_message = f"{username}: {message}"  # Ajoute le username
            print(full_message)
            broadcast(full_message)  # Envoie à tous
    except:
        pass

    # Gérer la déconnexion du client
    print(f"{clients.get(client_socket, 'Un utilisateur')} a quitté le chat.")
    broadcast(f"{clients.get(client_socket, 'Un utilisateur')} a quitté le chat.")
    del clients[client_socket]
    client_socket.close()

# Lancer le serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Serveur en écoute sur {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Nouvelle connexion : {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
