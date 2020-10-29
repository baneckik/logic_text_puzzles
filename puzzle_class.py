import numpy as np
import pandas as pd

# ------------------ class methods ----------------------------

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
        raise(Exception("Wrong value format! value must be either one of {0,1,2} or {-,O,X}"))
    
    if self.grid[str(min(K1, K2))+","+str(max(K1, K2))][j1, j2] != val2:
        self.changed = True
    self.grid[str(min(K1, K2))+","+str(max(K1, K2))][j1, j2] = val2

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
        
def clear_grid(self):
    for key in self.grid:
        self.grid[key] = np.zeros((self.k, self.k))
            
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
        return self.grid[str(min(K1, K2))+","+str(max(K1, K2))][j1, j2]

def is_line_completed(self, K1, i, K2):
    if K1<0 or K1>=self.K or K2<0 or K2>=self.K:
        raise(Exception("Wrong cathegory id!"))
    if i<0 or i>=self.k:
        raise(Exception("Wrong row/column id!"))
        
    box = self.grid[str(min(K1,K2))+","+str(max(K1,K2))]
    x_count = 0
    o_count = 0
    if K1<K2:
        for j in range(self.k):
            if box[i, j]==1:
                o_count += 1
            elif box[i, j]==2:
                x_count += 1
    else:
        for j in range(self.k):
            if box[j, i]==1:
                o_count += 1
            elif box[j, i]==2:
                x_count += 1
    return x_count==self.k-1 and o_count==1        
      
def count_x_in_line(self, K1, i, K2):
    if K1<0 or K1>=self.K or K2<0 or K2>=self.K:
        raise(Exception("Wrong cathegory id!"))
    if i<0 or i>=self.k:
        raise(Exception("Wrong row/column id!"))
        
    box = self.grid[str(min(K1,K2))+","+str(max(K1,K2))]
    x_count = 0
    if K1<K2:
        for j in range(self.k):
            if box[i, j]==2:
                x_count += 1
    else:
        for j in range(self.k):
            if box[j, i]==2:
                x_count += 1
    return x_count 
    
def grid_concile1(self):
    # conciliation no 1
    K = self.K
    k = self.k
    for key in self.grid:
        K1 = int(key.split(",")[0])
        K2 = int(key.split(",")[1])
        for i in range(k):
            for j in range(k):
                if self.grid[key][i,j]==1:
                    for l in range(k):
                        if l!=i:
                            self.grid_insert(K1, l, K2, j, "X")
                        if l!=j:
                            self.grid_insert(K1, i, K2, l, "X")

def grid_concile2(self):                
    # conciliation no 2
    for key in self.grid:
        K1 = int(key.split(",")[0])
        K2 = int(key.split(",")[1])
        for i in range(self.k):
            if self.count_x_in_line(K1,i,K2)==self.k-1 and not self.is_line_completed(K1, i, K2):
                for j in range(self.k):
                    if self.get_grid_value(K1,i,K2,j)==0:
                        self.grid_insert(K1, i, K2, j, "O")
                        for i2 in range(self.k):
                            if i2!=i:
                                self.grid_insert(K1, i2, K2, j, "X")
                        break
                
            if self.count_x_in_line(K2,i,K1)==self.k-1 and not self.is_line_completed(K2, i, K1):
                for j in range(self.k):
                    if self.get_grid_value(K2, i, K1, j)==0:
                        self.grid_insert(K2, i, K1, j, "O")
                        for i2 in range(self.k):
                            if i2!=i:
                                self.grid_insert(K2, i2, K1, j, "X")
                        break

def grid_concile3(self):
    # conciliation no 3
    K = self.K
    k = self.k
    for key in self.grid:
        K1 = int(key.split(",")[0])
        K2 = int(key.split(",")[1])
        for i in range(k):
            for j in range(k):
                if self.grid[key][i,j]==1:
                    for K3 in range(K):
                        if K3!=K2 and K3!=K1:
                            for j2 in range(k):
                                if self.get_grid_value(K1, i, K3, j2)==2:
                                    self.grid_insert(K2, j, K3, j2, "X")
                                if self.get_grid_value(K2, j, K3, j2)==2:
                                    self.grid_insert(K1, i, K3, j2, "X")
    
def grid_concile4(self):
    # conciliation no 4
    K = self.K
    k = self.k
    for K1 in range(K):
        for K2 in range(K):
            if K2!=K1:
                for K3 in range(K2+1, K):
                    if K3!=K1:
                        for j2 in range(k):
                            for j3 in range(k):
                                contradictory_lines = True
                                for i in range(k):
                                    val1 = self.get_grid_value(K1, i, K2, j2)
                                    val2 = self.get_grid_value(K1, i, K3, j3)
                                    if val1!=2 and val2!=2:
                                        contradictory_lines = False
                                        break
                                if contradictory_lines:
                                    self.grid_insert(K2, j2, K3, j3, "X")

def grid_concile5(self):
    # conciliation no 4
    K = self.K
    k = self.k
    if k<4:
        return
        
    for K1 in range(K):
        for K2 in range(K):
            if K1!=K2:
                # double lines to concile
                for i1 in range(k):
                    for i2 in range(i1+1, k):
                        common_empty = []
                        concile = True
                        for j in range(k):
                            val1 = self.get_grid_value(K1, i1, K2, j)
                            val2 = self.get_grid_value(K1, i2, K2, j)
                            if val1!=val2 or val1==1 or val2==1:
                                concile = False
                                break
                            if val1==0 and val1==val2:
                                common_empty.append(j)
                        if concile and len(common_empty)==2:
                            for j in common_empty:
                                for i3 in range(k):
                                    if i3!=i1 and i3!=i2:
                                        self.grid_insert(K1, i3, K2, j, "X")
                # triple lines to concile
                if k>5:
                    for i1 in range(k):
                        for i2 in range(i1+1, k):
                            for i3 in range(i2+1, k):
                                common_empty = []
                                concile = True
                                for j in range(k):
                                    val1 = self.get_grid_value(K1, i1, K2, j)
                                    val2 = self.get_grid_value(K1, i2, K2, j)
                                    val3 = self.get_grid_value(K1, i3, K2, j)
                                    if val1!=val2 or val3!=val2 or val1==1 or val2==1 or val3==1:
                                        concile = False
                                        break
                                    if val1==0 and val1==val2 and val2==val3:
                                        common_empty.append(j)
                                if concile and len(common_empty)==3:
                                    for j in common_empty:
                                        for i4 in range(k):
                                            if i4!=i1 and i4!=i2 and i4!=i3:
                                                self.grid_insert(K1, i4, K2, j, "X")

        
# --------------------- class definition ------------------------------
    
class puzzle:
    def __init__(self, K, k):
        self.K = K
        self.k = k
        self.grid = { str(i)+","+str(j): np.zeros((k,k)) for i in range(K) for j in range(K) if i<j }
        self.changed = False
        self.solved = False
        
    get_grid_value = get_grid_value
    grid_insert = grid_insert
    print_grid = print_grid
    clear_grid = clear_grid
    
    is_line_completed = is_line_completed
    count_x_in_line = count_x_in_line
    grid_concile1 = grid_concile1
    grid_concile2 = grid_concile2
    grid_concile3 = grid_concile3
    grid_concile4 = grid_concile4
    grid_concile5 = grid_concile5
    