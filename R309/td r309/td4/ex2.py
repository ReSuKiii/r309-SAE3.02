import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QMessageBox

class TempConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        # creation des widgets, des layouts et des signaux 
        self.setWindowTitle("Convertion de température") 
        self.resize(400, 200)

        self.input_label = QLabel("Entrez une température:") 
        self.input_field = QLineEdit() # champ de texte
        self.input_field.setPlaceholderText("Entrez une valeur") #texte par defaut

        self.unit_selector = QComboBox() # menu deroulant
        self.unit_selector.addItems(["Celsius > Kelvin", "Kelvin > Celsius"]) # choix dans le menu deroulant

        self.convert_button = QPushButton("Convertion")
        self.result_label = QLabel("Resultat: ")

        self.convert_button.clicked.connect(self.convert_temperature)

        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.unit_selector)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def convert_temperature(self): #logique de conversion
        try:
            value = float(self.input_field.text())
            if self.unit_selector.currentText() == "Celsius > Kelvin":
                result = value + 273.15
                if value < -273.15:
                    raise ValueError("Température en dessous du zéro absoluu")
            else:
                result = value - 273.15
                if result < -273.15:
                    raise ValueError("Température en dessous du zéro absoluu")
            self.result_label.setText(f"Result: {result:.2f}")
        except ValueError as e:
            QMessageBox.critical(self, "Erreure", str(e))

app = QApplication(sys.argv)
window = TempConverter()
window.show()
sys.exit(app.exec_())
