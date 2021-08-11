from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from Database import Database
from Otimizacao import otimizar
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget
from PageWindow import PageWindow, adjustlabel, adjustbotao, adjustlineedit, createmessage
from PyQt5.QtCore import Qt
from datetime import datetime
from ParametrosOtimizacao import Otimizacao
import Returnimg

#d = Database()
#d.connectdb()
#Otimizacao = Database.leiturasimulacao(d, 5)
Otimizacao = Otimizacao()

class Historico(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stacked_widget)

        self.m_pages = {}
        self.register(Historicosimulacao(), "HistóricoSimulacao")
        self.register(Otimizar(), "Otimizar")
        self.register(Graficos(), "Gráficos")

        self.goto("HistóricoSimulacao")

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


class Historicosimulacao(PageWindow):

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
        self.botaoacessar.clicked.connect(self.opensimu)
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

    def opensimu(self):
        itematual = int(self.listaescolhida.item(0).text())
        d = Database()
        d.connectdb()
        o = Database.leiturasimulacao(d, itematual)
        Otimizacao.copyotm(o)
        Otimizacao.resultado = otimizar(Otimizacao)
        self.gotoOtimizar()

    def gotoOtimizar(self):
        self.goto("Otimizar")


class Otimizar(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        info = QLabel("Resultado da Otimização")
        adjustlabel(info)
        self.layout.addWidget(info)
        self.layout.addStretch(1)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layoutinfos = QGridLayout()
        self.layoutgrafs = QGridLayout()
        self.sublayout = QHBoxLayout()
        btnavancar = QPushButton('Avançar')
        btnavancar.clicked.connect(self.avancargrafs)
        self.sublayout.addWidget(btnavancar)
        self.setLayout(self.layout)

    def showEvent(self, ev):

        success = None

        if Otimizacao.resultado['success'] == True:
            success = QLabel('A otimização foi um sucesso')
        else:
            success = QLabel('A otimização foi falha\nO método não convergiu!')

        adjustlabel(success)

        self.layoutinfos.addWidget(success, 0, 0, 1, len(Otimizacao.parametros))

        qntparametros = QLabel('Parametros selecionados:')
        adjustlabel(qntparametros)
        self.layoutinfos.addWidget(qntparametros, 1, 0, 1, len(Otimizacao.parametros))
        for i in range(len(Otimizacao.parametros)):
            par = Otimizacao.parametros[i]
            parnome = str(par.nome)
            parlimiteinf = str(par.limiteInf)
            parlimitesup = str(par.limiteSup)
            parametrosoti = QLabel(f"{parnome}:"
                                   f" \nLimite inferior: {parlimiteinf}"
                                   f" \nLimite superior: {parlimitesup}")
            adjustbotao(parametrosoti)
            self.layoutinfos.addWidget(parametrosoti, 2, i)

        qntvariedades = QLabel('Composições das variedades escolhidas:')
        adjustlabel(qntvariedades)
        self.layoutinfos.addWidget(qntvariedades, 3, 0, 1, len(Otimizacao.variedades))
        for i in range(len(Otimizacao.variedades)):
            var = Otimizacao.variedades[i]
            variedadesoti = QLabel(var.nome + ': ' + str(round(Otimizacao.resultado['x'][i] * 100, 2)) + '%')
            adjustbotao(variedadesoti)
            self.layoutinfos.addWidget(variedadesoti, 4, i)

        if Otimizacao.resultado['success'] == True:

            # Resultado da otimizacão
            parametros_resultado = QLabel('Valores dos parâmetros:')
            adjustlabel(parametros_resultado)
            self.layoutinfos.addWidget(parametros_resultado, 5, 0, 1, 2)

            custo = QLabel('Custo: R$' + str(round(Otimizacao.resultado['Custo'],2)))
            adjustbotao(custo)
            self.layoutinfos.addWidget(custo, 6 , 0)

            ph = QLabel('pH: ' + str(round(Otimizacao.resultado['pH'],2)))
            adjustbotao(ph)
            self.layoutinfos.addWidget(ph, 7 ,0)

            pol = QLabel('Pol: ' + str(round(Otimizacao.resultado['Pol'],2)))
            adjustbotao(pol)
            self.layoutinfos.addWidget(pol, 7, 1)

            pureza = QLabel('Pureza: ' + str(round(Otimizacao.resultado['Pureza']*100,2)) + '%')
            adjustbotao(pureza)
            self.layoutinfos.addWidget(pureza, 8, 0)

            atr = QLabel('ATR: ' + str(round(Otimizacao.resultado['ATR']*100,2)) + '%')
            adjustbotao(atr)
            self.layoutinfos.addWidget(atr, 8, 1)

            ar = QLabel('AR: ' + str(round(Otimizacao.resultado['AR']*100,2)) + '%')
            adjustbotao(ar)
            self.layoutinfos.addWidget(ar, 9, 0)

            fibra = QLabel('Fibra: ' + str(round(Otimizacao.resultado['Fibra']*100,2)) + '%')
            adjustbotao(fibra)
            self.layoutinfos.addWidget(fibra, 9, 1)

        self.layoutinfos.setAlignment(Qt.AlignCenter)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.layoutinfos)
        self.layout.addLayout(self.sublayout)

        return QWidget.showEvent(self, ev)

    def avancargrafs(self):
        self.cleanlayout(self.layoutinfos)
        self.goto('Gráficos')

    def cleanlayout(self, layout):
        items = []
        for i in range(layout.count()):
            items.append(layout.itemAt(i))
        for w in items:
            w.widget().deleteLater()


class Graficos(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        texto = QLabel('Resultados da otimização')
        adjustlabel(texto)
        self.layout = QVBoxLayout()
        self.layout.addWidget(texto)
        self.layoutname = QHBoxLayout()
        self.layoutgrafs = QGridLayout()
        self.sublayout = QHBoxLayout()
        self.btnretornar = QPushButton('Retornar para resultados')
        self.btnretornar.clicked.connect(self.retornar)
        self.btnvoltarinicio = QPushButton('Retornar ao início')
        self.btnvoltarinicio.clicked.connect(self.close)
        self.setLayout(self.layout)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.parent().parent().parent().openpaginainicial()

    def retornar(self):
        self.goto("Otimizar")
        self.cleanlayout(self.layoutname)

    def cleanlayout(self, layout):
        items = []
        for i in range(layout.count()):
            items.append(layout.itemAt(i))
        for w in items:
            w.widget().deleteLater()

    def showEvent(self, ev):
        self.sublayout.addWidget(self.btnvoltarinicio)
        self.sublayout.addWidget(self.btnretornar)
        lblnome = QLabel(f'Otimização escolhida: {Otimizacao.nome}')
        lblnome.setAlignment(Qt.AlignCenter)
        adjustlabel(lblnome)
        self.layoutname.addWidget(lblnome)
        for i in range(len(Otimizacao.parametros)):
            linf = Otimizacao.parametros[i].limiteInf
            lsup = Otimizacao.parametros[i].limiteSup
            nomepar = str(Otimizacao.parametros[i].nome)
            resultado = Otimizacao.resultado[nomepar]
            image = QLabel()
            texto = "Resultado do parâmetro " + nomepar
            graf = Returnimg.returnimg(texto, linf, lsup, resultado)
            image.setPixmap(graf)
            col = i % 3
            if i == 0 or i == 1 or i == 2:
                lin = 0
            else:
                lin = 1

            self.layoutgrafs.addWidget(image, lin, col)

        self.layout.addLayout(self.layoutname)
        self.layout.addLayout(self.layoutgrafs)
        self.layout.addLayout(self.sublayout)
