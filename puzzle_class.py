import numpy as np
import pandas as pd
import generating_cathegories_functions as funs

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

def grid_concile(self):
    self.changed = True
    while self.changed == True:
        self.changed = False
        self.grid_concile1()
        self.grid_concile2()
        self.grid_concile3()
        self.grid_concile4()
        self.grid_concile5()
    
                                                
def add_clue1(self):
    no_of_x = np.random.choice([1,2,3], 1, p=[0.8, 0.15, 0.05])
    K = self.K
    k = self.k
    key_list = np.random.choice(range(K*(K-1)//2), K*(K-1)//2, replace=False)
    i_list = np.random.choice(range(k), k, replace=False)
    j_list = np.random.choice(range(k), k, replace=False)
    
    boxes = []
    for key in self.grid:
        boxes.append(key)
        
    for key in key_list:
        K1 = int(boxes[key].split(",")[0])
        K2 = int(boxes[key].split(",")[1])
        for i in i_list:
            for j in j_list:
                if self.get_grid_value(K1, i, K2, j)==0:
                    if no_of_x==1:
                        self.clues.append({"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j})
                        return
                    other_i = []
                    other_j = []
                    for i2 in range(k):
                        if self.get_grid_value(K1, i2, K2, j)==0 and i2!=i:
                            other_i.append(i2)
                    for j2 in range(k):
                        if self.get_grid_value(K1, i, K2, j2)==0 and j2!=j:
                            other_j.append(j2)
                    if len(other_i)<=no_of_x-1 and len(other_j)<=no_of_x-1:
                        self.clues.append({"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j})
                        return
                    elif len(other_i)>no_of_x-1 and len(other_j)>no_of_x-1:
                        if np.random.randint(2)==0:
                            to_fill = np.random.choice(other_i, no_of_x-1, replace=False)
                            if no_of_x==2:
                                self.clues.append({"typ":1, "K1":K2, "i1":j, "K2":K1, "i2":i, "i3":to_fill[0]})
                                return
                            else:
                                self.clues.append({"typ":1, "K1":K2, "i1":j, "K2":K1, "i2":i, "i3":to_fill[0], "i4":to_fill[1]})
                                return
                        else:
                            to_fill = np.random.choice(other_j, no_of_x-1, replace=False)
                            if no_of_x==2:
                                self.clues.append({"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j, "i3":to_fill[0]})
                                return
                            else:
                                self.clues.append({"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j, "i3":to_fill[0], "i4":to_fill[1]})
                                return
                    elif len(other_i)>no_of_x-1:
                        to_fill = np.random.choice(other_i, no_of_x-1, replace=False)
                        if no_of_x==2:
                            self.clues.append({"typ":1, "K1":K2, "i1":j, "K2":K1, "i2":i, "i3":to_fill[0]})
                            return
                        else:
                            self.clues.append({"typ":1, "K1":K2, "i1":j, "K2":K1, "i2":i, "i3":to_fill[0], "i4":to_fill[1]})
                            return
                    else:
                        to_fill = np.random.choice(other_j, no_of_x-1, replace=False)
                        if no_of_x==2:
                            self.clues.append({"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j, "i3":to_fill[0]})
                            return
                        else:
                            self.clues.append({"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j, "i3":to_fill[0], "i4":to_fill[1]})
                            return

def add_clue2(self):
    K = self.K
    k = self.k
    
    K6_candidates = [ i for i, cat in enumerate(self.cathegories) if cat[0] in ['numerical','ordinal'] ]
    K6 = np.random.choice(K6_candidates, 1)[0]
    
    i_candidates = [ i for i in range(K*k) if i//k!=K6 ]
    i1_list = np.random.choice(i_candidates, len(i_candidates), replace=False)
    i2_list = np.random.choice(i_candidates, len(i_candidates), replace=False)
    i3_list = np.random.choice(i_candidates, len(i_candidates), replace=False)
    
    for i1p in i1_list:
        for i2p in i2_list:
            for i3p in i3_list:
                if i1p!=i2p and i1p!=i3p and i2p!=i3p:
                    K1 = i1p//k
                    i1 = i1p%k
                    K2 = i2p//k
                    i2 = i2p%k
                    K3 = i3p//k
                    i3 = i3p%k
                    val0 = self.get_grid_value(K1, i1, K6, 0)
                    val1 = self.get_grid_value(K1, i1, K6, 1)
                    val2 = self.get_grid_value(K2, i2, K6, 0)
                    val3 = self.get_grid_value(K2, i2, K6, k-1)
                    val4 = self.get_grid_value(K3, i3, K6, k-2)
                    val5 = self.get_grid_value(K3, i3, K6, k-1)
                    values = [val0, val1, val2, val3, val4, val5]
                    if any([val==1 for val in values]):
                        break
                    sum_of_free = sum([val==0 for val in values])
                    if sum_of_free>4:
                        self.clues.append({"typ":2, "K1":K1, "i1":i1, "K2":K2, "i2":i2, "K3":K3, "i3":i3, "K6": K6})
                        return
    print("Program couldn't fit any clue of type no 2!")
                
                        
def use_clue1(self, c):
    if len(self.clues)<=c or c<0:
        raise(Exception("Wrong clue id provided!"))
    if self.clues[c]["typ"]!=1:
        raise(Exception("Wrong clue type provided!"))
        
    clue = self.clues[c]
    self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i2"], "X")
    if "i3" in clue:
        self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i3"], "X")
        if "i4" in clue:
              self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i4"], "X")
                
def use_clue2(self, c):
    if len(self.clues)<=c or c<0:
        raise(Exception("Wrong clue id provided!"))
    if self.clues[c]["typ"]!=2:
        raise(Exception("Wrong clue type provided!"))
    
    clue = self.clues[c]
    self.grid_insert(clue["K1"], clue["i1"], clue["K6"], 0, "X")
    self.grid_insert(clue["K1"], clue["i1"], clue["K6"], 1, "X")
    self.grid_insert(clue["K2"], clue["i2"], clue["K6"], 0, "X")
    self.grid_insert(clue["K2"], clue["i2"], clue["K6"], self.k-1, "X")
    self.grid_insert(clue["K3"], clue["i3"], clue["K6"], self.k-2, "X")
    self.grid_insert(clue["K3"], clue["i3"], clue["K6"], self.k-1, "X")
    
    if clue["K1"]!=clue["K2"]:
        self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i2"], "X")
    if clue["K1"]!=clue["K3"]:
        self.grid_insert(clue["K1"], clue["i1"], clue["K3"], clue["i3"], "X")
    if clue["K2"]!=clue["K3"]:
        self.grid_insert(clue["K2"], clue["i2"], clue["K3"], clue["i3"], "X")
    
    for j in range(self.k-2):
        if self.get_grid_value(clue["K3"], clue["i3"], clue["K6"], j)==2:
            self.grid_insert(clue["K1"], clue["i1"], clue["K6"], j+2, "X")
            self.grid_insert(clue["K2"], clue["i2"], clue["K6"], j+1, "X")
        else:
            break
            
def is_grid_contradictory_with_clue2(self, c):
    if len(self.clues)<=c or c<0:
        raise(Exception("Wrong clue id provided!"))
    if self.clues[c]["typ"]!=2:
        raise(Exception("Wrong clue type provided!"))
       
    clue = self.clues[c]
    i1 = None
    i2 = None
    i3 = None
    for j in range(self.k):
        if i3==None and self.get_grid_value(clue["K3"], clue["i3"], clue["K6"], j)!=2:
            i3 = j
        elif i2==None and i3!=None and self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], j)!=2:
            i2 = j
        elif i2!=None and self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], j)!=2:
            i1 = j
            break
    if i1==None:
        return True
    else:
        return False
            
              
def is_grid_completed(self):
    for box in self.grid.values():
        for i in range(self.k):
            for j in range(self.k):
                if box[i, j]==0:
                    return False
    return True                                                   

def is_grid_contradictory(self):
    for box in self.grid.values():
        for i in range(self.k):
            o_count = 0
            x_count = 0
            for j in range(self.k):
                if box[i, j]==1:
                    o_count += 1
                if box[i, j]==2:
                    x_count += 1
            if o_count>1 or x_count==self.k:
                return True
        for j in range(self.k):
            o_count = 0
            x_count = 0
            for i in range(self.k):
                if box[i, j]==1:
                    o_count += 1
                if box[i, j]==2:
                    x_count += 1
            if o_count>1 or x_count==self.k:
                return True
    
    clues2 = [ i for i,clue in enumerate(self.clues) if clue["typ"]==2 ]
    for c in clues2:
        if self.is_grid_contradictory_with_clue2(c):
            print("Puzzle is contradictory with clue 2!")
            return True
    return False

def set_seed(self, seed):
    self.seed = seed
    np.random.seed(self.seed)

def draw_cathegories(self, diff=3):
    if not diff in [2,3,4]:
        raise Exception("Można losować zagadki tylko o liczbie gwiazdek równej 2, 3 albo 4!")
    self.cathegories = funs.losuj_kategorie(self.K, self.k, diff, self.seed)
    i = 0
    i_max = 100
    while funs.do_cathegories_repeat(self.cathegories):
        self.cathegories = funs.losuj_kategorie(self.K, self.k, diff, self.seed)
        i += 1
        if i>i_max:
            raise Exception("Cannot draw non-repeating cathegories!")
            
def try_to_solve(self):
    clues1 = [ i for i,clue in enumerate(self.clues) if clue["typ"]==1 ]
    clues2 = [ i for i,clue in enumerate(self.clues) if clue["typ"]==2 ]
    
    for c in clues1:
        self.use_clue1(c)
    self.grid_concile()
    
    self.changed = True
    while self.changed:
        self.changed = False
        for c in clues2:
            self.use_clue2(c)
            self.grid_concile()
            if self.is_grid_contradictory() or self.is_grid_completed():
                return
        
        
def draw_clues(self):
    no_of_clues2 = 4
    for i in range(no_of_clues2):
        self.add_clue2()
        self.use_clue2(i)
        self.grid_concile()
        self.use_clue2(i)
        if self.is_grid_completed() or self.is_grid_contradictory():
            break
    
    for i in range(100):
        self.add_clue1()
        self.use_clue1(len(self.clues)-1)
        self.grid_concile()
        for j in range(no_of_clues2):
            self.use_clue2(j)
            self.grid_concile()
            if self.is_grid_completed() or self.is_grid_contradictory():
                break

def try_to_restrict_clues(self):
    clues_copy = self.clues
    clues1 = [ i for i, clue in enumerate(clues_copy) if clue["typ"]==1 ]
    clue_order = np.random.choice(clues1, len(clues1), replace=False)
    to_restrict = []
    for i in clue_order:
        clues1_restricted = [ j for j in clues1 if j!=i ]
        self.clear_grid()
        self.clues = [ clue for j, clue in enumerate(clues_copy) if j in clues1_restricted ]
        self.try_to_solve()
        if self.is_grid_completed() and not self.is_grid_contradictory():
            to_restrict.append(i)
            clues1 = clues1_restricted
    print(to_restrict)
    self.clues = [ clue for j, clue in enumerate(clues_copy) if not j in to_restrict ]
    
# --------------------- class definition ------------------------------
    
class puzzle:
    def __init__(self, K, k):
        self.K = K
        self.k = k
        self.grid = { str(i)+","+str(j): np.zeros((k,k)) for i in range(K) for j in range(K) if i<j }
        self.changed = False
        self.solved = False
        self.cathegories = []
        self.clues = []
        self.seed = 0
        
    get_grid_value = get_grid_value
    grid_insert = grid_insert
    print_grid = print_grid
    clear_grid = clear_grid
    is_grid_completed = is_grid_completed
    is_grid_contradictory = is_grid_contradictory
    set_seed = set_seed
    
    draw_cathegories = draw_cathegories
    draw_clues = draw_clues
    
    is_line_completed = is_line_completed
    count_x_in_line = count_x_in_line
    grid_concile1 = grid_concile1
    grid_concile2 = grid_concile2
    grid_concile3 = grid_concile3
    grid_concile4 = grid_concile4
    grid_concile5 = grid_concile5
    grid_concile = grid_concile
    
    add_clue1 = add_clue1
    add_clue2 = add_clue2
    use_clue1 = use_clue1
    use_clue2 = use_clue2
    is_grid_contradictory_with_clue2 = is_grid_contradictory_with_clue2
    
    try_to_solve = try_to_solve
    try_to_restrict_clues = try_to_restrict_clues
    