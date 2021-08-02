import matplotlib
import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize
from ParametrosOtimizacao import Otimizacao
from ParametrosOtimizacao import Parametro

def otimizar(objeto_otimizacao):

    qtdvariedades = objeto_otimizacao.getqtdvariedades()

    # Chute inicial
    x0 = np.zeros(qtdvariedades)
    x_inicial = 1/qtdvariedades

    x0 = [x_inicial for i in range(qtdvariedades)] 

    # Limites para as composições de cada variedade
    LB = np.zeros(qtdvariedades)
    UB = np.ones(qtdvariedades)
    limites = Bounds(LB, UB)

    # Limites superior e inferior de cada variedade
    for i in range(len(objeto_otimizacao.parametros)):

        if objeto_otimizacao.parametros[i].nome == 'pH':
            ph = Parametro('pH') 
            ph.limiteInf = objeto_otimizacao.parametros[i].limiteInf
            ph.limiteSup = objeto_otimizacao.parametros[i].limiteSup

        if objeto_otimizacao.parametros[i].nome == 'Pol':
            pol = Parametro('Pol') 
            pol.limiteInf = objeto_otimizacao.parametros[i].limiteInf
            pol.limiteSup = objeto_otimizacao.parametros[i].limiteSup

        if objeto_otimizacao.parametros[i].nome == 'Pureza':
            pureza = Parametro('Pureza') 
            pureza.limiteInf = objeto_otimizacao.parametros[i].limiteInf
            pureza.limiteSup = objeto_otimizacao.parametros[i].limiteSup
            
        if objeto_otimizacao.parametros[i].nome == 'ATR':
            atr = Parametro('ATR') 
            atr.limiteInf = objeto_otimizacao.parametros[i].limiteInf
            atr.limiteSup = objeto_otimizacao.parametros[i].limiteSup 

        if objeto_otimizacao.parametros[i].nome == 'AR':
            ar = Parametro('AR') 
            ar.limiteInf = objeto_otimizacao.parametros[i].limiteInf
            ar.limiteSup = objeto_otimizacao.parametros[i].limiteSup   

        if objeto_otimizacao.parametros[i].nome == 'Fibra':
            fibra = Parametro('Fibra') 
            fibra.limiteInf = objeto_otimizacao.parametros[i].limiteInf
            fibra.limiteSup = objeto_otimizacao.parametros[i].limiteSup

    # Definição da função Objetivo - CUSTO (minimizar)
    def custo(x):
        custo = [(objeto_otimizacao.variedades[i].custo*x[i]) for i in range(qtdvariedades)]
        return sum(custo)

    #restrição pH limite inferior
    def ph1(x):
        ph1 = [(objeto_otimizacao.variedades[i].ph*x[i]) for i in range(qtdvariedades)]
        return sum(ph1) - ph.limiteInf

    #restrição pH limite superior
    def ph2(x):
        ph2 = [(objeto_otimizacao.variedades[i].ph*x[i]) for i in range(qtdvariedades)]
        return ph.limiteSup - sum(ph2)

    #restrição pol limite inferior
    def pol1(x):
        pol1 = [(objeto_otimizacao.variedades[i].pol*x[i]) for i in range(qtdvariedades)]
        return sum(pol1) - pol.limiteInf

    #restrição pol limite superior
    def pol2(x):
        pol2 = [(objeto_otimizacao.variedades[i].pol*x[i]) for i in range(qtdvariedades)]
        return pol.limiteSup - sum(pol2)

    #restrição pureza limite inferior
    def pureza1(x):
        pureza1 = [(objeto_otimizacao.variedades[i].pureza*x[i]) for i in range(qtdvariedades)]
        return sum(pureza1) - pureza.limiteInf

    #restrição pureza limite superior
    def pureza2(x):
        pureza2 = [(objeto_otimizacao.variedades[i].pureza*x[i]) for i in range(qtdvariedades)]
        return pureza.limiteSup - sum(pureza2)

    #restrição atr limite inferior
    def atr1(x):
        atr1 = [(objeto_otimizacao.variedades[i].atr*x[i]) for i in range(qtdvariedades)]
        return sum(atr1) - atr.limiteInf

    #restrição atr limite superior
    def atr2(x):
        atr2 = [(objeto_otimizacao.variedades[i].atr*x[i]) for i in range(qtdvariedades)]
        return atr.limiteSup - sum(atr2)

    #restrição ar limite inferior
    def ar1(x):
        ar1 = [(objeto_otimizacao.variedades[i].ar*x[i]) for i in range(qtdvariedades)]
        return sum(ar1) - ar.limiteInf

    #restrição atr limite superior
    def ar2(x):
        ar2 = [(objeto_otimizacao.variedades[i].ar*x[i]) for i in range(qtdvariedades)]
        return ar.limiteSup - sum(ar2)

    #restrição fibra limite inferior
    def fibra1(x):
        fibra1 = [(objeto_otimizacao.variedades[i].fibra*x[i]) for i in range(qtdvariedades)]
        return sum(fibra1) - fibra.limiteInf

    #restrição fibra limite superior
    def fibra2(x):
        fibra2 = [(objeto_otimizacao.variedades[i].fibra*x[i]) for i in range(qtdvariedades)]
        return fibra.limiteSup - sum(fibra2)

    def composicao(x):
        return sum(x) - 1

    #Criação das funções de restrição
    ph1 = {'type': 'ineq', 'fun': ph1}
    ph2 = {'type': 'ineq', 'fun': ph2}
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

    #Pegando os parâmetros escolhidos pelo usuário
    restricoes = []

    for i in range(len(objeto_otimizacao.parametros)):

        if objeto_otimizacao.parametros[i].nome == 'pH':
            restricoes.append(ph1)
            restricoes.append(ph2)

        if objeto_otimizacao.parametros[i].nome == 'Pol':
            restricoes.append(pol1)
            restricoes.append(pol2)

        if objeto_otimizacao.parametros[i].nome == 'Pureza':
            restricoes.append(pureza1)
            restricoes.append(pureza2)

        if objeto_otimizacao.parametros[i].nome == 'ATR':
            restricoes.append(atr1)
            restricoes.append(atr2)

        if objeto_otimizacao.parametros[i].nome == 'AR':
            restricoes.append(ar1)
            restricoes.append(ar2)

        if objeto_otimizacao.parametros[i].nome == 'Fibra':
            restricoes.append(fibra1)
            restricoes.append(fibra2)

    restricoes.append(composicao)

    #função de otimização
    solucao = minimize(custo, x0, method='SLSQP', bounds=limites, constraints=restricoes)

    #Calculando o resultado
    xf = solucao.x

    custo = sum([(objeto_otimizacao.variedades[i].custo*xf[i]) for i in range(qtdvariedades)])
    ph = sum([(objeto_otimizacao.variedades[i].ph*xf[i]) for i in range(qtdvariedades)])
    pol = sum([(objeto_otimizacao.variedades[i].pol*xf[i]) for i in range(qtdvariedades)])
    pureza = sum([(objeto_otimizacao.variedades[i].pureza*xf[i]) for i in range(qtdvariedades)])
    atr = sum([(objeto_otimizacao.variedades[i].atr*xf[i]) for i in range(qtdvariedades)])
    ar = sum([(objeto_otimizacao.variedades[i].ar*xf[i]) for i in range(qtdvariedades)])
    fibra = sum([(objeto_otimizacao.variedades[i].fibra*xf[i]) for i in range(qtdvariedades)])

    resultado = {'x': xf,
                 'Custo': custo,
                 'pH': ph,
                 'Pol': pol,
                 'Pureza': pureza,
                 'ATR': atr,
                 'AR': ar,
                 'Fibra': fibra,
                 'success': solucao.success}
                 
    return resultado