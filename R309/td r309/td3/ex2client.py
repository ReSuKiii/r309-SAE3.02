# ex2
'''
• Ajout de messages de « protocole » :
• bye – qui provoque l’arrêt du client mais pas du serveur
• arret – qui arrête le client et le serveur
• De manière synchrone
• Le client envoie un message et le serveur répond
• Tester votre code avec votre voisin
• Attention un client doit pouvoir se reconnecter après la déconnexion du
précédent
'''
import socket
import sys

# PARTIE CLIENT

def client():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 12345))
    print('Connected to server')
    while True:
        message = input('Enter message: ')
        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()
        print('Received:', response)
        if response == 'bye' or response == 'arret':
            client_socket.close()
            break
            
    

try:
    client()
except KeyboardInterrupt:
    print("Client stopped")
    sys.exit(0)

        
        