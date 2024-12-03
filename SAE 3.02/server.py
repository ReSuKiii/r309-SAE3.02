import sys
import socket
import threading
import os
import shutil

class Server: 
    def __init__(self, host='localhost', port=4200, max_clients=5):
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
            # Send acknowledgment to client
            client.sendall(f"File {filename} received successfully.".encode())
        except Exception as e:
            print(f"Error receiving file: {e}")
            client.sendall(f"Error: {e}".encode())

    def __reception(self, client):
        try:
            while True:
                header = client.recv(4096).decode()
                if header.startswith("FILE"):
                    print(f"Header received: {header}")
                    _, filename, file_size = header.split()
                    print(f"Header received: {header}")
                    file_size = int(file_size)
                    print(f"Receiving file {filename} ({file_size} bytes).")
                    self.receive_file(client, filename, file_size)
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




if __name__ == "__main__":
    try:
        server = Server()
        server.start_server()
        input("Press Enter to stop the server...\n")
    except KeyboardInterrupt:
        print("\nServer is stopping...")
    except Exception as e:
        print(e)
    finally:
        server.stop_server()
        sys.exit(0)