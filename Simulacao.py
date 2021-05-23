import sys
from random import randint

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from BaseDados import Basedados


class PageWindow(QWidget):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class Selecaoparametros(PageWindow):

    def botaocheck(self, nome):
        botao = QCheckBox(nome)
        botao.setCheckState(Qt.Unchecked)
        return botao

    def colocarbotao(self, layout, botao):
        self.layout.addWidget(botao)

    def __init__(self):
        super().__init__()

        info = QLabel("Selecione os parâmetros a serem otimizados")
        self.layout = QVBoxLayout()
        self.layout.addWidget(info)
        parametros = ['Custo', 'pH', 'Ponto de Fusão', 'Ponto de Ebulição', 'Brix', 'Pol', 'Viscosidade', 'Cor']
        self.listabotoes = []

        for i in range(len(parametros)):
            botao = self.botaocheck(parametros[i])
            self.colocarbotao(self.layout, botao)
            self.listabotoes.append(botao)

        btnvariedades = QPushButton("Selecionar Variedades")
        btnvariedades.clicked.connect(self.goToQntVariedades)
        btnvariedades.clicked.connect(self.checarselecionados)
        self.layout.addWidget(btnvariedades)
        self.setLayout(self.layout)

    def checarselecionados(self):
        selecionados = []
        for botao in self.listabotoes:
            if botao.checkState():
                selecionados.append(botao)
        print(selecionados)

    def goToQntVariedades(self):
        self.checarselecionados()
        self.goto("QntVariedades")


class QntVariedades(PageWindow):
    def __init__(self):
        super().__init__()

        info = QLabel("Selecione a Quantidade de Variedades de Álcool")

        quantvar = ["2", "3", "4", "5", "6", "7", "8", "9"]

        btnselecionarvar = QPushButton("Escolher Variedades")
        btnselecionarvar.clicked.connect(self.goToSelecaoVariedades)
        btnvoltarparametros = QPushButton("Voltar para seleção de parametros")
        btnvoltarparametros.clicked.connect(self.goToSelecaoParametros)
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.caixavar = QComboBox()
        self.caixavar.addItems(quantvar)
        self.layout1.addWidget(info)
        self.layout1.addWidget(self.caixavar)
        self.layout2.addWidget(btnvoltarparametros)
        self.layout2.addWidget(btnselecionarvar)
        self.layout1.addLayout(self.layout2)
        self.setLayout(self.layout1)

    def qntselecionada(self):
        numvar = int(self.caixavar.currentText())
        print(numvar)

    def goToSelecaoParametros(self):
        self.goto("SelecaoParametros")

    def goToSelecaoVariedades(self):
        self.qntselecionada()
        self.goto("SelecaoVariedades")


class SelecaoVariedades(PageWindow, Basedados):
    def __init__(self, nomearquivo, nomeplanilha, parent=None):
        super().__init__(nomearquivo, nomeplanilha, parent)
        grafico = QLabel('Teste')
        self.layout.addWidget(grafico)
        listaselecionadas = QListWidget()
        self.layout.addWidget(listaselecionadas)
        self.layout2 = QHBoxLayout()
        btnvoltarqnt = QPushButton('Voltar para quantidade de variedades')
        btnvoltarqnt.clicked.connect(self.goToQntVariedades)
        btnlimitepar = QPushButton('Avançar para seleção de Limites')
        btnlimitepar.clicked.connect(self.goToLimiteParametro)
        self.layout2.addWidget(btnvoltarqnt)
        self.layout2.addWidget(btnlimitepar)
        self.layout.addLayout(self.layout2)

    def goToQntVariedades(self):
        self.goto("QntVariedades")

    def goToLimiteParametro(self):
        self.goto("LimiteParametros")


class LimiteParametros(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        info = QLabel('Selecione os limites de otimização para os parâmetros escolhidos')
        self.layout.addWidget(info)

        for i in range(7):
            self.layoutvar = QHBoxLayout()
            nomevar = QLineEdit()
            limiteinf = QLineEdit()
            limiteinf.setPlaceholderText("Limite Inferior do parâmetro")
            limitesup = QLineEdit()
            limitesup.setPlaceholderText("Limite Superior do parâmetro")
            self.layoutvar.addWidget(nomevar)
            self.layoutvar.addWidget(limiteinf)
            self.layoutvar.addWidget(limitesup)
            self.layout.addLayout(self.layoutvar)

        btnvoltarselecao = QPushButton('Voltar para selecao de variedades')
        btnvoltarselecao.clicked.connect(self.goToSelecaoVariedades)
        btnotimizar = QPushButton('Otimizar')
        btnotimizar.clicked.connect(self.goToOtimizar)
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(btnvoltarselecao)
        self.layout2.addWidget(btnotimizar)
        self.layout.addLayout(self.layout2)
        self.setLayout(self.layout)

    def goToSelecaoVariedades(self):
        self.goto("SelecaoVariedades")

    def goToOtimizar(self):
        self.goto("Otimizar")


class Otimizar(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        info = QLabel("Resultado da Otimização")
        self.layout.addWidget(info)
        self.setLayout(self.layout)


class Simulacao(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()
        #self.setCentralWidget(self.stacked_widget)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(Selecaoparametros(), "SelecaoParametros")
        self.register(QntVariedades(), "QntVariedades")
        self.register(SelecaoVariedades("Base de dados inicial.xls", "Planilha1"), "SelecaoVariedades")
        self.register(LimiteParametros(), "LimiteParametros")
        self.register(Otimizar(), "Otimizar")

        self.goto("SelecaoParametros")
        self.setLayout(self.layout)

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


class PaginaInicial(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        texto = QLabel("Otimização em Python")
        img = QLabel()
        imagem = QPixmap("CanadeAcucar.jfif")
        img.setPixmap(imagem)
        self.layout.addWidget(texto)
        self.layout.addWidget(img)
        self.setLayout(self.layout)