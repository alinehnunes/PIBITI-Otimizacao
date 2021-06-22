import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from Simulacao import Simulacao, PaginaInicial
from BancodeDados import GraficoParametro
from HistoricoSimulacao import Historicosimulacao
from Sobre import Sobre


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Otimização Cana de Açúcar')
        self.setGeometry(400, 200, 600, 400)
        #self.setStyleSheet("background-color: #d3d3d3;")

        self.createmenubar()

        t = PaginaInicial()
        self.setCentralWidget(t)


    def createmenubar(self):
        simulacaoact = QAction('Nova Simulação', self)
        simulacaoact.triggered.connect(self.opennovasimulacao)

        bancodedadosact = QAction('Banco de Dados', self)
        bancodedadosact.triggered.connect(self.openbancodedados)

        historicosimuact = QAction('Histórico de Simulações', self)
        historicosimuact.triggered.connect(self.openhistoricosimu)

        sobreact = QAction('Sobre', self)
        sobreact.triggered.connect(self.opensobre)

        menubar = self.menuBar()

        menubar.addAction(simulacaoact)
        menubar.addAction(bancodedadosact)
        menubar.addAction(historicosimuact)
        menubar.addAction(sobreact)

    def opennovasimulacao(self):
        t = Simulacao()
        self.setCentralWidget(t)

    def openbancodedados(self):
        t = GraficoParametro("Gráfico teste", "Base de dados inicial.xls", "Planilha1")
        self.setCentralWidget(t)

    def openhistoricosimu(self):
        t = Historicosimulacao()
        self.setCentralWidget(t)

    def opensobre(self):
        t = Sobre()
        self.setCentralWidget(t)

app = QApplication(sys.argv)
app.setStyle('Fusion')

qp = QPalette()
qp.setColor(QPalette.ButtonText, Qt.black)
qp.setColor(QPalette.Window, Qt.lightGray)
qp.setColor(QPalette.Button, Qt.gray)
app.setPalette(qp)

w = MainWindow()
w.show()
app.exec_()
