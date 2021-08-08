import sqlite3
import os
import pandas as pd
from ParametrosOtimizacao import Otimizacao, Parametro
from Variedade import Variedade


class Database:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connectdb(self):
        if os.path.isfile('Otimizacao.db'):
            self.conn = sqlite3.connect('Otimizacao.db')
            self.cursor = self.conn.cursor()
        else:
            self.conn = sqlite3.connect('Otimizacao.db')
            self.cursor = self.conn.cursor()
            self.createsimulacao()
            self.createvariedade()
            self.createparametro()
            self.inserirvariedades()
            self.inserirparametros()
            self.createvariedadesimulacao()
            self.createparametrosimulacao()

            self.conn.commit()

    def createsimulacao(self):

        print(f'Criando tabela de simulações')
        self.cursor.execute("""
        CREATE TABLE Simulacao (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Data INTEGER NOT NULL,
            Sucesso TEXT NOT NULL 
            );     
        """)

    def createvariedade(self):

        print(f'Criando tabela de variedades')
        self.cursor.execute("""
        CREATE TABLE Variedade (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Custo REAL NOT NULL,
            pH REAL NOT NULL,
            Pol REAL NOT NULL,
            Pureza REAL NOT NULL,
            ATR REAL NOT NULL,
            AR REAL NOT NULL,
            Fibra REAL NOT NULL
            );
        """)

    def inserirvariedades(self):

        print(f'Inserindo Variedades')
        self.cursor.execute("""
        INSERT INTO Variedade (Nome, Custo, pH, Pol, Pureza, ATR, AR, Fibra) 
        VALUES ('Var1', 3, 5, 13, 0.8, 0.15, 0.007, 0.1120) """)

        self.cursor.execute("""
        INSERT INTO Variedade (Nome, Custo, pH, Pol, Pureza, ATR, AR, Fibra) 
        VALUES ('Var2', 2.4, 5.4, 20, 0.75, 0.2, 0.0075, 0.1250) """)

        self.cursor.execute("""
        INSERT INTO Variedade (Nome, Custo, pH, Pol, Pureza, ATR, AR, Fibra) 
        VALUES ('Var3', 2.8, 5.8, 21, 0.9, 0.11, 0.006, 0.1146) """)

        self.cursor.execute("""
        INSERT INTO Variedade (Nome, Custo, pH, Pol, Pureza, ATR, AR, Fibra) 
        VALUES ('Var4', 3.1, 7, 19, 0.7, 0.25, 0.0077, 0.1289) """)

        self.cursor.execute("""
        INSERT INTO Variedade (Nome, Custo, pH, Pol, Pureza, ATR, AR, Fibra) 
        VALUES ('Var5', 2.5, 8, 16, 0.82, 0.16, 0.0059, 0.1201) """)

        self.cursor.execute("""
        INSERT INTO Variedade (Nome, Custo, pH, Pol, Pureza, ATR, AR, Fibra) 
        VALUES ('Var6', 3.2, 4.3, 15, 0.86, 0.18, 0.0064, 0.1178) """)

    def createparametro(self):

        print(f'Criando tabela de parâemetro')
        self.cursor.execute("""
        CREATE TABLE Parametro (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            LimiteInf REAL NOT NULL,
            LimiteSup REAL NOT NULL
            );
            """)

    def inserirparametros(self):

        print(f'Inserindo parâmetros')
        self.cursor.execute("""
        INSERT INTO Parametro (Nome, LimiteInf, LimiteSup) 
        VALUES ('pH', 4, 6) """)

        self.cursor.execute("""
        INSERT INTO Parametro (Nome, LimiteInf, LimiteSup) 
        VALUES ('Pol', 14, 100) """)

        self.cursor.execute("""
        INSERT INTO Parametro (Nome, LimiteInf, LimiteSup) 
        VALUES ('Pureza', 0.85, 1) """)

        self.cursor.execute("""
        INSERT INTO Parametro (Nome, LimiteInf, LimiteSup) 
        VALUES ('ATR', 0.15, 1) """)

        self.cursor.execute("""
        INSERT INTO Parametro (Nome, LimiteInf, LimiteSup) 
        VALUES ('AR', 0, 0.0008) """)

        self.cursor.execute("""
        INSERT INTO Parametro (Nome, LimiteInf, LimiteSup) 
        VALUES ('Fibra', 0.11, 0.13) """)

    def createvariedadesimulacao(self):

        self.cursor.execute("""
        CREATE TABLE Variedadesimulacao (
            idsimulacao INTEGER NOT NULL,
            idvariedade INTEGER NOT NULL,
            PRIMARY KEY (idsimulacao, idvariedade)
            );     
        """)

    def createparametrosimulacao(self):

        self.cursor.execute("""
        CREATE TABLE Parametrosimulacao (
            idsimulacao INTEGER NOT NULL,
            idparametro INTEGER NOT NULL,
            limitesup REAL NOT NULL,
            limiteinf REAL NOT NULL,
            PRIMARY KEY (idsimulacao, idparametro)
            );     
        """)

    def leituraparametros(self):
        sql = "SELECT Nome FROM Parametro ORDER BY id"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        parametros = []

        for row in rows:
            parametros.append(row[0])

        return parametros

    def leituravariedades(self):
        dataframe = pd.read_sql_query("SELECT * FROM Variedade", self.conn)
        del dataframe['id']
        return dataframe

    def leiturahistorico(self):
        dataframe = pd.read_sql_query("SELECT * FROM Simulacao", self.conn)
        return dataframe

    def salvarsimulacacao(self, objotimizacao):
        self.connectdb()
        sql = """INSERT INTO Simulacao (Nome, Data, Sucesso) VALUES (?, datetime('now', 'localtime'), ?)"""

        if objotimizacao.resultado['success'] == True:
            sucesso = 'Sucesso'
        else:
            sucesso = 'Falha'
        self.cursor.execute(sql,[objotimizacao.nome, sucesso])

        idsimulacao = self.cursor.lastrowid

        # Insert de parametros
        sql = """INSERT INTO Parametrosimulacao (Idsimulacao, Idparametro, limitesup, limiteinf) VALUES (?, ?, ?, ?)"""
        for i in range(len(objotimizacao.parametros)):
            idparametro = self.getidparametro(objotimizacao.parametros[i].nome)
            self.cursor.execute(sql, [idsimulacao, idparametro, objotimizacao.parametros[i].limiteSup,
                                      objotimizacao.parametros[i].limiteInf])

        sql = """INSERT INTO Variedadesimulacao (Idsimulacao, Idvariedade) VALUES (?, ?)"""
        for i in range(len(objotimizacao.variedades)):
            idvariedade = self.getidvariedade(objotimizacao.variedades[i].nome)
            self.cursor.execute(sql, [idsimulacao, idvariedade])

        self.conn.commit()
        self.conn.close()

    def getidparametro(self, nome):
        sql = """SELECT id FROM PARAMETRO WHERE NOME = ?"""
        self.cursor.execute(sql, [nome])
        row = self.cursor.fetchone()
        id = row[0]
        return id

    def getidvariedade(self, nome):
        sql = """SELECT id FROM VARIEDADE WHERE NOME = ?"""
        self.cursor.execute(sql, [nome])
        return self.cursor.fetchone()[0]

    def leiturasimulacao(self, idsimulacao):
        sql = """SELECT * FROM Simulacao s WHERE s.id = ? """
        self.cursor.execute(sql, [idsimulacao])
        row = self.cursor.fetchone()
        simulacao = Otimizacao()
        simulacao.nome = row[1]
        simulacao.time = row[2]
        simulacao.sucesso = row[3]
        simulacao.historico = True
        simulacao.resultado = None
        simulacao.qtdvariedades = 0
        simulacao.variedades = self.leituravariedadessimulacao(idsimulacao)
        simulacao.parametros = self.leituraparametrossimulacao(idsimulacao)

        return simulacao

    def leituravariedadessimulacao(self, idsimulacao):
        sql = """SELECT v.nome, v.custo, v.ph, v.pol, v.pureza, v.atr, v.ar, v.fibra  
                  FROM Variedade v, 
                       Variedadesimulacao vs 
                 WHERE v.id = vs.idvariedade 
                   and vs.idsimulacao = ?"""
        self.cursor.execute(sql, [idsimulacao])
        rows = self.cursor.fetchall()
        variedades = []
        for row in rows:
            V = Variedade(*row)
            variedades.append(V)
        return variedades

    def leituraparametrossimulacao(self, idsimulacao):
        sql = """SELECT * 
            FROM Parametro p, 
                 Parametrosimulacao ps 
           WHERE p.id = ps.idparametro 
             and ps.idsimulacao = ?"""
        self.cursor.execute(sql, [idsimulacao])
        rows = self.cursor.fetchall()
        parametros = []
        for row in rows:
            P = Parametro(row[1])
            P.setlimites(row[2], row[3])
            parametros.append(P)
        return parametros


if __name__ == '__main__':
    Database = Database()
    Database.connectdb()
    Otim = Database.leiturasimulacao(3)
    print(Otim.variedades)
