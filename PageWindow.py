from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class PageWindow(QWidget):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


def adjustlabel(lbl):
    lbl.setStyleSheet("""
                        QWidget {
                        font: Helvetica;
                        border: 1px solid black;
                        border-radius: 5px;
                        font-size: 14px;
                        padding: 5px;
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
