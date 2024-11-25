#Asynchrone server
'''
• Ajout de messages de « protocole » :
• bye – qui provoque l’arrêt du client mais pas du serveur
• arret – qui arrête les client et le serveur
• De manière asynchrone
• Le client et le serveur peuvent envoyer des messages quand il le souhaite
• En utilisant un mécanisme de Thread
• Tester votre code avec votre voisin
'''

import socket
import threading
import time
import sys

server_socket = socket.socket()
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
print("Server is listening...")


def client_handler(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("Received:", data.decode())
        if data.decode() == "bye":
            break
        if data.decode() == "arret":
            client_socket.close()
            server_socket.close()
            break
        message = input("Enter message: ") 
        client_socket.send(message.encode())
    client_socket.close()

def main():
    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from", addr)
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

try:
    main()
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)

# Le serveur attend une connexion d'un client, puis crée un thread pour gérer la connexion.
# Le thread lit les messages du client et envoie un message en retour.
# Si le message est "bye", le thread se termine.
# Si le message est "arret", le thread se termine et le serveur se termine.
# Le serveur peut gérer plusieurs clients simultanément.
# Le serveur se termine avec Ctrl+C.
    
