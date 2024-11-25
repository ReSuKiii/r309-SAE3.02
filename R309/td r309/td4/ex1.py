import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

# fonctionnement :
# self.x = y
# self = l'objet principal
# x = l'attribut, une variable de la classe
# y = la valeur de l'attribut
# ça peut aussi avoir la forme de x.y où x est un attribut et y une méthode (ex layout.addWidget)

class SimpleDisplay(QMainWindow):
    def __init__(self):
        super().__init__() # appel du constructeur de la classe parente
        self.setWindowTitle("Simple Display") # titre de la fenêtre
        self.resize(300, 200) # taille de la fenêtre

        self.label = QLabel("Cliquez sur le bouton ok", self) # création d'un label (texte)
        self.button = QPushButton("ok", self) # création d'un bouton avec le texte ok
        self.button.clicked.connect(self.on_click) # lien entre le clic sur le bouton et la méthode on_click

        layout = QVBoxLayout() # création d'un layout vertical 
        layout.addWidget(self.label) 
        layout.addWidget(self.button) 

        container = QWidget() # création d'un widget (conteneur)
        container.setLayout(layout) 
        self.setCentralWidget(container) # ajout du widget à la fenêtre principale

    def on_click(self): 
        self.label.setText("Vous avez cliqué sur ok") # modification du texte du label

app = QApplication(sys.argv) # création de l'application
window = SimpleDisplay() # création de la fenêtre
window.show() # affichage de la fenêtre  
sys.exit(app.exec_()) # exécution de l'application
