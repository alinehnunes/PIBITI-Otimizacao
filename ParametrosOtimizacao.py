from math import inf


class Parametro:
    def __init__(self, n):
        self.nome = n
        self.limiteInf = -inf
        self.limiteSup = inf

    def setlimites(self, linf, lsup):
        self.limiteInf = linf
        self.limiteSup = lsup

class Variedade:
    def __init__(self, n):
        self.nome = n



class Otimizacao:
    def __init__(self):
        self.parametros = []
        self.qntvariedades = 0
        self.variedades = []

    def addparametro(self, parametro):
        self.parametros.append(parametro)

    def addvariedade(self, variedade):
        self.variedades.append(variedade)
