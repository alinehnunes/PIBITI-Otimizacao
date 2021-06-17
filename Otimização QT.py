import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from Simulacao import Simulacao, PaginaInicial
from BancodeDados import GraficoParametro
from HistoricoSimulacao import Historicosimulacao


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Otimização Cana de Açúcar')
        self.setGeometry(400, 200, 600, 400)
        self.setStyleSheet("background-color: #d3d3d3;")

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

        menubar = self.menuBar()

        menubar.addAction(simulacaoact)
        menubar.addAction(bancodedadosact)
        menubar.addAction(historicosimuact)

    def opennovasimulacao(self):
        t = Simulacao()
        self.setCentralWidget(t)

    def openbancodedados(self):
        t = GraficoParametro("Gráfico teste", "Base de dados inicial.xls", "Planilha1")
        self.setCentralWidget(t)

    def openhistoricosimu(self):
        t = Historicosimulacao()
        self.setCentralWidget(t)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
