import datetime
from math import inf
import datetime

class Parametro:
    def __init__(self, n):
        self.nome = n
        self.limiteInf = -inf
        self.limiteSup = inf

        if self.nome == 'pH':
            self.limiteInf = 4
            self.limiteSup = 6

        if self.nome == 'Pol':
            self.limiteInf = 14
            self.limiteSup = 100

        if self.nome == 'Pureza':
            self.limiteInf = 0.85
            self.limiteSup = 1

        if self.nome == 'ATR':
            self.limiteInf = 0.15
            self.limiteSup = 1

        if self.nome == 'AR':
            self.limiteInf = 0
            self.limiteSup = 0.008

        if self.nome == 'Fibra':
            self.limiteInf = 0.11
            self.limiteSup = 0.13

    def setlimites(self, linf, lsup):
        self.limiteInf = linf
        self.limiteSup = lsup

    def setlimiteSup(self, lsup):
        self.limiteSup = lsup

    def setlimiteInf(self, linf):
        self.limiteInf = linf

class Otimizacao():
    def __init__(self):
        self.nome = None
        self.parametros = []
        self.qtdvariedades = 0
        self.variedades = []
        self.resultado = None
        self.time = None

    def addparametro(self, parametro):
        self.parametros.append(parametro)

    def addvariedade(self, variedade):
        self.variedades.append(variedade)

    def getqtdvariedades(self):
        self.qtdvariedades = len(self.variedades)
        return self.qtdvariedades

    def addnome(self, texto):
        self.nome = str(texto)

    def addtime(self):
        self.time = datetime.datetime.now()
