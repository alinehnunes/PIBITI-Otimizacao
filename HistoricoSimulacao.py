from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtWidgets import QWidget


class Historicosimulacao(QWidget):

    def __init__(self):
        super().__init__()

        info = QLabel("Espaço onde estará disponível o Histórico de Simulações")
        self.layout = QVBoxLayout()
        self.layout.addWidget(info)
        self.setLayout(self.layout)
