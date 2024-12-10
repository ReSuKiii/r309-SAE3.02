import socket
import subprocess
import os

class SlaveServer:
    def __init__(self, host='localhost', port=4300):
        self.host = host
        self.port = port
        self.running = True  # Flag to control the slave server loop

    def start(self):
        slave_socket = socket.socket()
        slave_socket.bind((self.host, self.port))
        slave_socket.listen(1)
        print(f"Slave server started on {self.host}:{self.port}")
        
        while self.running:
            client_socket, address = slave_socket.accept()
            print(f"Connection from master: {address}")
            try:
                self.handle_client(client_socket)
            except Exception as e:
                print(f"Error during client handling: {e}")
            finally:
                client_socket.close()

    def execute_program(self, file_path):
        try:
            if file_path.endswith('.py'):
                result = subprocess.run(['python3', file_path], capture_output=True, text=True)
                # Delete the file in the /files after execution
                subprocess.run(['del', file_path], shell=True)
            elif file_path.endswith('.java'):
                compile_result = subprocess.run(['javac', file_path], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    return f"Compilation error: {compile_result.stderr}"
                class_name = os.path.splitext(os.path.basename(file_path))[0]
                result = subprocess.run(['java', class_name], capture_output=True, text=True)
                subprocess.run(['del', f"{class_name}.class"], shell=True)
            elif file_path.endswith('.c'):
                executable = os.path.splitext(file_path)[0]
                compile_result = subprocess.run(['gcc', file_path, '-o', executable], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    return f"Compilation error: {compile_result.stderr}"
                result = subprocess.run([executable], capture_output=True, text=True)
                subprocess.run(['del', f"{executable}.exe"], shell=True)
                
            else:
                return "Unsupported file type."

            if result.returncode == 0:
                return result.stdout
            else:
                return f"Execution error: {result.stderr}"
        except Exception as e:
            return f"Execution error: {e}"

    def handle_client(self, client_socket):
        while True:  # Keep the connection alive for multiple requests
            try:
                header = client_socket.recv(4096).decode()
                if not header:
                    break  # Disconnect if no data received

                if header.startswith("STOP"):
                    print("Shutdown command received. Terminating slave.")
                    client_socket.sendall("Slave shutting down.".encode())
                    self.running = False
                    return
                elif header.startswith("FILE"):
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

                    print(f"File {filename} received. Executing...")
                    result = self.execute_program(file_path)
                    client_socket.sendall(result.encode())
                elif header.startswith("TEXT"):
                    text = header[5:]  # Extract the text content
                    print(f"Received text: {text}")
                    response = f"Text received: {text}"
                    client_socket.sendall(response.encode())
                else:
                    client_socket.sendall("Unknown command.".encode())
            except Exception as e:
                print(f"Error handling client: {e}")
                break

if __name__ == "__main__":
    slave_server = SlaveServer()
    slave_server.start()
