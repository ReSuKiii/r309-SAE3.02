import socket
import subprocess
import os

class SlaveServer:
    def __init__(self, host='localhost', port=4300):
        self.host = host
        self.port = port

    def start(self):
        slave_socket = socket.socket()
        slave_socket.bind((self.host, self.port))
        slave_socket.listen(1)
        print(f"Slave server started on {self.host}:{self.port}")
        
        while True:
            client_socket, address = slave_socket.accept()
            print(f"Slave connected to master: {address}")
            self.handle_client(client_socket)

    # slaves.py

    def execute_program(self, filename):
        try:
            result = subprocess.run(['python3', filename], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout  # Successful execution
            else:
                return f"Execution error: {result.stderr}"
        except Exception as e:
            return f"Execution error: {e}"

    def handle_client(self, client_socket):
        try:
            header = client_socket.recv(4096).decode()
            if header.startswith("FILE"):
                _, filename, file_size = header.split('|')
                file_size = int(file_size)
                file_path = os.path.join(os.getcwd(), filename)

                # Receive file
                with open(file_path, 'wb') as f:
                    total_received = 0
                    while total_received < file_size:
                        chunk = client_socket.recv(min(4096, file_size - total_received))
                        if not chunk:
                            break
                        f.write(chunk)
                        total_received += len(chunk)

                # Execute file and return results
                result = self.execute_program(file_path)
                client_socket.sendall(result.encode())
        except Exception as e:
            client_socket.sendall(f"Error: {e}".encode())
        finally:
            client_socket.close()




if __name__ == "__main__":
    slave_server = SlaveServer()
    slave_server.start()
