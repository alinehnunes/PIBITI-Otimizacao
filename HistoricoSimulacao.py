from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from Database import Database
from ParametrosOtimizacao import Otimizacao
import datetime


class Historicosimulacao(QWidget):

    def __init__(self):
        super().__init__()

        self.dataframe = None
        self.leiturahistorico()

        self.layout = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QVBoxLayout()

        self.tablewidget = QTableWidget()
        self.textoaux = QLabel("Essa é a simulação escolhida:")
        self.listaescolhida = QListWidget()
        self.botaoapagar = QPushButton("Apagar simulação do Histórico")
        self.botaoapagar.clicked.connect(self.removeitem)
        self.botaoacessar = QPushButton("Acessar simulação")
        self.layout.addWidget(self.openbase(self.dataframe))
        self.layout.addWidget(self.textoaux)
        self.layout2.addWidget(self.listaescolhida)
        self.layout3.addWidget(self.botaoapagar)
        self.layout3.addWidget(self.botaoacessar)
        self.layout2.addLayout(self.layout3)
        self.layout.addLayout(self.layout2)
        self.setLayout(self.layout)

    def eventFilter(self, source, event):
        if self.tablewidget.selectedIndexes() != []:
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    row = self.tablewidget.currentRow()
                    self.addlist(row)

        return QtCore.QObject.event(source, event)

    def addlist(self, row):
        escolhido = self.tablewidget.item(row, 0).text()
        self.listaescolhida.clear() # Verificar se esse método realmente limpa a lista
        self.listaescolhida.addItem(escolhido)

    def leiturahistorico(self):
        d = Database()
        d.connectdb()
        self.dataframe = d.leiturahistorico()

    def openbase(self, dataframe):

        self.tablewidget = QTableWidget()

        linhas = self.dataframe.index
        numlinhas = len(linhas)
        self.tablewidget.setRowCount(numlinhas)

        colunas = self.dataframe.columns
        numcolunas = len(colunas)
        self.tablewidget.setColumnCount(numcolunas)

        self.tablewidget.setHorizontalHeaderLabels(dataframe)

        for i in range(numlinhas):
            for j in range(numcolunas):
                aux = self.dataframe.iloc[i, j]
                aux2 = str(aux)
                self.tablewidget.setItem(i, j, QTableWidgetItem(aux2))

        self.tablewidget.viewport().installEventFilter(self)
        return self.tablewidget

    def removeitem(self):
        deletelist = self.listaescolhida.selectedItems()
        if not deletelist:
            return
        for item in deletelist:
            self.listaescolhida.takeItem(self.listaescolhida.row(item))

# Ainda não implementado

    def opensimu(self):
        # from OtimizacaoQT import w
        # objotimizacao = self.createobjotim()
        # w.opennovasimulacao()
        pass


    def createobjotim(self):
        pass