import numpy as np
import pandas as pd

class PL:
    
    def __init__ (self, n, m):        
        self.n = n
        self.m = m
        self.c = np.zeros(n)
        self.A = np.zeros((m, n))
        self.b = np.zeros(m)
        self.leitura()

    def leitura(self):
        print('Digite os elementos do vetor b de custos:')
        for i in range(self.n):
            self.c[i] = int(input(f'c{i}: '))
        print('\n')

        print('Digite os elementos da matriz A de coeficientes das restrições:')
        for i in range(self.m):
            for j in range(self.n):
                self.A[i][j] = int(input(f'a{i+1}{j+1}: '))
            print("\n")

        print('Digite os elementos do vetor b das restrições:')
        for i in range(self.m):
            self.b[i] = int(input(f'b{i}: '))
        print('\n')
    
    def imprimeA(self):
        dfA = pd.DataFrame(self.A)
        print(dfA)
    
    def imprimeb(self):
        dfb = pd.DataFrame(self.b)
        print(dfb)

    def imprimec(self):
        dfc = pd.DataFrame(self.c)
        print(dfc)
        