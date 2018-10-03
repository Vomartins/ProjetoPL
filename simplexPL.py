import numpy as np
import pandas as pd

class PL:
    
    #Atributos da classe
    def __init__ (self, n, m):        
        self.n = n #Qnt de variáveis
        self.m = m #Qnt de restrições
        self.o = n-m #Qnt de variáveis originais
        self.c = np.zeros(n) #Vetor custo
        self.cb = np.zeros(m) #Vetor de custo básico
        self.cn = np.zeros(n-m) #Vetor de custo não básico
        self.A = np.zeros((m, n)) #Matriz de coeficientes
        self.b = np.zeros(m) #Vetor de restrições
        self.I = np.eye(m) #Matriz identidade caracteristica da base B
        self.C = 0 
        self.B = np.zeros((m, m)) #Base B
        self.vb = np.zeros(n) #Vetor de variáveis básicas
        self.vn = np.arange(1, n+1) #Vetor de variáveis não básicas
        self.r = np.zeros(n-m) #Vetor de custos reduzidos
        self.E = np.zeros(m) #Vetor de tamanho de passo
        self.leitura()
    
    #Método para ler as matrizes do problema
    def leitura(self):
        print('Digite os elementos do vetor c de custos:')
        for i in range(self.n):
            self.c[i] = float(input(f'c{i+1}: '))
        print('\n')

        print('Digite os elementos da matriz A de coeficientes das restrições:')
        for i in range(self.m):
            for j in range(self.n):
                self.A[i, j] = float(input(f'a{i+1}{j+1}: '))
            print("\n")

        print('Digite os elementos do vetor b das restrições:')
        for i in range(self.m):
            self.b[i] = float(input(f'b{i+1}: '))
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
            for j in range(self.o, self.n):
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
            for i in range(self.m):
                self.cb[i] = self.c[int(self.vb[i])-1]
            for i in range(self.n - self.m):
                self.cn[i] = self.c[int(self.vn[i])-1]
            #print(self.cb)
            #print(self.cn)
            #print('\n')
            self.__Simplex()
        else:
            print(f'O seu PPL não possui uma base B (igual a identidade {self.m}x{self.m}) factível.')
            resp = str(input('Gostaria de usar o método de duas fases[f] ou o BigM[M]? '))
            print(resp)
            print(self.B)
            print('\n')
            print(self.vb)
            print(self.vn)
            print('\n')
            if resp == "M":
                self.__BigM()
            
    def __Simplex(self):
                      
        k = 1
        while k <= np.exp(self.m): 
            print(f'Iteração: {k}')
            
            xb = np.linalg.solve(self.B, self.b)
            print(f'xb = {xb}')
            z = np.inner(self.cb, xb)
            print(f'z: {z}')
            lb = np.linalg.solve(self.B.transpose(), self.cb)
            print(f'lb = {lb}')

            #r = np.ones(self.n)

            for i in range(self.o):
                self.r[i] = self.c[int(self.vn[i])-1] - np.dot(lb, self.A[:, int(self.vn[i])-1])

            #r = np.array([l for l in r if l != 0])

            print(f'r = {self.r}')

            if (np.min(self.r) >= 0):
                print('A solução foi encontrada')
                
                if(np.min(self.r) > 0):
                    for i in range(self.m):
                        if (xb[i] == 0 and self.vb[i] > self.o) :
                            print(f'A solução é degenerada.')
                            print(f'xb = {xb}')
                            print(f'vb = {self.vb}')
                            print(f'vn = {self.vn}')
                            print(f'Valor da função objetivo: {z}')
                            break
                    print(f'xb = {xb}')
                    print(f'vb = {self.vb}')
                    print(f'vn = {self.vn}')
                    print(f'Valor da função objetivo: {z}')
                    break                            
                    if (xb != 0).all():
                        print(f'xb = {xb}')
                        print(f'vb = {self.vb}')
                        print(f'vn = {self.vn}')
                        print(f'Valor da função objetivo: {z}')
                        break
                else:
                    print("Há infinitas soluções limitadas")
                    print(f'xb = {xb}')
                    print(f'vb = {self.vb}')
                    print(f'vn = {self.vn}')
                    print(f'Valor da função objetivo: {z}')
                    break
                    
                
            else:
                a = self.vn[np.argmin(self.r)]
                print(f'Variável que entra : {a}')

            a = int(a)
            d = np.linalg.solve(self.B, self.A[:, a-1])
            print(f'direção = {d}')
            
            if (d <= 0).all():
                print("A solução é ilimitada")
                print(f'xb = {xb}')
                print(f'vb = {self.vb}')
                print(f'vn = {self.vn}')
                print(f'Valor da função objetivo: {z}')
                break
                
            E = np.zeros(self.m)
            for i in range(self.m):
                if d[i] > 0:
                    E[i] = (xb[i]/d[i])
                else:
                    E[i] = np.exp(np.max(xb))

            #E = np.array([l for l in E if l != 0])

            b = self.vb[np.argmin(E)]

            print(f'passo = {E}')
            print(f'Variável que sai: {b}')

            for i in range(self.m):
                if self.vb[i] == b:
                    self.vb[i] = a
            for i in range(self.o):
                if self.vn[i] == a:
                    self.vn[i] = b

            for i in range(self.m):
                self.cb[i] = self.c[int(self.vb[i])-1]
            for i in range(self.o):
                self.cn[i] = self.c[int(self.vn[i])-1]

            print(f'vb = {self.vb}')
            print(f'cb = {self.cb}')
            print(f'vn = {self.vn}')
            print(f'cn = {self.cn}')

            for j in range(self.m):
                for i in range(self.m):
                    self.B[i, j] = self.A[i, int(self.vb[j])-1]

            print(f'B = {self.B}')
            print('\n')
            k += 1
      
    def __BigM(self):
        
        W = self.I - self.B
        self.B = np.append(self.B, W, axis=1)
        W = np.transpose(np.array([W[:,l] for l in range(self.m) if (W[:, l] != np.zeros((self.m,1))).any()]))
        self.B = np.transpose(np.array([self.B[:,l] for l in range(self.n) if (self.B[:, l] != np.zeros((self.m,1))).any()]))
        self.A = np.append(self.A, W, axis=1)
        self.vb = np.append(self.vb, np.arange(self.n + 1, self.n + self.m - self.C + 1))
        self.vn = np.append(self.vn, np.zeros((1, self.m - self.C)))
        
        M = np.exp(np.max(self.c))
        
        self.c = np.append(self.c, np.zeros((1, self.m - self.C)))
        for i in range(self.n + self.m - self.C):
            if i >= self.n:
                self.c[i] = M
        self.vb = np.array([l for l in self.vb if l != 0])
        for i in range(self.m):
            self.cb[i] = self.c[int(self.vb[i])-1]
        self.cn = np.append(self.cn, np.zeros((1, self.m - self.C)))
        self.vn = np.array([l for l in self.vn if l != 0])
        for i in range(self.n - self.C):
            self.cn[i] = self.c[int(self.vn[i])-1]
        self.r = np.append(self.r, np.zeros((1, self.m - self.C)))
        self.o = self.n - self.C
        
        self.__Simplex()
        
    '''
    def __DuasFases(self):

    '''

            
            
        