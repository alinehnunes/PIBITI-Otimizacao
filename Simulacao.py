from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from BaseDados import Basedados
from ParametrosOtimizacao import Otimizacao, Parametro
from Otimizacao import otimizar
import math

Otimizacao = Otimizacao()

class PageWindow(QWidget):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class Selecaoparametros(PageWindow):

    def botaocheck(self, nome):
        botao = QCheckBox(nome)
        adjustbotao(botao)
        return botao

    def colocarbotao(self, layout, botao):
        layout.addWidget(botao)

    def __init__(self):
        super().__init__()

        info = QLabel("Selecione os parâmetros a serem otimizados")
        adjustlabel(info)
        self.layoutprincipal = QVBoxLayout()
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(info)
        self.layout1.addStretch(1)
        self.layout1.setAlignment(Qt.AlignHCenter)
        self.layoutprincipal.addLayout(self.layout1)
        self.layout2 = QVBoxLayout()
        parametros = ['Custo', 'pH', 'Pol', 'Pureza', 'ATR', 'AR', 'Fibra']
        self.listabotoes = []
        for i in range(len(parametros)):
            botao = self.botaocheck(parametros[i])
            self.colocarbotao(self.layout2, botao)
            self.listabotoes.append(botao)

        self.layout2.addStretch(1)
        btnlimites = QPushButton("Escolher Limites")
        btnlimites.clicked.connect(self.checarselecionados)
        self.layoutprincipal.addLayout(self.layout2)
        self.layoutprincipal.addWidget(btnlimites)
        self.setLayout(self.layoutprincipal)

    def checarselecionados(self):
        Otimizacao.parametros = []
        checkedbuttons = []
        for botao in self.listabotoes:
            param = Parametro(botao.text())
            if botao.checkState():
                Otimizacao.addparametro(param)
                checkedbuttons.append(botao)
        if len(checkedbuttons) == 0:
            createmessage("Adicionar Parametros", "Favor selecionar no mínimo um parâmetro para avançar")
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
        if self.checarlimites():
            self.addlimites()
            self.goto("SelecaoVariedades")
        else:
            pass

    def showEvent(self, ev):

        self.cleanlayout(self.layout2)
        for i in range(len(Otimizacao.parametros)):
            nomevar = QLabel(Otimizacao.parametros[i].nome)
            nomevar.setAlignment(Qt.AlignCenter)
            nomevar.setStyleSheet("""
                        QWidget {
                            border: 1px solid black;
                            border-radius: 5px;
                            font-size: 14px;
                            padding: 5px;
                            }
                        """)
            limiteinf = QLineEdit()
            limiteinf.setPlaceholderText("Limite Inferior do parâmetro")
            adjustlineedit(limiteinf)
            limitesup = QLineEdit()
            limitesup.setPlaceholderText("Limite Superior do parâmetro")
            adjustlineedit(limitesup)
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
            if limiteinf == '':
                limiteinf = -math.inf
            if limitesup == '':
                limitesup = math.inf
            limiteinf = float(limiteinf)
            limitesup = float(limitesup)
            Otimizacao.parametros[i].setlimites(limiteinf, limitesup)

    def checarlimites(self):
        for i in range(len(Otimizacao.parametros)):
            limiteinf = self.layout2.itemAtPosition(i, 1).widget().text()
            limitesup = self.layout2.itemAtPosition(i, 2).widget().text()
            if limiteinf == '':
                limiteinf = -math.inf
            if limitesup == '':
                limitesup = math.inf
            check = self.isvalid(limiteinf, limitesup)
            if not check:
                createmessage("Tipo inválido", "Favor utilizar apenas números nos campos de limites")
                return False
            if check:
                limiteinf = float(limiteinf)
                limitesup = float(limitesup)
                if limiteinf > limitesup:
                    createmessage("Erro Matemático", f'Limite inferior do parâmetro {Otimizacao.parametros[i].nome} '
                                                     f'maior que o limite superior')
                    return False
        return True

    def isvalid(self, resposta1, resposta2):
        if resposta1 == '' or resposta2 == '':
            return True
        else:
            try:
                float(resposta1)
                float(resposta2)
                return True
            except:
                return False


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
        btnotimizar = QPushButton('Otimizar')
        btnotimizar.clicked.connect(self.goToOtimizar)
        self.layout2.addWidget(btnvoltarqnt)
        self.layout2.addWidget(btnotimizar)
        self.layout.addLayout(self.sublayout)
        self.layout.addLayout(self.layout2)

    def conectarotimizacao(self):
        Otimizacao.variedades = []
        for i in range(self.listaselecionadas.count()):
            itematual = self.listaselecionadas.item(i).text()
            Otimizacao.addvariedade(self.listavariedades[itematual])
        Otimizacao.resultado = otimizar(Otimizacao)

    def goToLimiteParametros(self):
        self.goto("LimiteParametros")

    def goToOtimizar(self):
        if self.listaselecionadas.count() == 0:
            createmessage("Adicionar Variedades", "Favor selecionar no mínimo uma variedade para avançar")
        else:
            self.conectarotimizacao()
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
        self.layout.addStretch(1)
        self.layout.setAlignment(Qt.AlignCenter)
        self.sublayout = QHBoxLayout()
        btnsalvar = QPushButton('Salvar Simulação')
        btnvoltarinicio = QPushButton('Retornar ao início')
        btnvoltarinicio.clicked.connect(self.close)
        self.sublayout.addWidget(btnsalvar)
        self.sublayout.addWidget(btnvoltarinicio)
        self.setLayout(self.layout)

    def showEvent(self, ev):
        self.layoutinfos = QVBoxLayout()

        resultado_otm = QLabel('Resultado da Otimização:')
        adjustlabel(resultado_otm)
        self.layoutinfos.addWidget(resultado_otm)
        custo = QLabel('custo:' + str(Otimizacao.resultado['custo']))
        adjustbotao(custo)
        self.layoutinfos.addWidget(custo)

        qntparametros = QLabel('Parametros selecionados:')
        adjustlabel(qntparametros)
        self.layoutinfos.addWidget(qntparametros)
        for i in range(len(Otimizacao.parametros)):
            par = Otimizacao.parametros[i]
            parnome = str(par.nome)
            parlimiteinf = str(par.limiteInf)
            parlimitesup = str(par.limiteSup)
            parametrosoti = QLabel(parnome + ':  Limite inferior:  ' + parlimiteinf + ', Limite superiror:  ' +
                                   parlimitesup)
            adjustbotao(parametrosoti)
            self.layoutinfos.addWidget(parametrosoti)

        qntvariedades = QLabel('As variedades escolhidas foram:')
        adjustlabel(qntvariedades)
        self.layoutinfos.addWidget(qntvariedades)
        for i in range(len(Otimizacao.variedades)):
            var = Otimizacao.variedades[i]
            variedadesoti = QLabel(var.nome)
            adjustbotao(variedadesoti)
            self.layoutinfos.addWidget(variedadesoti)
        self.layoutinfos.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.layoutinfos)
        self.layout.addLayout(self.sublayout)

        return QWidget.showEvent(self, ev)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        print('Fechou')
        self.abrirpaginainicial()

    def abrirpaginainicial(self):
        from OtimizacaoQT import w
        w.acaopaginainicial()

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
        imagem = QPixmap("Cana2.jpg")
        imagemcorrigida = imagem.scaled(640, 640, QtCore.Qt.KeepAspectRatio)
        img.setPixmap(imagemcorrigida)
        self.layout.addWidget(texto)
        self.layout.addWidget(img)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)


def adjustlabel(lbl):
    lbl.setStyleSheet("""
                        QWidget {
                        font: Helvetica;
                        border: 1px solid black;
                        border-radius: 5px;
                        font-size: 14px;
                        }
                    """)


def adjustlineedit(lineedit):
    lineedit.setStyleSheet("""
                            border: 1px solid black;
                            border-radius: 15px;
                            padding: 8px;
                            background: gray;
                            selection - background - color: darkgray;
                            }
                        """)


def adjustbotao(botao):
    botao.setStyleSheet("""
        QWidget {
            border: 2px solid white;
            border-radius: 5px;
            min-width: 200px;
            max-width: 400px;
            font-size: 14px;
            padding: 5px;
            }
        """)


def createmessage(titulo, message):
    msg = QMessageBox()
    msg.setWindowTitle(titulo)
    msg.setText(message)
    msg.exec_()
