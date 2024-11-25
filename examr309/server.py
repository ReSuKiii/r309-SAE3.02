import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit

class Server(QWidget):
    def __init__(self):
        super().__init__()
        self.clients = []
        self.server = None
        self.socket = None
        self.setWindowTitle("Le serveur de tchat")
        self.layout = QVBoxLayout()
        self.host = QLineEdit("localhost")
        self.host.setPlaceholderText("Hôte")
        self.layout.addWidget(self.host)
        self.port = QLineEdit("4200")
        self.port.setPlaceholderText("Port")
        self.layout.addWidget(self.port)
        self.max_clients = QLineEdit("5")
        self.max_clients.setPlaceholderText("Max clients")
        self.layout.addWidget(self.max_clients)
        self.start = QPushButton("Démarrer le serveur")
        self.start.clicked.connect(self.__demarrage)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.start)
        self.setLayout(self.layout)
        self.show()

    def __demarrage(self):
        if self.start.text() == "Démarrer le serveur":
            try:
                self.start.setText("Arrêt du serveur")
                self.server = self.host.text()
                self.port = int(self.port.text())
                self.max_clients = int(self.max_clients.text())
                self.socket = socket.socket()
                self.socket.bind((self.server, self.port))
                self.socket.listen(self.max_clients)
                self.accept_thread = threading.Thread(target=self.__accept)
                self.accept_thread.start()
            except ValueError:
                self.text.append("Erreur : Le port et le nombre de clients doivent être des nombres entiers.")
                self.start.setText("Démarrer le serveur")
            except Exception as e:
                self.text.append(f"Erreur : {e}")
                self.start.setText("Démarrer le serveur")
        else:
            self.start.setText("Démarrer le serveur")
            if self.socket:
                self.socket.close()
            self.server = None
            self.port = None
            self.max_clients = None
            self.socket = None

    def __accept(self):
        while True:
            try:
                client, address = self.socket.accept()
                self.clients.append(client)
                self.text.append(f"Connexion de {address}")
                threading.Thread(target=self.__reception, args=(client,)).start()
            except Exception as e:
                self.text.append(f"Erreur lors de l'acceptation : {e}")
                break

    def __reception(self, client):
        while True:
            try:
                message = client.recv(1024).decode()
                if message == "deco-server":
                    self.text.append(f"Déconnexion de {client.getpeername()}")
                    self.clients.remove(client)
                    client.close()
                    break
                self.text.append(message)
            except Exception as e:
                self.text.append(f"Erreur lors de la réception : {e}")
                break

    def closeEvent(self, event):
        self.__demarrage()
        event.accept()

try:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        server = Server()
        sys.exit(app.exec_())
except Exception as e:
    print(e)
    sys.exit(1)
