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

       
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafafa;
                color: #333;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }

            QLineEdit {
                border: 1px solid #cccccc;
                padding: 4px 8px;
                border-radius: 5px;
                margin-bottom: 6px;
                background-color: #f0f0f0;
                font-size: 12px;
            }

            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                margin-bottom: 8px;
                min-width: 130px;
            }

            QPushButton#stop_button {
                background-color: red;
                color: white;
            }

            QPushButton#clear_button {
                background-color: #d3d3d3;
                color: #333;
            }

            QPushButton#connect_button {
                background-color: #28a745;
                color: white;
            }

            QPushButton#connect_button.disconnect {
                background-color: red;
                color: white;
            }

            QTextEdit {
                background-color: #fff;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 6px;
                font-family: Consolas, monospace;
                font-size: 12px;
                min-height: 150px;
                max-height: 200px;
            }
        """)

       
        self.setGeometry(100, 100, 700, 500) 

        
        self.host = QLineEdit("localhost")
        self.host.setPlaceholderText("Hôte")
        self.layout.addWidget(self.host)

        self.port = QLineEdit("4200")
        self.port.setPlaceholderText("Port")
        self.layout.addWidget(self.port)

        self.connect_button = QPushButton("Se connecter")
        self.connect_button.setObjectName("connect_button")
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
        self.clear.setObjectName("clear_button")
        self.clear.clicked.connect(self.log.clear)
        self.layout.addWidget(self.clear)

        self.stop_button = QPushButton("Arrêter le serveur")
        self.stop_button.setObjectName("stop_button")  
        self.stop_button.clicked.connect(self.__send_stop_command)
        self.layout.addWidget(self.stop_button)

        self.press_enter_to_send()

        self.show()

        self.socket = None
        self.connected = False
        self.file_path = None
        self.disconnecting = False  

    def clear_log(self):
        self.log.clear()

    def __toggle_connection(self):
        if self.connected:
            self.__disconnect()
        else:
            threading.Thread(target=self.__connect).start()

    def __send_stop_command(self):
        if self.connected and self.socket:
            try:
                self.socket.sendall("STOP".encode())
                self.log.append("Commande d'arrêt envoyée au serveur.")
                self.__disconnect() 
            except Exception as e:
                self.log.append(f"Erreur lors de l'arrêt: {e}")

    def __connect(self):
        host = self.host.text()
        port = int(self.port.text())
        for attempt in range(5):
            try:
                self.socket = socket.socket()
                self.socket.connect((host, port))
                self.connect_button.setText("Se déconnecter")
                self.connect_button.setObjectName("connect_button")
                self.connect_button.setStyleSheet("background-color: red; color: white;")  
                self.connected = True
                threading.Thread(target=self.__receive_messages, daemon=True).start() 
                self.log.append("Connecté au serveur.")
                return
            except Exception as e:
                self.log.append(f"Tentative {attempt + 1} : Erreur de connexion : {e}")
                time.sleep(1)
        self.log.append("Impossible de se connecter après 5 tentatives.")

    def __disconnect(self):
        if self.disconnecting:  
            return

        self.disconnecting = True  
        try:
            if self.socket:
                self.socket.close()
            self.socket = None
            self.connected = False
            self.connect_button.setText("Se connecter")
            self.connect_button.setObjectName("connect_button")
            self.connect_button.setStyleSheet("background-color: #28a745; color: white;") 
            self.log.append("Déconnecté du serveur.")
        except Exception as e:
            self.log.append(f"Erreur lors de la déconnexion : {e}")
        finally:
            self.disconnecting = False  

    def __send_message(self):
        if self.connected and self.socket:
            threading.Thread(target=self.__send_message_thread).start()
        else:
            self.log.append("Erreur : Vous devez être connecté pour envoyer un message.")

    def __send_message_thread(self):
        try:
            message = self.message.text()
            self.socket.sendall("TEXT".encode() + message.encode())
            self.log.append(f"Envoyé : {message}")
            self.message.clear()
        except Exception as e:
            self.log.append(f"Erreur lors de l'envoi du message : {e}")

    def press_enter_to_send(self):
        self.message.returnPressed.connect(self.__send_message)


    def __choose_file(self):
        options = QFileDialog.Options()
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier", "", "All Files (*);;Text Files (*.txt)", options=options)
        if self.file_path:
            self.log.append(f"Fichier sélectionné : {self.file_path}")

    def __send_file(self):
        if self.connected and self.socket and self.file_path:
            try:
                file_size = os.path.getsize(self.file_path)
                file_name = os.path.basename(self.file_path)
            
                self.log.append(f"Envoi de l'en-tête : FILE {file_name} {file_size}")
                self.socket.sendall(f"FILE|{file_name}|{file_size}".encode())
            
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
                data = self.socket.recv(4096)
                if data:
                    self.log.append(f"Response: {data.decode()}")
                else:
                    break  
        except socket.error as e:
            if str(e) != "[WinError 10038] Une opération a été tentée sur autre chose qu’un socket":
                pass
        finally:
            if self.connected:
                self.__disconnect()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
