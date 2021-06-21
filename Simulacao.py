import sys
from random import randint

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
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
        layout.addWidget(botao)

    def __init__(self):
        super().__init__()

        info = QLabel("Selecione os parâmetros a serem otimizados")
        adjustlabel(info)
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
        self.layout.addWidget(btnvariedades)
        self.setLayout(self.layout)

    def checarselecionados(self):
        Otimizacao.parametros = []
        checkedbuttons = []
        for botao in self.listabotoes:
            param = Parametro(botao.text())
            if botao.checkState():
                Otimizacao.addparametro(param)
                checkedbuttons.append(botao)
        if len(checkedbuttons) == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Adicionar Parametros")
            msg.setText("Favor selecionar no mínimo um parâmetro para avançar")
            msg.exec_()
        else:
            self.goToLimiteParametros()

    def goToLimiteParametros(self):
        self.goto("LimiteParametros")


class LimiteParametros(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layoutprincipal = QVBoxLayout()
        info = QLabel('Selecione os limites de otimização para os parâmetros escolhidos')
        adjustlabel(info)
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(info)
        self.layout1.setAlignment(Qt.AlignCenter)
        self.layoutprincipal.addLayout(self.layout1)
        self.layout2 = QGridLayout()
        self.layout3 = QHBoxLayout()
        self.layoutprincipal.addLayout(self.layout2)
        btnvoltarselecao = QPushButton('Voltar para selecao de parâmetros')
        btnvoltarselecao.clicked.connect(self.goToSelecaoParametros)
        btnescolhervar = QPushButton('Escolher Variedades')
        btnescolhervar.clicked.connect(self.goToSelecaoVariedades)
        self.layout3.addWidget(btnvoltarselecao)
        self.layout3.addWidget(btnescolhervar)
        self.layout3.setAlignment(Qt.AlignBottom)
        self.layoutprincipal.addLayout(self.layout3)

        self.setLayout(self.layoutprincipal)

    def cleanlayout(self, layout):
        items = []
        for i in range(layout.count()):
            items.append(layout.itemAt(i))
        for w in items:
            w.widget().deleteLater()

    def goToSelecaoParametros(self):
        self.cleanlayout(self.layout2)
        self.goto("SelecaoParametros")

    def goToSelecaoVariedades(self):
        self.goto("SelecaoVariedades")
        self.addlimites()

    def showEvent(self, ev):

        self.cleanlayout(self.layout2)
        for i in range(len(Otimizacao.parametros)):
            nomevar = QLabel(Otimizacao.parametros[i].nome)
            limiteinf = QLineEdit()
            limiteinf.setPlaceholderText("Limite Inferior do parâmetro")
            limitesup = QLineEdit()
            limitesup.setPlaceholderText("Limite Superior do parâmetro")
            self.layout2.addWidget(nomevar, i, 0)
            self.layout2.addWidget(limiteinf, i, 1)
            self.layout2.addWidget(limitesup, i, 2)
            self.layout2.setAlignment(Qt.AlignCenter)
        self.layoutprincipal.addLayout(self.layout2)
        return QWidget.showEvent(self, ev)

    def addlimites(self):
        for i in range(len(Otimizacao.parametros)):
            limiteinf = self.layout2.itemAtPosition(i, 1).widget().text()
            limitesup = self.layout2.itemAtPosition(i, 2).widget().text()
            Otimizacao.parametros[i].setlimites(limiteinf, limitesup)
            print("o parametro", Otimizacao.parametros[i].nome, "tem limites", Otimizacao.parametros[i].limiteInf, "e", Otimizacao.parametros[i].limiteSup )


class SelecaoVariedades(PageWindow, Basedados):
    def __init__(self, nomearquivo, nomeplanilha, parent=None):
        super().__init__(nomearquivo, nomeplanilha, parent)
        infoselecao = QLabel('Selecione as variedades escolhidas na tabela acima')
        self.sublayout = QHBoxLayout()
        self.layout.addWidget(infoselecao)
        self.listaselecionadas = QListWidget()
        self.sublayout.addWidget(self.listaselecionadas)
        btnapagar = QPushButton('Apagar Variedade')
        btnapagar.clicked.connect(self.removeitem)
        self.sublayout.addWidget(btnapagar)
        self.layout2 = QHBoxLayout()
        btnvoltarqnt = QPushButton('Voltar para seleção de limites')
        btnvoltarqnt.clicked.connect(self.goToLimiteParametros)
        btnlimitepar = QPushButton('Otimizar')
        btnlimitepar.clicked.connect(self.goToOtimizar)
        self.layout2.addWidget(btnvoltarqnt)
        self.layout2.addWidget(btnlimitepar)
        self.layout.addLayout(self.sublayout)
        self.layout.addLayout(self.layout2)

    def goToLimiteParametros(self):
        self.goto("LimiteParametros")

    def goToOtimizar(self):
        self.goto("Otimizar")

    def eventFilter(self, source, event):
        if self.tablewidget.selectedIndexes() != []:
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    row = self.tablewidget.currentRow()
                    self.addlist(row)

        return QtCore.QObject.event(source, event)

    def addlist(self, row):
        escolhido = self.tablewidget.item(row, 0).text()
        check = True
        for i in range(self.listaselecionadas.count()):
            if escolhido == self.listaselecionadas.item(i).text():
                check = False
            else:
                pass
        if check:
            self.listaselecionadas.addItem(escolhido)

    def removeitem(self):
        deletelist = self.listaselecionadas.selectedItems()
        if not deletelist:
            return
        for item in deletelist:
            self.listaselecionadas.takeItem(self.listaselecionadas.row(item))


class Otimizar(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        info = QLabel("Resultado da Otimização")
        adjustlabel(info)
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
        adjustlabel(texto)
        texto.setAlignment(Qt.AlignCenter)
        img = QLabel()
        img.setFrameStyle(QFrame.Panel)
        img.setLineWidth(2)
        imagem = QPixmap("CanadeAcucar.jfif")
        img.setPixmap(imagem)
        self.layout.addWidget(texto)
        self.layout.addWidget(img)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)


def adjustlabel(lbl):
    lbl.setFont(QFont('Helvetica', 12))
    lbl.setFrameStyle(QFrame.Panel)
