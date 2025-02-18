import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

HOST = '127.0.0.1'  
PORT = 12345        

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Chat")

        # Zone d'affichage des messages
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, state=tk.DISABLED)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Champ pour taper les messages
        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)

        # Bouton d'envoi
        self.send_button = tk.Button(root, text="Envoyer", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Connexion au serveur
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        # Demande du username
        self.username = simpledialog.askstring("Nom d'utilisateur", "Entrez votre nom d'utilisateur:")
        self.client_socket.send(self.username.encode())  # Envoie le username au serveur

        # Thread pour recevoir les messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        """Reçoit les messages du serveur et les affiche, sauf ceux envoyés par soi-même"""
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message and not message.startswith(f"{self.username}:"):  # Éviter de réafficher son propre message
                    self.display_message(message)
            except:
                break



    def send_message(self):
        """Envoie le message au serveur et l'affiche immédiatement pour l'envoyeur"""
        message = self.message_entry.get()
        if message:
            # Afficher le message localement avant de l'envoyer
            full_message = f"{self.username}: {message}"
            self.display_message(full_message)
            
            # Envoyer le message au serveur (sans le username, juste le texte)
            self.client_socket.send(message.encode())
            self.message_entry.delete(0, tk.END)



    def display_message(self, message):
        """Affiche le message dans la zone de texte"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

# Lancement de l'interface
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
