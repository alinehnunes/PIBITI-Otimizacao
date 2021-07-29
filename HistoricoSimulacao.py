from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtWidgets import *


class Historicosimulacao(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QVBoxLayout()

        self.tablewidget = QTableWidget()
        self.listaescolhidas = QListWidget()
        self.botaoapagar = QPushButton("Apagar simulação do Histórico")
        self.botaoacessar = QPushButton("Acessar simulação")
        self.layout.addWidget(self.tablewidget)
        self.layout2.addWidget(self.listaescolhidas)
        self.layout3.addWidget(self.botaoapagar)
        self.layout3.addWidget(self.botaoacessar)
        self.layout2.addLayout(self.layout3)
        self.layout.addLayout(self.layout2)
        self.setLayout(self.layout)
