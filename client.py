import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import itertools

HOST = '127.0.0.1'
PORT = 12345

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

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Chat")

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, state=tk.DISABLED)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Envoyer", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        self.username = simpledialog.askstring("Nom d'utilisateur", "Entrez votre nom d'utilisateur:")
        self.client_socket.send(vigenere(self.username).encode())  
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        """Reçoit et déchiffre les messages du serveur"""
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024).decode()
                if encrypted_message:
                    message = vigenere_decrypt(encrypted_message)  
                    if not message.startswith(f"{self.username}:"):
                        self.display_message(message)
            except:
                break

    def send_message(self):
        """Chiffre et envoie le message au serveur et l'affiche immédiatement"""
        message = self.message_entry.get()
        if message:
            full_message = f"{self.username}: {message}"
            encrypted_message = vigenere(full_message)
            self.client_socket.send(encrypted_message.encode())

            # Afficher immédiatement le message sans attendre le retour du serveur
            self.display_message(full_message)

            self.message_entry.delete(0, tk.END)


    def display_message(self, message):
        """Affiche le message dans la zone de texte"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
