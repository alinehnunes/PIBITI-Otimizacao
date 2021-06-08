import sys
from random import randint

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from BaseDados import Basedados
from ParametrosOtimizacao import Otimizacao, Parametro

Otimizacao = Otimizacao()


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

        btnvariedades = QPushButton("Escolhe Limites")
        btnvariedades.clicked.connect(self.checarselecionados)
        btnvariedades.clicked.connect(self.goToLimiteParametros)
        self.layout.addWidget(btnvariedades)
        self.setLayout(self.layout)

    def checarselecionados(self):
        Otimizacao.parametros = []
        for botao in self.listabotoes:
            param = Parametro(botao.text())
            if botao.checkState():
                Otimizacao.addparametro(param)

    def goToLimiteParametros(self):
        self.goto("LimiteParametros")


class LimiteParametros(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layoutprincipal = QVBoxLayout()
        info = QLabel('Selecione os limites de otimização para os parâmetros escolhidos')
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(info)
        self.layoutprincipal.addLayout(self.layout1)
        self.layout2 = QVBoxLayout()
        self.layout3 = QHBoxLayout()
        btnvoltarselecao = QPushButton('Voltar para selecao de parâmetros')
        btnvoltarselecao.clicked.connect(self.goToSelecaoParametros)
        btnescolhervar = QPushButton('Escolher Variedades')
        btnescolhervar.clicked.connect(self.goToSelecaoVariedades)
        self.layout3.addWidget(btnvoltarselecao)
        self.layout3.addWidget(btnescolhervar)
        self.layoutprincipal.addLayout(self.layout2)
        self.layoutprincipal.addLayout(self.layout3)

        self.setLayout(self.layoutprincipal)


    def goToSelecaoParametros(self):
        self.goto("SelecaoParametros")

    def goToSelecaoVariedades(self):
        self.goto("SelecaoVariedades")

    def showEvent(self, ev):

        while self.layout2.count() > 0:
            self.layout2.itemAt(0).setParent(None)
        for i in range(len(Otimizacao.parametros)):
            self.layoutvar = QHBoxLayout()
            nomevar = QLabel(Otimizacao.parametros[i].nome)
            limiteinf = QLineEdit()
            limiteinf.setPlaceholderText("Limite Inferior do parâmetro")
            limitesup = QLineEdit()
            limitesup.setPlaceholderText("Limite Superior do parâmetro")
            self.layoutvar.addWidget(nomevar)
            self.layoutvar.addWidget(limiteinf)
            self.layoutvar.addWidget(limitesup)
            self.layout2.addLayout(self.layoutvar)
            self.layoutprincipal.addLayout(self.layout2)

        return QWidget.showEvent(self, ev)


class SelecaoVariedades(PageWindow, Basedados):
    def __init__(self, nomearquivo, nomeplanilha, parent=None):
        super().__init__(nomearquivo, nomeplanilha, parent)
        grafico = QLabel('Teste')
        self.layout.addWidget(grafico)
        listaselecionadas = QListWidget()
        self.layout.addWidget(listaselecionadas)
        self.layout2 = QHBoxLayout()
        btnvoltarqnt = QPushButton('Voltar para seleção de limites')
        btnvoltarqnt.clicked.connect(self.goToLimiteParametros)
        btnlimitepar = QPushButton('Otimizar')
        btnlimitepar.clicked.connect(self.goToOtimizar)
        self.layout2.addWidget(btnvoltarqnt)
        self.layout2.addWidget(btnlimitepar)
        self.layout.addLayout(self.layout2)

    def goToLimiteParametros(self):
        self.goto("LimiteParametros")

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

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(Selecaoparametros(), "SelecaoParametros")
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