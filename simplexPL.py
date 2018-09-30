import numpy as np
import pandas as pd

class PL:
    
    #Atributos da classe
    def __init__ (self, n, m):        
        self.n = n #Qnt de variáveis
        self.m = m #Qnt de restrições
        self.c = np.zeros(n) #Vetor custo
        self.A = np.zeros((m, n)) #Matriz de coeficientes
        self.b = np.zeros(m) #Vetor de restrições
        self.I = np.eye(m) #Matriz identidade caracteristica da base B
        self.C = 0 
        self.B = np.zeros((m, m)) #Base B
        self.vb = np.zeros(n) #Vetor de variáveis básicas
        self.vn = np.arange(1, n+1) #Vetor de variáveis não básicas
        self.leitura()
    
    #Método para ler as matrizes do problema
    def leitura(self):
        print('Digite os elementos do vetor b de custos:')
        for i in range(self.n):
            self.c[i] = float(input(f'c{i}: '))
        print('\n')

        print('Digite os elementos da matriz A de coeficientes das restrições:')
        for i in range(self.m):
            for j in range(self.n):
                self.A[i, j] = float(input(f'a{i+1}{j+1}: '))
            print("\n")

        print('Digite os elementos do vetor b das restrições:')
        for i in range(self.m):
            self.b[i] = float(input(f'b{i}: '))
        print('\n')
        
        self.__carac()
    
    #Métodos que mostram as matrizes do problema em forma de dataframe. Melhorar a visualização.
    def imprimeA(self):
        dfA = pd.DataFrame(self.A)
        print(dfA)
    
    def imprimeb(self):
        dfb = pd.DataFrame(self.b)
        print(dfb)

    def imprimec(self):
        dfc = pd.DataFrame(self.c)
        print(dfc)
    
    #Método para caracterizar se o problema precisa de duas fases/BigM ou ja esta pronto para o simplex.
    def __carac(self):
        for i in range(self.m):
            for j in range((self.m-1), self.n):
                if (self.I[:,i] == self.A[:,j]).all():                
                    self.C += 1
                    self.vb[j] = j + 1
                    for k in range(self.m):
                        self.B[k, i] = self.A[k, j]
        self.vn = self.vn - self.vb
                        
        if self.C == self.m:
            print(f'O seu PPL já possui uma base B (igual a identidade {self.m}x{self.m}) factível.')
            print(self.B)
            print('\n')
            print(self.vb)
            print(self.vn)
            self.vn = np.array([l for l in self.vn if l != 0])
            self.vb = np.array([l for l in self.vb if l != 0])
        else:
            print(f'O seu PPL não possui uma base B (igual a identidade {self.m}x{self.m}) factível.')
            resp = str(input('Gostaria de usar o método de duas fases[f] ou o BigM[M]? '))
            print(resp)
            print(self.B)
            print('\n')
            print(self.vb)
            print(self.vn)
            
    #def __Simplex(self):
        
    '''
    def __DuasFases(self):

    def __BigM(self):
    '''

            
            
        