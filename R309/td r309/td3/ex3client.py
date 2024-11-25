#Asynchrone client
'''• Ajout de messages de « protocole » :
• bye – qui provoque l’arrêt du client mais pas du serveur
• arret – qui arrête le client et le serveur
• De manière asynchrone
• Le client et le serveur peuvent envoyer des messages quand il le souhaite
• En utilisant un mécanisme de Thread
• Tester votre code avec votre voisin
'''

import socket
import threading
import time
import sys

def receive_handler(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("Reçus:", data.decode())
    client_socket.close()

def main():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 12345))
    print("Connected to server")
    receive_thread = threading.Thread(target=receive_handler, args=(client_socket,))
    receive_thread.start()
    while True:
        message = input("Entrez une réponse: ")
        client_socket.send(message.encode())
        if message == "bye":
            break
        if message == "arret":
            client_socket.close()
            break
    client_socket.close()

if __name__ == "__main__":
    main()
                                            
