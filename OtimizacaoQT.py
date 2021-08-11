import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from Simulacao import Simulacao, PaginaInicial
from GraficoParametros import GraficoParametro
from HistoricoSimulacao import Historico
from Sobre import Sobre
from ParametrosOtimizacao import Otimizacao

#Otimizacao = Otimizacao()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Otimização Cana de Açúcar')
        self.setGeometry(200, 100, 800, 600)

        t = PaginaInicial()
        self.setCentralWidget(t)

        self.createmenubar()


    def createmenubar(self):
        paginainicialact = QAction('Pagina Inicial', self)
        paginainicialact.triggered.connect(self.openpaginainicial)

        simulacaoact = QAction('Nova Simulação', self)
        simulacaoact.triggered.connect(self.opennovasimulacao)

        bancodedadosact = QAction('Banco de Dados', self)
        bancodedadosact.triggered.connect(self.openbancodedados)

        historicosimuact = QAction('Histórico de Simulações', self)
        historicosimuact.triggered.connect(self.openhistoricosimu)

        sobreact = QAction('Sobre', self)
        sobreact.triggered.connect(self.opensobre)

        menubar = self.menuBar()

        menubar.addAction(paginainicialact)
        menubar.addAction(simulacaoact)
        menubar.addAction(bancodedadosact)
        menubar.addAction(historicosimuact)
        menubar.addAction(sobreact)

    def openpaginainicial(self):
        t = PaginaInicial()
        self.setCentralWidget(t)

    def opennovasimulacao(self, otm=None):
        t = Simulacao(self, otm)
        self.setCentralWidget(t)

    def openbancodedados(self):
        t = GraficoParametro("Gráfico teste")
        self.setCentralWidget(t)

    def openhistoricosimu(self):
        t = Historico()
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
