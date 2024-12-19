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
        self.clients = [] 
        self.server = host
        self.port = port
        self.max_clients = max_clients
        self.socket = None
        self.files_dir = os.path.join(os.path.dirname(__file__), 'files') 
        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir) 

    def demarrer_server(self):
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

    def connection_slave(self):
        retries = 5
        for attempt in range(retries):
            try:
                self.slave_socket = socket.socket()
                self.slave_socket.connect((self.slave_host, self.slave_port))
                print(f"Connected to slave server at {self.slave_host}:{self.slave_port}")
                return
            except Exception as e:
                print(f"Attempt {attempt + 1}: Connection to slave failed: {e}")
                time.sleep(1)
        print("Unable to connect to the slave server after retries.")


    def recept_text(self, text):
        output_file = 'output.txt' 
        with open(output_file, 'w') as f:
            f.write(text)
        shutil.move(output_file, os.path.join(self.files_dir, output_file))
        print(f"File moved to {self.files_dir}.")


    def __accept(self):
        while True:
            try:
                client, address = self.socket.accept()
                self.clients.append(client)
                print(f"Connection from {address}")
                threading.Thread(target=self.reception, args=(client,), daemon=True).start()
            except Exception as e:
                print(f"Error during acceptance: {e}")
                break

    def recept_file(self, client, filename, file_size):
        try:
            file_path = os.path.join(self.files_dir, filename)
            with open(file_path, 'wb') as f:
                total_received = 0
                while total_received < file_size:
                    data = client.recv(min(4096, file_size - total_received))
                    if not data:
                        break
                    f.write(data)
                    total_received += len(data)
            print(f"File {filename} received and saved to {file_path}.")

            if self.slave_socket:
                self.envoi_slave(file_path, filename, file_size)
            else:
                client.sendall("Slave connection not available.".encode())

        except Exception as e:
            print(f"Error receiving file: {e}")
            client.sendall(f"Error: {e}".encode())
        
    def envoi_slave(self, file_path, filename, file_size):
        try:
            header = f"FILE|{filename}|{file_size}"
            self.slave_socket.sendall(header.encode())
            with open(file_path, 'rb') as f:
                while (chunk := f.read(4096)):
                    self.slave_socket.sendall(chunk)
            result = self.slave_socket.recv(4096).decode()
            print(f"Result from slave: {result}")
            if self.clients:
                self.clients[-1].sendall(result.encode())
        except Exception as e:
            print(f"Error sending file to slave: {e}")
            self.connection_slave()  

    
    def reception(self, client):
        try:
            while True:
                header = client.recv(4096).decode()
                if header.startswith("STOP"):
                    print("Shutdown command received. Stopping server and slaves.")
                    client.sendall("Server shutting down.".encode())
                    self.stop_slaves()
                    self.stop_server()  
                    os._exit(0) 
                elif header.startswith("FILE"):
                    try:
                        _, filename, file_size = header.split('|')
                        file_size = int(file_size)
                        print(f"Receiving file {filename} ({file_size} bytes).")
                        self.recept_file(client, filename, file_size)
                    except ValueError as e:
                        print(f"Error parsing header: {e}")
                        client.sendall(f"Error parsing header: {e}".encode())
                elif header.startswith("TEXT"):
                    text = header[5:]
                    print(f"Received text: {text}")
                    self.recept_text(text)
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
        server.connection_slave()
        server.demarrer_server()
        input("Press Enter to stop the server...\n")
    except KeyboardInterrupt:
        print("\nServer is stopping...")
    except Exception as e:
        print(e)
    finally:
        server.stop_server()
        sys.exit(0)
