import sys
import socket
import threading
import os
import shutil
import time

class Server: 
    def __init__(self, host='localhost', port=4200, max_clients=5, slave_host='localhost', slave_port=4300):
        self.slave_host = slave_host
        self.slave_port = slave_port
        self.slave_socket = None
        self.clients = [] # Liste des clients connectés pour gérer les déconnexions
        self.server = host
        self.port = port
        self.max_clients = max_clients
        self.socket = None
        self.files_dir = os.path.join(os.path.dirname(__file__), 'files') # Dossier pour stocker les fichiers reçus
        if not os.path.exists(self.files_dir): # Créer le dossier s'il n'existe pas
            os.makedirs(self.files_dir) 

    def start_server(self):
        try:
            self.socket = socket.socket()
            self.socket.bind((self.server, self.port))
            self.socket.listen(self.max_clients)
            print(f"Server started on {self.server}:{self.port}")
            self.accept_thread = threading.Thread(target=self.__accept)
            self.accept_thread.start()
        except ValueError:
            print("Error: Port and max clients must be integers.")
        except Exception as e:
            print(f"Error: {e}")

    def stop_server(self):
        for client in self.clients:
            client.close()
        if self.socket:
            self.socket.close()
        self.server = None
        self.port = None
        self.max_clients = None
        self.socket = None

        print("Server stopped.")

    def connect_to_slave(self):
        for essais in range(5):
            try:
                self.slave_socket = socket.socket()
                self.slave_socket.connect((self.slave_host, self.slave_port))
                print(f"Connected to slave server at {self.slave_host}:{self.slave_port}")
                return
            except Exception as e:
                print(f"Attempt {essais + 1}: Connection au slave impossible: {e}")
                time.sleep(1)


    def receive_text(self, text): # Recevoir un texte du client et l'écrire dans un fichier
        output_file = 'output.txt' 
        with open(output_file, 'w') as f:
            f.write(text)
        shutil.move(output_file, os.path.join(self.files_dir, output_file))
        print(f"File moved to {self.files_dir}.")


    # server.py (Modifications majeures uniquement)

    def __accept(self):
        while True:
            try:
                client, address = self.socket.accept()
                self.clients.append(client)
                print(f"Connection from {address}")
                threading.Thread(target=self.__reception, args=(client,), daemon=True).start()
            except Exception as e:
                print(f"Error during acceptance: {e}")
                break

    def receive_file(self, client, filename, file_size):
        try:
            file_path = os.path.join(self.files_dir, filename)
            with open(file_path, 'wb') as f:
                total_received = 0
                while total_received < file_size:
                    data = client.recv(min(1024, file_size - total_received))
                    if not data:
                        break
                    f.write(data)
                    total_received += len(data)
            print(f"File {filename} received and saved to {file_path}.")

            # Envoi du fichier au slave
            if self.slave_socket:
                self.send_file_to_slave(file_path, filename, file_size)

        except Exception as e:
            print(f"Error receiving file: {e}")
            client.sendall(f"Error: {e}".encode())
        
    def send_file_to_slave(self, file_path, filename, file_size):
        try:
            header = f"FILE|{filename}|{file_size}"
            self.slave_socket.sendall(header.encode())
            with open(file_path, 'rb') as f:
                while (chunk := f.read(4096)):
                    self.slave_socket.sendall(chunk)
            print(f"File {filename} sent to slave.")
            # Recevoir le résultat du slave
            result = self.slave_socket.recv(4096).decode()
            print(f"Result from slave: {result}")
            # Envoi au client
            if self.clients:
                self.clients[-1].sendall(result.encode())  # Envoyer au dernier client connecté
        except Exception as e:
            print(f"Error sending file to slave: {e}")

    
    def __reception(self, client):
        try:
            while True:
                header = client.recv(4096).decode()
                if header.startswith("STOP"):
                    print("Shutdown command received. Stopping server and slaves.")
                    client.sendall("Server shutting down.".encode())
                    self.stop_slaves()
                    self.stop_server()  # Arrêter le serveur principal
                    os._exit(0)  # Arrêter le processus proprement
                elif header.startswith("FILE"):
                    try:
                        _, filename, file_size = header.split('|')
                        file_size = int(file_size)
                        print(f"Receiving file {filename} ({file_size} bytes).")
                        self.receive_file(client, filename, file_size)
                    except ValueError as e:
                        print(f"Error parsing header: {e}")
                        client.sendall(f"Error parsing header: {e}".encode())
                elif header.startswith("TEXT"):
                    text = header[5:]  # Remove "TEXT "
                    print(f"Received text: {text}")
                    self.receive_text(text)
                    client.sendall("Text received successfully.".encode())
                else:
                    print(f"Unknown message: {header}")
        except Exception as e:
            print(f"Error during reception: {e}")
            self.clients.remove(client)
            client.close()

    def stop_slaves(self, ):
        try:
            self.slave_socket.sendall("STOP".encode())
            print("2")
            response = self.slave_socket.recv(4096).decode()
            print(f"Slave response: {response}")
            self.slave_socket.close()
            print("Slave stopped.")
        except Exception as e:
            print(f"Error stopping slave: {e}")




if __name__ == "__main__":
    try:
        server = Server()
        server.connect_to_slave()
        server.start_server()
        input("Press Enter to stop the server...\n")
    except KeyboardInterrupt:
        print("\nServer is stopping...")
    except Exception as e:
        print(e)
    finally:
        server.stop_server()
        sys.exit(0)
