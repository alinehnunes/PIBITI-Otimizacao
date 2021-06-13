import matplotlib
import numpy as np
from scipy.optimize import Bounds
from scipy.optimize import minimize

# Pos 0 = Hidratado | Pos 1 = Anidro | Pos 2 = Comercial
x0 = [0.6, 0.2, 0.2]

# Limites para as composições de cada álcool
LB = [0, 0, 0]
UB = [1, 1, 1]
limites = Bounds(LB, UB)

# Definição da função Objetivo
def objective(x):
    return (-1)*(0.5164*x[0] + 0.5356*x[1] + 0.4938*x[2])

def restri1(x):
    return 6.442462*x[0] + 4.817462*x[1] + 4.557462*x[2] - 0.859242*x[0]*x[1] + 6.570758*x[1]*x[2] - 6

def restri2(x):
    return 8 - (6.442462*x[0] + 4.817462*x[1] + 4.557462*x[2] - 0.859242*x[0]*x[1] + 6.570758*x[1]*x[2])
# Definição das restrições
def restri3(x):
    return 0.812263*x[0] + 0.795183*x[1] + 0.791183*x[2] - 0.8076

def restri4(x):
    return 0.811 - (0.812263*x[0] + 0.795183*x[1] + 0.791183*x[2])

def restri5(x):
    return 30 - (29.8658*x[0] + 32.8683*x[1] + 56.8883*x[2] - 26.8405*x[0]*x[1] - 26.8405*x[0]*x[2])

def restri6(x):
    return 92.15857*x[0] + 98.1157*x[1] + 99.45857*x[2] - 92.5

def restri7(x):
    return 93.8 - (92.15857*x[0] + 98.1157*x[1] + 99.45857*x[2])

def restri8(x):
    return x[0] + x[1] + x[2] - 1


rest1 = {'type': 'ineq', 'fun': restri1}
rest2 = {'type': 'ineq', 'fun': restri2}
rest3 = {'type': 'ineq', 'fun': restri3}
rest4 = {'type': 'ineq', 'fun': restri4}
rest5 = {'type': 'ineq', 'fun': restri5}
rest6 = {'type': 'ineq', 'fun': restri6}
rest7 = {'type': 'ineq', 'fun': restri7}
rest8 = {'type': 'eq', 'fun': restri8}

restricoes = [rest1, rest2, rest3, rest4, rest5, rest6, rest7, rest8]

solucao = minimize(objective, x0, method='SLSQP', bounds=limites, constraints=restricoes)
print(solucao)
