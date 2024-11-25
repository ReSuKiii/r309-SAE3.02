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

# PARTIE SERVEUR

def ex2server():
    server_address = ('localhost', 12345)
    server_socket = socket.socket()
    server_socket.bind(server_address)
    server_socket.listen(5)
    conn, addr = server_socket.accept()
    print('Connection from:', addr)

    while True:
        message = conn.recv(1024).decode()
        print('Received:', message)
        if message == 'bye':
            conn.send('bye'.encode())
            conn.close()
            conn, addr = server_socket.accept()
        elif message == 'arret':
            conn.send('arret'.encode())
            break
        else:
            conn.send('Message received'.encode())
        

def main():
    ex2server()

try :
    main()
except KeyboardInterrupt:
    print("Server stopped")
    sys.exit(0)