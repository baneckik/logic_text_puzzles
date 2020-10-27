import numpy as np
import pandas as pd

class puzzle:
    def __init__(self, K, k):
        self.K = K
        self.k = k
        self.grid = { str(i)+","+str(j): np.zeros((k,k)) for i in range(K) for j in range(K) if i<j }
    
    def get_grid_value(self, K1, i1, K2, i2):
        if K1>=self.K or K2>=self.K or K1<0 or K2<0 or K1==K2:
            raise(Exception("Cathegory index out of range!"))
        if i1>=self.k or i2>=self.k or i1<0 or i2<0:
            raise(Exception("Word in cathegory index is out of range!"))
        if K1<K2:
            j1 = i1
            j2 = i2
        else:
            j1 = i2
            j2 = i1
        return self.grid[str(min(K1,K2))+","+str(max(K1,K2))][j1, j2]
    
    def grid_insert(self, K1, i1, K2, i2, val):
        if K1>=self.K or K2>=self.K or K1<0 or K2<0 or K1==K2:
            raise(Exception("Cathegory index out of range!"))
        if i1>=self.k or i2>=self.k or i1<0 or i2<0:
            raise(Exception("Word in cathegory index is out of range!"))
        if K1<K2:
            j1 = i1
            j2 = i2
        else:
            j1 = i2
            j2 = i1
        if val==0 or val=="-":
            val2 = 0
        elif val==1 or val=="O":
            val2 = 1
        elif val==2 or val=="X":
            val2 = 2
        else:
            raise(Exception("Wrong value format! value must be one of {0,1,2} or {-,O,X}"))
        self.grid[str(min(K1,K2))+","+str(max(K1,K2))][j1, j2] = val2
    
    def print_grid(self):
        for K_row in range(self.K-1):
            for row in range(self.k):
                line = ""
                for K_col in range(self.K-1-K_row):
                    for col in range(self.k):
                        val = self.get_grid_value(K_row, row, self.K-1-K_col, col)
                        if val==0:
                            line += "-"
                        elif val==1:
                            line += "O"
                        else:
                            line += "X"
                    line += " "
                print(line)
            print()