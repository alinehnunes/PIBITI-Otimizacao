import pandas as pd
from PyQt5.QtWidgets import *
from ParametrosOtimizacao import Otimizacao


class Basedados(QWidget):

    def __init__(self, nomearquivo, nomeplanilha, parent=None):
        super().__init__(parent)

        self.dataframe = None
        self.tablewidget = None
        self.leituradados(nomearquivo, nomeplanilha)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.openbase(self.dataframe))
        self.setLayout(self.layout)
        self.listavariedades = self.createVariedades(self.dataframe)

    def leituradados(self, nomearquivo, nomepasta):
        dados = pd.ExcelFile(nomearquivo)
        dataframe = pd.read_excel(dados, nomepasta)
        self.dataframe = dataframe

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

    def createVariedades(self, dataframe):
        listavariedades = {}
        for i in range(len(dataframe.index)):
            variedade = Variedade(*dataframe.loc[i])
            listavariedades[variedade.nome] = variedade
        return listavariedades


class Variedade:
    def __init__(self, nome="", custo=0, ph=7, pol=0, pureza=1, atr=1, ar=1, fibra=1):
        self.nome = nome
        self.custo = custo
        self.ph = ph
        self.pol = pol
        self.pureza = pureza
        self.atr = atr
        self.ar = ar
        self.fibra = fibra