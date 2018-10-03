import numpy as np
import pandas as pd

class PL:
    
    #Atributos da classe
    def __init__ (self, n, m, o):        
        self.__n = n #Qnt de variáveis
        self.__m = m #Qnt de restrições
        self.__o = o #Qnt de variáveis originais
        self.__c = np.zeros(n) #Vetor custo
        self.__cb = np.zeros(m) #Vetor de custo básico
        self.__cn = np.zeros(n-m) #Vetor de custo não básico
        self.__A = np.zeros((m, n)) #Matriz de coeficientes
        self.__b = np.zeros(m) #Vetor de restrições
        self.__I = np.eye(m) #Matriz identidade caracteristica da base B
        self.__C = 0 
        self.__B = np.zeros((m, m)) #Base B
        self.__vb = np.zeros(n) #Vetor de variáveis básicas
        self.__vn = np.arange(1, n+1) #Vetor de variáveis não básicas
        self.__r = np.zeros(n-m) #Vetor de custos reduzidos
        self.__E = np.zeros(m) #Vetor de tamanho de passo
        self.__leitura()
    
    #Método para ler as matrizes do problema
    def __leitura(self):
        print('Digite os elementos do vetor c de custos:')
        for i in range(self.__n):
            self.__c[i] = float(input(f'c{i+1}: '))
        print('\n')

        print('Digite os elementos da matriz A de coeficientes das restrições:')
        for i in range(self.__m):
            for j in range(self.__n):
                self.__A[i, j] = float(input(f'a{i+1}{j+1}: '))
            print("\n")

        print('Digite os elementos do vetor b das restrições:')
        for i in range(self.__m):
            self.__b[i] = float(input(f'b{i+1}: '))
        print('\n')
        
        self.imprimeA()
        self.imprimeb()
        self.imprimec()
        print('\n')
        self.__carac()
    
    #Métodos que mostram as matrizes do problema em forma de dataframe.
    def imprimeA(self):
        dfA = pd.DataFrame(self.__A, columns=['A'+ str(i) for i in range(1,self.__n+1)], index=['Restrição '+ str(i) for i in range(1,self.__m+1)])
        return dfA
  
    def imprimeb(self):
        dfb = pd.DataFrame(np.transpose(self.__b),columns=None, index=['Restrição '+ str(i) for i in range(1,self.__m+1)])
        return dfb

    def imprimec(self):
        dfc = pd.DataFrame(np.transpose(self.__c), index=['c'+ str(i) for i in range(1,self.__n+1)])
        return dfc
    
    #Método para caracterizar se o problema precisa de duas fases/BigM ou ja esta pronto para o simplex.
    def __carac(self):
        for i in range(self.__m):
            for j in range(self.__o, self.__n):
                if (self.__I[:,i] == self.__A[:,j]).all():                
                    self.__C += 1
                    self.__vb[j] = j + 1
                    for k in range(self.__m):
                        self.__B[k, i] = self.__A[k, j]
        self.__vn = self.__vn - self.__vb
                        
        if self.__C == self.__m:
            print(f'O seu PPL já possui uma base B (igual a identidade {self.__m}x{self.__m}) factível.')
            print('Partição Básica: B = {}'.format(self.__B))
            print('\n')
            print('Vetor Básico: Vb =  {}'.format(self.__vb))
            print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
            self.__vn = np.array([l for l in self.__vn if l != 0])
            self.__vb = np.array([l for l in self.__vb if l != 0])
            for i in range(self.__m):
                self.__cb[i] = self.__c[int(self.__vb[i])-1]
            for i in range(self.__n - self.__m):
                self.__cn[i] = self.__c[int(self.__vn[i])-1]
            #print(self.cb)
            #print(self.cn)
            #print('\n')
            self.__Simplex()
        else:
            print(f'O seu PPL não possui uma base B igual a identidade {self.__m}x{self.__m}) factível.')
            print('Portanto é necessário usar o método BigM')
            print('Partição Básica: B = {}'.format(self.__B))
            print('Vetor Básico: Vb =  {}'.format(self.__vb))
            print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
            print('\n')
            self.__BigM()
                
    #Método do método Simplex.        
    def __Simplex(self):
        print('\n')              
        k = 1
        while k <= np.exp(self.__m): 
            print(f'Iteração: {k}')
            
            xb = np.linalg.solve(self.__B, self.__b)
            print('Solução Básica Factível: Xb = {}'.format(xb))
            z = np.inner(self.__cb, xb)
            print('Valor da Função Objetivo: F(x) = {}'.format(z))
            lb = np.linalg.solve(self.__B.transpose(), self.__cb)
            print('Valor do Multplicador Simplex: Lb = {}'.format(lb))

            #r = np.ones(self.n)

            for i in range(self.__o):
                self.__r[i] = self.__c[int(self.__vn[i])-1] - np.dot(lb, self.__A[:, int(self.__vn[i])-1])

            #r = np.array([l for l in r if l != 0])

            print(f'r = {self.__r}')

            if (np.min(self.__r) >= 0):
                print('A solução para o problema foi encontrada!\n')
                
                if(np.min(self.__r) > 0):
                    for i in range(self.__m):
                        if (xb[i] == 0 and self.__vb[i] > self.__o) :
                            print(f'A solução é DEGENERADA')
                            print('Solução Básica Factível: Xb = {}'.format(xb))
                            print('Vetor Básico: Vb =  {}'.format(self.__vb))
                            print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
                            print('Valor da Função Objetivo: F(x) = {}'.format(z))
                            break
                    print('Solução Básica Factível: Xb = {}'.format(xb))
                    print('Vetor Básico: Vb =  {}'.format(self.__vb))
                    print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
                    print('Valor da Função Objetivo: F(x) = {}'.format(z))
                    break                            
                    if (xb != 0).all():
                        print('Solução Básica Factível: Xb = {}'.format(xb))
                        print('Vetor Básico: Vb =  {}'.format(self.__vb))
                        print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
                        print('Valor da Função Objetivo: F(x) = {}'.format(z))
                        break
                else:
                    
                    a = self.__vn[np.argmin(self.__r)]
                    print('Vetor que entra na Base: x{}'.format(int(a)))
                    a = int(a)
                    d = np.linalg.solve(self.__B, self.__A[:, a-1])
                    print('Direção Simplex: d = {}'.format(d))
                    if (d <= 0).all():
                        print("A solução é ilimitada!")
                        print('Solução Básica Factível: Xb = {}'.format(xb))
                        print('Vetor Básico: Vb =  {}'.format(self.__vb))
                        print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
                        print('Valor da Função Objetivo: F(x) = {}'.format(z))
                        break
                    print("Há infinitas soluções limitadas")
                    print('Solução Básica Factível: Xb = {}'.format(xb))
                    print('Vetor Básico: Vb =  {}'.format(self.__vb))
                    print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
                    print('Valor da Função Objetivo: F(x) = {}'.format(z))
                    break
                    
                
            else:
                a = self.__vn[np.argmin(self.__r)]
                print('Vetor que entra na Base: x{}'.format(int(a)))

            a = int(a)
            d = np.linalg.solve(self.__B, self.__A[:, a-1])
            print('Direção Simplex: d = {}'.format(d))
            
            if (d <= 0).all():
                print("A solução é ilimitada!")
                print('Solução Básica Factível: Xb = {}'.format(xb))
                print('Vetor Básico: Vb =  {}'.format(self.__vb))
                print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
                print('Valor da Função Objetivo: F(x) = {}'.format(z))
                break
                
            E = np.zeros(self.__m)
            for i in range(self.__m):
                if d[i] > 0:
                    E[i] = (xb[i]/d[i])
                else:
                    E[i] = np.exp(np.max(xb))

            #E = np.array([l for l in E if l != 0])

            b = self.__vb[np.argmin(E)]

            print('Tamanho do Passo Simplex: Ê = {}'.format(E))
            print('Vetor que sai da Base: x{}'.format(int(b)))

            for i in range(self.__m):
                if self.__vb[i] == b:
                    self.__vb[i] = a
            for i in range(self.__o):
                if self.__vn[i] == a:
                    self.__vn[i] = b

            for i in range(self.__m):
                self.__cb[i] = self.__c[int(self.__vb[i])-1]
            for i in range(self.__o):
                self.__cn[i] = self.__c[int(self.__vn[i])-1]

            print('Vetor Básico: Vb =  {}'.format(self.__vb))
            print('Custo Básico: Cb = {}'.format(self.__cb))
            print('Vetor Não-Básico: Vn = {}'.format(self.__vn))
            print('Custo Não-Básico: Cn = {}'.format(self.__cn))

            for j in range(self.__m):
                for i in range(self.__m):
                    self.__B[i, j] = self.__A[i, int(self.__vb[j])-1]

            print('Partição Básica: B = {}'.format(self.__B))
            print('\n')
            k += 1
            
    #Método do método BigM, basicamente ele reformula o problema para os moldes do BigM e chama o método Simplex em seguida.  
    def __BigM(self):
        
        W = self.__I - self.__B
        self.__B = np.append(self.__B, W, axis=1)
        W = np.transpose(np.array([W[:,l] for l in range(self.__m) if (W[:, l] != np.zeros((self.__m,1))).any()]))
        self.__B = np.transpose(np.array([self.__B[:,l] for l in range(self.__n) if (self.__B[:, l] != np.zeros((self.__m,1))).any()]))
        self.__A = np.append(self.__A, W, axis=1)
        self.__vb = np.append(self.__vb, np.arange(self.__n + 1, self.__n + self.__m - self.__C + 1))
        self.__vn = np.append(self.__vn, np.zeros((1, self.__m - self.__C)))
        
        M = np.exp(np.max(self.__c))
        
        self.__c = np.append(self.__c, np.zeros((1, self.__m - self.__C)))
        for i in range(self.__n + self.__m - self.__C):
            if i >= self.__n:
                self.__c[i] = M
        self.__vb = np.array([l for l in self.__vb if l != 0])
        for i in range(self.__m):
            self.__cb[i] = self.__c[int(self.__vb[i])-1]
        self.__cn = np.append(self.__cn, np.zeros((1, self.__m - self.__C)))
        self.__vn = np.array([l for l in self.__vn if l != 0])
        for i in range(self.__n - self.__C):
            self.__cn[i] = self.__c[int(self.__vn[i])-1]
        self.__r = np.append(self.__r, np.zeros((1, self.__m - self.__C)))
        self.__o = self.__n - self.__C
        
        self.__Simplex()
        
        if np.max(self.__vb) >= self.__n + 1:
            print('O problema é INFACTÍVEL!')        
            
        
