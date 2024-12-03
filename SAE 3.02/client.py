import consignes
import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget, QFileDialog, QTextEdit
import os
import time


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        
        self.host = QLineEdit("localhost")
        self.host.setPlaceholderText("Hôte")
        self.layout.addWidget(self.host)
        
        self.port = QLineEdit("4200")
        self.port.setPlaceholderText("Port")
        self.layout.addWidget(self.port)
        
        self.connect_button = QPushButton("Se connecter")
        self.connect_button.clicked.connect(self.__toggle_connection)
        self.layout.addWidget(self.connect_button)
        
        self.message = QLineEdit()
        self.message.setPlaceholderText("Message à envoyer")
        self.layout.addWidget(self.message)
        
        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.__send_message)
        self.layout.addWidget(self.send_button)
        
        self.file_button = QPushButton("Choisir un fichier")
        self.file_button.clicked.connect(self.__choose_file)
        self.layout.addWidget(self.file_button)
        
        self.send_file_button = QPushButton("Envoyer le fichier")
        self.send_file_button.clicked.connect(self.__send_file)
        self.layout.addWidget(self.send_file_button)
        
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.layout.addWidget(self.log)

        self.clear = QPushButton("Effacer")
        self.clear.clicked.connect(self.log.clear)
        self.layout.addWidget(self.clear)
        
        self.setLayout(self.layout)
        self.show()
        
        self.socket = None
        self.connected = False
        self.file_path = None

    def clear_log(self):
        self.log.clear()

    def __toggle_connection(self):
        if self.connected:
            self.__disconnect()
        else:
            threading.Thread(target=self.__connect).start()

    def __connect(self):
        host = self.host.text()
        port = int(self.port.text())
        for attempt in range(5):
            try:
                self.socket = socket.socket()
                self.socket.connect((host, port))
                self.connect_button.setText("Se déconnecter")
                self.connected = True
                threading.Thread(target=self.__receive_messages, daemon=True).start() # Start a thread to receive messages
                self.log.append("Connecté au serveur.")
                return
            except Exception as e:
                self.log.append(f"Tentative {attempt + 1} : Erreur de connexion : {e}")
                time.sleep(1)
        self.log.append("Impossible de se connecter après 5 tentatives.")

    def __disconnect(self):
        try:
            if self.socket:
                self.socket.close()
            self.socket = None
            self.connected = False
            self.connect_button.setText("Se connecter")
            self.log.append("Déconnecté du serveur.")
        except Exception as e:
            self.log.append(f"Erreur lors de la déconnexion : {e}")

    def __send_message(self):
        if self.connected and self.socket:
            threading.Thread(target=self.__send_message_thread).start()
        else:
            self.log.append("Erreur : Vous devez être connecté pour envoyer un message.")

    def __send_message_thread(self):
        try:
            message = self.message.text()
            self.socket.sendall(message.encode())
            self.log.append(f"Envoyé : {message}")
            self.message.clear()
        except Exception as e:
            self.log.append(f"Erreur : {e}")

    def __choose_file(self):
        options = QFileDialog.Options()
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier", "", "All Files (*);;Text Files (*.txt)", options=options)
        if self.file_path:
            self.log.append(f"Fichier sélectionné : {self.file_path}")

    def __send_file(self):
        if self.connected and self.socket and self.file_path:
            try:
                # Extraire les informations sur le fichier
                file_size = os.path.getsize(self.file_path)
                file_name = os.path.basename(self.file_path)
            
            # Envoi de l'en-tête de fichier
                self.log.append(f"Envoi de l'en-tête : FILE {file_name} {file_size}")
                self.socket.sendall(f"FILE|{file_name}|{file_size}".encode())
                
            
            # Envoi du contenu du fichier
                with open(self.file_path, 'rb') as file:
                    while (chunk := file.read(5024)):
                        self.socket.sendall(chunk)
            
                self.log.append(f"Fichier envoyé : {self.file_path}")
            except Exception as e:
                self.log.append(f"Erreur : {e}")
        else:
            self.log.append("Erreur : Vous devez être connecté et avoir sélectionné un fichier pour envoyer un fichier.")
    
    def __receive_messages(self):
        try:
            while self.connected:
                data = self.socket.recv(4096)  # Buffer size increased for larger responses
                if not data:
                    self.log.append("Server disconnected.")
                    self.__disconnect()
                    break
                self.log.append(f"Response: {data.decode()}")
        except Exception as e:
            self.log.append(f"Error: {e}")
            self.__disconnect()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
