import sys
import socket
import threading
import os
import shutil
import time
import subprocess
import random
import slaves as slaves

class Server: 
    MAX_CLIENTS_PER_SLAVE = 5

    def __init__(self, host='localhost', port=4200, max_clients=5, slave_host='localhost', slave_port=4300, slave_processes=[], slave_loads=[]):
        self.slaves = []
        self.slave_host = slave_host
        self.slave_port = slave_port
        self.slave_processes = slave_processes
        self.slave_loads = slave_loads
        self.slave_sockets = []
        self.clients = [] 
        self.server = host
        self.port = port
        self.host = host
        self.max_clients = max_clients
        self.socket = None
        self.lock = threading.Lock()
        self.files_dir = os.path.join(os.path.dirname(__file__), 'files') 
        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir) 

    def accept_clients(self, server_socket):
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                self.assign_client_to_slave(client_socket)
            except Exception as e:
                print(f"Error accepting clients: {e}")
                break

    def demarrer_server(self):
        try:
            self.socket = socket.socket()
            self.socket.bind((self.server, self.port))
            self.socket.listen(self.max_clients)
            print(f"Server started on {self.server}:{self.port}")
            time.sleep(1)
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
        for process in self.slave_processes:
            process.terminate()
        for sock in self.slave_sockets:
            sock.close()
        self.server = None
        self.port = None
        self.max_clients = None
        self.socket = None

        print("Server stopped.")

    def connection_slave(self, slave_port):
        retries = 5
        for attempt in range(retries):
            try:
                slave_socket = socket.socket()
                slave_socket.connect((self.slave_host, slave_port))
                self.slave_sockets.append(slave_socket)
                print(f"Connected to slave server at {self.slave_host}:{slave_port}")
                return slave_socket
            except Exception as e:
                print(f"Attempt {attempt + 1}: Connection to slave failed: {e}")
                time.sleep(1)
        print(f"Unable to connect to slave on port {slave_port} after {retries} retries.")
        return None

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

            if self.slave_sockets:
                self.envoi_slave(file_path, filename, file_size, client)
            else:
                print("No slaves connected. Starting a new slave.")
                self.start_new_slave()
                retries = 5
                for attempt in range(retries):
                    if self.slave_sockets:
                        break
                    print(f"Attempt {attempt + 1}: Waiting for slave to be ready...")
                    time.sleep(1)
                if self.slave_sockets:
                    self.envoi_slave(file_path, filename, file_size, client)
                else:
                    client.sendall("Failed to start a new slave.".encode())

        except Exception as e:
            print(f"Error receiving file: {e}")
            client.sendall(f"Error: {e}".encode())

    def envoi_slave(self, file_path, filename, file_size, client_socket):
        try:
            header = f"FILE|{filename}|{file_size}"
            slave_index = self.get_least_loaded_slave()
            slave_socket = self.slave_sockets[slave_index]
            print(f"Sending file {filename} to slave on port {slave_socket.getpeername()[1]}")
            slave_socket.sendall(header.encode())
            time.sleep(1)
            with open(file_path, 'rb') as f:
                while (chunk := f.read(4096)):
                    slave_socket.sendall(chunk)
            result = slave_socket.recv(4096).decode()
            print(f"Result from slave: {result}")
            client_socket.sendall(result.encode())
            self.slave_loads[slave_index] += 1
            if self.slave_loads[slave_index] >= self.MAX_CLIENTS_PER_SLAVE:
                print(f"Slave on port {slave_socket.getpeername()[1]} reached max load. Starting a new slave.")
                self.start_new_slave()
        except Exception as e:
            print(f"Error sending file to slave: {e}")
            self.connection_slave(slave_socket.getpeername()[1])

    def reception(self, client):
        try:
            while True:
                if client.fileno() == -1:
                    break
                header = client.recv(4096).decode()
                if not header:
                    break
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
            if client:
                self.clients.remove(client)
                client.close()

    def stop_slaves(self):
        try:
            for sock in self.slave_sockets:
                sock.sendall("STOP".encode())
                response = sock.recv(4096).decode()
                print(f"Slave response: {response}")
                sock.close()
            print("Slaves stopped.")
        except Exception as e:
            print(f"Error stopping slaves: {e}")

    def start_new_slave(self):
        new_port = random.randint(5000, 6000)
        slave = subprocess.Popen([sys.executable, '/DossierMaitre-Slave/slaves.py', str(new_port)])
        self.slave_processes.append(slave)
        self.slave_loads.append(0)
        print(f"New slave started on port {new_port}")
        retries = 5
        for attempt in range(retries):
            slave_socket = self.connect_to_slave(new_port)
            if slave_socket:
                self.slave_sockets.append(slave_socket)
                self.slaves.append({'port': new_port, 'load': 0})
                return
            print(f"Attempt {attempt + 1}: Waiting for slave to be ready...")
            time.sleep(1)
        print(f"Unable to connect to new slave on port {new_port} after {retries} retries.")

    def get_least_loaded_slave(self):
        if not self.slave_loads:
            self.start_new_slave()
        min_load = min(self.slave_loads)
        return self.slave_loads.index(min_load)
    
    def start_slave(self, port):
        slaves.SlaveServer(host='localhost', port=port).start()

    def assign_client_to_slave(self, client_socket):
        self.lock.acquire()
        try:
            for i, slave in enumerate(self.slaves):
                if slave['load'] < self.MAX_CLIENTS_PER_SLAVE:
                    slave['load'] += 1
                    print(f"Assigned client to slave {i} on port {slave['port']}. Current load: {slave['load']}")
                    self.send_to_slave(slave['port'], client_socket)
                    return
            new_port = random.randint(5000, 6000)
            threading.Thread(target=self.start_slave, args=(new_port,), daemon=True).start()
            self.slaves.append({'port': new_port, 'load': 1})
            print(f"New slave started on port {new_port}. Assigned client to this slave.")
            self.send_to_slave(new_port, client_socket)
        finally:
            self.lock.release()
    
    def connect_to_slave(self, slave_port):
        try:
            slave_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            slave_socket.connect(('localhost', slave_port))
            print(f"Connected to slave on port {slave_port}")
            return slave_socket
        except Exception as e:
            print(f"Error connecting to slave on port {slave_port}: {e}")

    def send_to_slave(self, slave_port, client_socket):
        try:
            slave_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            slave_socket.connect(('localhost', slave_port))
            print(f"Connected to slave on port {slave_port}")
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                slave_socket.sendall(data)
            client_socket.close()
            slave_socket.close()
        except Exception as e:
            print(f"Error sending client to slave on port {slave_port}: {e}")

if __name__ == "__main__":
    try:
        server = Server()
        server.demarrer_server()
        input("Press Enter to stop the server...\n")
    except KeyboardInterrupt:
        print("\nServer is stopping...")
    except Exception as e:
        print(e)
    finally:
        server.stop_server()
        sys.exit(0)
