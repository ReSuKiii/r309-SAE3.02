

import socket

host = '0.0.0.0'
port = 12345
reply = "I'm a server!"

server_socket = socket.socket() # creation du socket
server_socket.bind(('0.0.0.0', port)) # liaison du socket a l'adresse et au port
server_socket.listen(1) # mise en ecoute du socket
conn, address = server_socket.accept() # acceptation de la connexion
message = conn.recv(1024).decode() # reception du message
print(message) # affichage du message recus
conn.send(reply.encode()) # envoi de la reponse
conn.close() # fermeture de la connexion
server_socket.close() # fermeture du socket
