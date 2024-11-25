# ex2

import socket

host = "localhost"
port = 12345
message = "I'm a client!"

   


client_socket = socket.socket() # creation du socket
client_socket.connect((host, port)) # connexion au serveur
client_socket.send(message.encode()) # envoi du message
reply = str(client_socket.recv(1024).decode()) # reception de la reponse
print(reply) # affichage de la reponse  
client_socket.close()  # fermeture de la connexion



