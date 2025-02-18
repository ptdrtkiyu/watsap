import socket
import threading
import logging
import itertools

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

HOST = '127.0.0.1'
PORT = 12345
clients = {}

# Chiffrement César
def cesar(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift if char.islower() else shift % 26
            new_char = chr((ord(char) - ord('a' if char.islower() else 'A') + shift_amount) % 26 + ord('a' if char.islower() else 'A'))
            result += new_char
        else:
            result += char
    return result

# Déchiffrement César
def cesar_decrypt(text, shift=3):
    return cesar(text, -shift)

# Chiffrement Vigenère
def vigenere(text, key="SECRET"):
    result = []
    key_iter = itertools.cycle(key)
    for char in text:
        if char.isalpha():
            shift = ord(next(key_iter).upper()) - ord('A')
            new_char = cesar(char, shift)
            result.append(new_char)
        else:
            result.append(char)
    return "".join(result)

# Déchiffrement Vigenère
def vigenere_decrypt(text, key="SECRET"):
    result = []
    key_iter = itertools.cycle(key)
    for char in text:
        if char.isalpha():
            shift = -(ord(next(key_iter).upper()) - ord('A'))
            new_char = cesar(char, shift)
            result.append(new_char)
        else:
            result.append(char)
    return "".join(result)

def broadcast(message):
    """Envoie un message à tous les clients"""
    encrypted_message = vigenere(message)  # Chiffrement avant envoi
    for client_socket in list(clients.keys()):
        try:
            client_socket.send(encrypted_message.encode())
        except:
            client_socket.close()
            del clients[client_socket]

def handle_client(client_socket):
    """Gère la communication avec un client"""
    try:
        encrypted_username = client_socket.recv(1024).decode()
        username = vigenere_decrypt(encrypted_username)
        clients[client_socket] = username
        logging.info(f"{username} a rejoint le chat.")
        broadcast(f"{username} a rejoint le chat.")

        while True:
            encrypted_message = client_socket.recv(1024).decode()
            if not encrypted_message:
                break
            logging.info(f"Message chiffré reçu de {username}: {encrypted_message}")
            message = vigenere_decrypt(encrypted_message)  
            broadcast(message)

    except:
        pass

    logging.info(f"{clients.get(client_socket, 'Un utilisateur')} a quitté le chat.")
    broadcast(f"{clients.get(client_socket, 'Un utilisateur')} a quitté le chat.")
    del clients[client_socket]
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
logging.info(f"Serveur en écoute sur {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    logging.info(f"Nouvelle connexion : {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
