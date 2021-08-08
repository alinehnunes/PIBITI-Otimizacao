from Database import Database
from PyQt5.QtWidgets import *
from ParametrosOtimizacao import Otimizacao
from Variedade import Variedade


class Basedados(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.dataframe = None
        self.tablewidget = None
        self.leituradados()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.openbase(self.dataframe))
        self.setLayout(self.layout)
        self.listavariedades = self.createVariedades(self.dataframe)

    def leituradados(self):
        d = Database()
        d.connectdb()
        self.dataframe = d.leituravariedades()


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

