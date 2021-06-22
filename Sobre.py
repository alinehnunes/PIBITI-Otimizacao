from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap


class Sobre(QWidget):

    def __init__(self):
        super().__init__()

        info = QLabel("Projeto de PIBITI desenvolvido na Universidade Federal de Alagoas")
        orientador = QLabel('Orientador: Rodolfo Junqueira Brandão')
        participantes = QLabel('Participantes: Aline Rodrigues Nunes, Rafael Domingos Nobre de Araújo')
        adjustlabel(info)
        adjustlabel(orientador)
        adjustlabel(participantes)
        img = QLabel()
        imagem = QPixmap("Brasão_Ufal.png")
        imagemcorrigida = imagem.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        img.setPixmap(imagemcorrigida)
        adjustlabel(img)
        self.layout = QVBoxLayout()
        self.sublayout = QHBoxLayout()
        self.sublayout.addWidget(info)
        self.sublayout.addWidget(img)
        self.layout.addLayout(self.sublayout)
        self.layout.addWidget(orientador)
        self.layout.addWidget(participantes)
        self.layout.addStretch(1)
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
