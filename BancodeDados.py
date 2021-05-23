from PyQt5.QtWidgets import QLabel
from BaseDados import Basedados
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MplCanvas(FigureCanvas):
    def __init__(self, title, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

        x = np.linspace(0, 2 * np.pi, 400)
        y = (x ** 2)
        p = self.figure.subplots()
        title = "grafico teste"
        p.plot(x, y)
        p.set_title(title)
    

class GraficoParametro(Basedados):

    def __init__(self, nomearquivo, nomeplanilha, parent=None):
        super().__init__(nomearquivo, nomeplanilha, parent)
        grafico = MplCanvas(self, "Grafico Inicial")
        # grafico.axes.bar(["var1", "var2", "var3", "var4", "var5", "var6"], [3, 4, 5, 6, 3, 5])

        info = QLabel("Selecione o Parâmetro para ser comparado na tabela acima")
        self.layout.addWidget(info)
        self.layout.addWidget(grafico)


    def plotargraf(self, linhas, colunas):
        labels = self.linhas
        values = self.colunas

        plt.bar(labels, values)

        plt.figure(figsize=())

        plt.show()
