from math import inf
import mongoengine


class Parametro:
    def __init__(self, n):
        self.nome = n
        self.limiteInf = -inf
        self.limiteSup = inf

    def setlimites(self, linf, lsup):
        self.limiteInf = linf
        self.limiteSup = lsup


class Otimizacao(mongoengine.Document):
    def __init__(self):
        self.parametros = []
        self.qtdvariedades = 0
        self.variedades = []

    def addparametro(self, parametro):
        self.parametros.append(parametro)

    def addvariedade(self, variedade):
        self.variedades.append(variedade)

    def setqtdvariedades(self, qtdvariedades):
        self.qtdvariedades = qtdvariedades
