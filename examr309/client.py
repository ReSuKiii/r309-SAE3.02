
import sys
import socket
import threading
import time

host = "127.0.0.1"
port = 4200
client_socket = socket.socket()
client_socket.connect((host, port))

def client():
    
    while True:
        message = input("Entrez votre message: ")
        client_socket.send(message.encode())
        # if message == "deco-server":
        #     break
        # reply = str(client_socket.recv(1024).decode())
        # print(reply)
    client_socket.close()

try:
    client()
except ConnectionRefusedError:
    print("Le serveur est fermé")
except ConnectionResetError:
    print("Le serveur a été fermé")
except KeyboardInterrupt:
    print("Vous avez fermé le client")
finally:
    try:
        client_socket.close()
    except:
        pass

   

