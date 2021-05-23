from math import inf


class Parametro:
    def __init__(self):
        self.nome = ""
        self.limiteInf = -inf
        self.limiteSup = inf


class ParametrosOtimizacao:
    def __init__(self):
        self.parametros = []
        self.qntvariedades = 0
        self.variedades = []

    def addparametro(self, parametro):
        self.parametros.append(parametro)

    def addvariedade(self, variedade):
        self.variedades.append(variedade)
