import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, xmin, xmax, px, parent=None, width=2, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.xmin = xmin
        self.xmax = xmax
        self.px = px
        super(MplCanvas, self).__init__(fig)


def returnimg(titulo, xmin, xmax, px):
    sc = MplCanvas(xmin, xmax, px, width=2, height=4, dpi=100)
    sc.axes.set_xlim(0, 8)
    sc.axes.set_ylim(0, 4)
    y = 2
    height = 1

    plt.clf()
    plt.title(titulo)
    plt.hlines(y, sc.xmin, sc.xmax)
    plt.vlines(sc.xmin, y - height / 2., y + height / 2.)
    plt.vlines(sc.xmax, y - height / 2., y + height / 2.)
    plt.plot(sc.px, y, 'bo', ms=15, mfc='b')

    plt.text(sc.xmin, y, sc.xmin, horizontalalignment='right')
    plt.text(sc.xmax, y, sc.xmax, horizontalalignment='left')

    plt.annotate('Valor Calculado:' + str(round(px,2)), (sc.px, y), xytext=(sc.px, y + 0.3),
                 arrowprops=dict(facecolor='black'),
                 horizontalalignment='right')
    plt.axis('off')

    img = plt.gcf()
    canvas = FigureCanvasQTAgg(img)
    canvas.resize(1500, 1000)
    canvas.draw()
    w, h = canvas.get_width_height()
    aux = QImage(canvas.buffer_rgba(), w, h, QImage.Format_RGBA8888)
    im = QPixmap(aux)
    imf = im.scaled(360, 360, QtCore.Qt.KeepAspectRatio)
    return imf
