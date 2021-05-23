import pandas as pd
from PyQt5.QtWidgets import *


class Basedados(QWidget):

    def __init__(self, nomearquivo, nomeplanilha, parent=None):
        super().__init__(parent)

        self.dataframe = None
        self.tablewidget = None
        self.leituradados(nomearquivo, nomeplanilha)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.openbase(self.dataframe))
        self.setLayout(self.layout)
        self.listavariedades = []
        for i in range(len(self.dataframe.index)):
            for j in range(len(self.dataframe.columns)):
                variedade = Variedade(self.dataframe.iloc[i, j])
            print(variedade.nome)
            print(variedade.custo)
            print(variedade.ph)
            print(variedade.pf)
            print(variedade.pe)
            print(variedade.viscosidade)
            print(variedade.brix)
            print(variedade.pol)
            print(variedade.cor)
            self.listavariedades.append(variedade)
        print(self.listavariedades)


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

        return self.tablewidget


class Variedade:
    def __init__(self, nome="", custo=0, ph=7, pf=0, pe=100, brix=0, pol=0, viscosidade=0, cor=0):
        self.nome = nome
        self.custo = custo
        self.ph = ph
        self.pf = pf
        self.pe = pe
        self.brix = brix
        self.pol = pol
        self.viscosidade = viscosidade
        self.cor = cor


