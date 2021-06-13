import matplotlib
import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize
from ParametrosOtimizacao import Otimizacao
from ParametrosOtimizacao import Parametro

teste_otm = Otimizacao()
teste_otm.setqtdvariedades(3)

qtdvariedades = teste_otm.qtdvariedades

# Chute inicial
x0 = np.zeros(qtdvariedades)
x_inicial = 1/qtdvariedades

x0 = [x_inicial for i in range(qtdvariedades)] 

# Limites para as composições de cada álcool
LB = np.zeros(qtdvariedades)
UB = np.ones(qtdvariedades)
limites = Bounds(LB, UB)

custo = 0
pol = 0
pureza = 0 
atr = 0 
ar = 0 
fibra = 0

# Definição da função Objetivo - CUSTO (minimizar)
#def custo(x,teste_otm,custo):
def custo(x):
    custo = [custo+(teste_otm.variedades[i].custo*x[i]) for i in range(qtdvariedades)]
    return (-1)*custo

#restrição pol limite inferior
def pol1(x):
    pol = [pol+(teste_otm.variedades[i].pol*x[i]) for i in range(qtdvariedades)]
    return pol - Parametro("pol").limiteInf

#restrição pol limite superior
def pol2(x):
    pol = [pol+(teste_otm.variedades[i].pol*x[i]) for i in range(qtdvariedades)]
    return Parametro("pol").limiteSup - pol

#restrição pureza limite inferior
def pureza1(x):
    pureza = [pureza+(teste_otm.variedades[i].pureza*x[i]) for i in range(qtdvariedades)]
    return pureza - Parametro("pureza").limiteInf

#restrição pureza limite superior
def pureza2(x):
    pureza = [pureza+(teste_otm.variedades[i].pureza*x[i]) for i in range(qtdvariedades)]
    return Parametro("pureza").limiteSup - pureza

#restrição atr limite inferior
def atr1(x):
    atr = [atr+(teste_otm.variedades[i].atr*x[i]) for i in range(qtdvariedades)]
    return atr - Parametro("atr").limiteInf

#restrição atr limite superior
def atr2(x):
    atr = [atr+(teste_otm.variedades[i].atr*x[i]) for i in range(qtdvariedades)]
    return Parametro("atr").limiteSup - atr

#restrição ar limite inferior
def ar1(x):
    ar = [ar+(teste_otm.variedades[i].ar*x[i]) for i in range(qtdvariedades)]
    return ar - Parametro("ar").limiteInf

#restrição atr limite superior
def ar2(x):
    ar = [ar+(teste_otm.variedades[i].ar*x[i]) for i in range(qtdvariedades)]
    return Parametro("ar").limiteSup - ar

#restrição fibra limite inferior
def fibra1(x):
    fibra = [fibra+(teste_otm.variedades[i].fibra*x[i]) for i in range(qtdvariedades)]
    return fibra - Parametro("fibra").limiteInf

#restrição fibra limite superior
def fibra2(x):
    fibra = [fibra+(teste_otm.variedades[i].fibra*x[i]) for i in range(qtdvariedades)]
    return Parametro("fibra").limiteSup - fibra

def composicao(x):
    return sum(x) - 1

#restrições
pol1 = {'type': 'ineq', 'fun': pol1}
pol2 = {'type': 'ineq', 'fun': pol2}
pureza1 = {'type': 'ineq', 'fun': pureza1}
pureza2 = {'type': 'ineq', 'fun': pureza2}
atr1 = {'type': 'ineq', 'fun': atr1}
atr2 = {'type': 'ineq', 'fun': atr2}
ar1 = {'type': 'ineq', 'fun': ar1}
ar2 = {'type': 'ineq', 'fun': ar2}
fibra1 = {'type': 'ineq', 'fun': fibra1}
fibra2 = {'type': 'ineq', 'fun': fibra2}
composicao = {'type': 'eq', 'fun': composicao}

restricoes = [pol1, pol2, pureza1, pureza2, atr1, atr2, ar1, ar2, fibra1, fibra2, composicao]

solucao = minimize(custo, x0, method='SLSQP', bounds=limites, constraints=restricoes)
print(solucao)
