import numpy as np
import pandas as pd
import copy
import generating_categories_functions as funs

# ------------------ class methods ----------------------------

def grid_insert(self, K1, i1, K2, i2, val):
    if K1>=self.K or K2>=self.K or K1<0 or K2<0 or K1==K2:
        raise(Exception("Category index out of range!"))
    if i1>=self.k or i2>=self.k or i1<0 or i2<0:
        raise(Exception("Word in category index is out of range!"))
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
            raise(Exception("Category index out of range!"))
        if i1>=self.k or i2>=self.k or i1<0 or i2<0:
            raise(Exception("Word in category index is out of range!"))
        if K1<K2:
            j1 = i1
            j2 = i2
        else:
            j1 = i2
            j2 = i1
        return self.grid[str(min(K1, K2))+","+str(max(K1, K2))][j1, j2]

def is_line_completed(self, K1, i, K2):
    if K1<0 or K1>=self.K or K2<0 or K2>=self.K:
        raise(Exception("Wrong category id!"))
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
        raise(Exception("Wrong category id!"))
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
    """ 
    Conciliation no 1
    If there is an 'O' in the box add 'X's in all directions (cross like).
    """
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
    """ 
    Conciliation no 2
    If there is only one blank space in row/column insert 'O' in it (and add 'X's in all directions from it).
    """
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
    """ 
    Conciliation no 3
    If there is an 'O' in the box linking object i1 to object i2, concile their 'X's.
    That is, if i1 has an 'X' with some other object, i2 has to had 'X' with it too.
    """
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
    """ 
    Conciliation no 4
    Look for contradictory lines. If two lines with respect to some category K1 contradicts each other 
    (that is, in summary they exclude all of the options), then the objects associated with that lines 
    cannot be linked together (therefore we put 'X' there).
    """
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
    """ 
    Conciliation no 5
    If two/three line's blank spaces are restricted only to two/three the same options, then no other line can 
    have 'O' on the level of that blank space.
    """
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
    
def is_forbidden(self, clue_cand):
    """
    This function tests if a candicate for a clue is directly solving any clue type 4 or 5.
    Also detects too nested clues of type 2 or 3(only if k is small, otherwise nested clues 2 and 3 are allowed).
    """
    forbidden45 = []
    for clue in self.clues:
        if clue["typ"] in [4, 5]:
            forbidden45.append( (clue["K1"], clue["i1"], clue["K2"], clue["i2"]) )
            forbidden45.append( (clue["K3"], clue["i3"], clue["K4"], clue["i4"]) )
            if clue["typ"]==4:
                forbidden45.append( (clue["K5"], clue["i5"], clue["K6"], clue["i6"]) )
    forb_list = []
    for f in forbidden45:
        forb_list.append( (f[2:]+f[:2]) ) 
    forb_list += forbidden45
    
    if clue_cand["typ"]==1:
        for forb in forb_list:
            if (clue_cand["K1"], clue_cand["i1"], clue_cand["K2"], clue_cand["i2"])==forb:
                return True
            if "i3" in clue_cand:
                if (clue_cand["K1"], clue_cand["i1"], clue_cand["K2"], clue_cand["i3"])==forb:
                    return True
            if "i4" in clue_cand:
                if (clue_cand["K1"], clue_cand["i1"], clue_cand["K2"], clue_cand["i4"])==forb:
                    return True
    elif clue_cand["typ"]==2:
        for forb in forb_list:
            if (clue_cand["K1"], clue_cand["i1"], clue_cand["K6"], 0)==forb:
                return True
            if (clue_cand["K1"], clue_cand["i1"], clue_cand["K6"], 1)==forb:
                return True
            if (clue_cand["K2"], clue_cand["i2"], clue_cand["K6"], 0)==forb:
                return True
            if (clue_cand["K2"], clue_cand["i2"], clue_cand["K6"], self.k-1)==forb:
                return True
            if (clue_cand["K3"], clue_cand["i3"], clue_cand["K6"], self.k-1)==forb:
                return True
            if (clue_cand["K3"], clue_cand["i3"], clue_cand["K6"], self.k-2)==forb:
                return True
            
            if clue_cand["K1"]!=clue_cand["K2"] and (clue_cand["K1"], clue_cand["i1"], clue_cand["K2"], clue_cand["i2"])==forb:
                return True
            if clue_cand["K1"]!=clue_cand["K3"] and (clue_cand["K1"], clue_cand["i1"], clue_cand["K3"], clue_cand["i3"])==forb:
                return True
            if clue_cand["K2"]!=clue_cand["K3"] and (clue_cand["K2"], clue_cand["i2"], clue_cand["K3"], clue_cand["i3"])==forb:
                return True
    elif clue_cand["typ"]==3:
        for forb in forb_list:
            if clue_cand["K1"]!=clue_cand["K2"] and (clue_cand["K1"], clue_cand["i1"], clue_cand["K2"], clue_cand["i2"])==forb:
                return True
            
            if (clue_cand["K1"], clue_cand["i1"], clue_cand["K6"], self.k-1)==forb:
                return True
            if (clue_cand["K2"], clue_cand["i2"], clue_cand["K6"], 0)==forb:
                return True
    elif clue_cand["typ"]==6:
        for forb in forb_list:
            if clue_cand["K1"]!=clue_cand["K2"] and (clue_cand["K1"], clue_cand["i1"], clue_cand["K2"], clue_cand["i2"])==forb:
                return True
    
    if clue_cand["typ"]==2 and self.k<6:
        for clue in [ c for c in self.clues if c["typ"]==2 ]:
            if clue["K6"]==clue_cand["K6"]:
                if clue["K1"]==clue_cand["K3"] and clue["i1"]==clue_cand["i3"]:
                    return True
                if clue["K3"]==clue_cand["K1"] and clue["i3"]==clue_cand["i1"]:
                    return True
                if self.k<5:
                    if clue["K2"]==clue_cand["K3"] and clue["i2"]==clue_cand["i3"]:
                        return True
                    if clue["K2"]==clue_cand["K1"] and clue["i2"]==clue_cand["i1"]:
                        return True
                    if clue["K3"]==clue_cand["K2"] and clue["i3"]==clue_cand["i2"]:
                        return True
                    if clue["K1"]==clue_cand["K2"] and clue["i1"]==clue_cand["i2"]:
                        return True
        if self.k<5:
            for clue in [ c for c in self.clues if c["typ"]==3 ]:
                if clue["K6"]==clue_cand["K6"]:
                    if clue["K1"]==clue_cand["K1"] and clue["i1"]==clue_cand["i1"]:
                        return True
                    if clue["K2"]==clue_cand["K2"] and clue["i2"]==clue_cand["i2"]:
                        return True
    elif clue_cand["typ"]==3 and self.k<5:
        for clue in [ c for c in self.clues if c["typ"]==2 ]:
            if clue["K6"]==clue_cand["K6"]:
                if clue["K1"]==clue_cand["K1"] and clue["i1"]==clue_cand["i1"]:
                    return True
                if clue["K3"]==clue_cand["K2"] and clue["i3"]==clue_cand["i2"]:
                    return True

    return False
                                                
def add_clue1(self):
    """
    Adding clue of type 1:
    Single/double or triple 'X' in the grid.
    """
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
                        clue_cand = {"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j}
                        if self.is_forbidden(clue_cand):
                            break
                        self.clues.append(clue_cand)
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
                        clue_cand = {"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j}
                        if self.is_forbidden(clue_cand):
                            break
                        self.clues.append(clue_cand)
                        return
                    elif len(other_i)>no_of_x-1 and len(other_j)>no_of_x-1:
                        if np.random.randint(2)==0:
                            to_fill = np.random.choice(other_i, no_of_x-1, replace=False)
                            if no_of_x==2:
                                clue_cand = {"typ":1, "K1":K2, "i1":j, "K2":K1, "i2":i, "i3":to_fill[0]}
                                if self.is_forbidden(clue_cand):
                                    break
                                self.clues.append(clue_cand)
                                return
                            else:
                                clue_cand = {"typ":1, "K1":K2, "i1":j, "K2":K1, "i2":i, "i3":to_fill[0], "i4":to_fill[1]}
                                if self.is_forbidden(clue_cand):
                                    break
                                self.clues.append(clue_cand)
                                return
                        else:
                            to_fill = np.random.choice(other_j, no_of_x-1, replace=False)
                            if no_of_x==2:
                                clue_cand = {"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j, "i3":to_fill[0]}
                                if self.is_forbidden(clue_cand):
                                    break
                                self.clues.append(clue_cand)
                                return
                            else:
                                clue_cand = {"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j, "i3":to_fill[0], "i4":to_fill[1]}
                                if self.is_forbidden(clue_cand):
                                    break
                                self.clues.append(clue_cand)
                                return
                    elif len(other_i)>no_of_x-1:
                        to_fill = np.random.choice(other_i, no_of_x-1, replace=False)
                        if no_of_x==2:
                            clue_cand = {"typ":1, "K1":K2, "i1":j, "K2":K1, "i2":i, "i3":to_fill[0]}
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                        else:
                            clue_cand = {"typ":1, "K1":K2, "i1":j, "K2":K1, "i2":i, "i3":to_fill[0], "i4":to_fill[1]}
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                    else:
                        to_fill = np.random.choice(other_j, no_of_x-1, replace=False)
                        if no_of_x==2:
                            clue_cand = {"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j, "i3":to_fill[0]}
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                        else:
                            clue_cand = {"typ":1, "K1":K1, "i1":i, "K2":K2, "i2":j, "i3":to_fill[0], "i4":to_fill[1]}
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return

def add_clue2(self):
    """
    Adding clue of type 2:
    With respect to the Category K6(numerical or ordinal) we have 'K3,i3 < K2,i2 < K1,i1'.
    """
    K = self.K
    k = self.k
    
    K6_candidates = [ i for i, cat in enumerate(self.categories) if cat[0] in ['numerical','ordinal'] ]
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
                    
                    if K1!=K2:
                        values.append(self.get_grid_value(K1, i1, K2, i2))
                    if K1!=K3:
                        values.append(self.get_grid_value(K1, i1, K3, i3))
                    if K2!=K3:
                        values.append(self.get_grid_value(K2, i2, K3, i3))
                    
                    if any([val==1 for val in values]):
                        break
                    sum_of_free = sum([val==0 for val in values])
                    if sum_of_free>5:
                        clue_cand = {"typ":2, "K1":K1, "i1":i1, "K2":K2, "i2":i2, "K3":K3, "i3":i3, "K6": K6}
                        if self.is_forbidden(clue_cand):
                            break
                        self.clues.append(clue_cand)
                        return
    #print("Program couldn't fit any clue of type no 2!")
           
def add_clue3(self):
    """
    Adding clue of type 3:
    With respect to the Category K6 (numerical) we have 'K2,i2 = K1,i1 oper diff'.
    oper is one of {+, *}.
    """
    K = self.K
    k = self.k
    
    K6_candidates = [ i for i, cat in enumerate(self.categories) if cat[0]=='numerical' ]
    K6 = np.random.choice(K6_candidates, 1)[0]
    values = self.categories[K6][1]
    
    possible_randomized = np.random.permutation(list(self.categories[K6][2]))
    diff_list = [ float(diff_string.split("y")[-1][1:]) for diff_string in possible_randomized ]
    operations = [ diff_string.split("y")[-1][0] for diff_string in possible_randomized ]
    
    i_candidates = [ i for i in range(K*k) if i//k!=K6 ]
    i1_list = np.random.permutation(i_candidates)
    i2_list = np.random.permutation(i_candidates)
    
    for i1p in i1_list:
        for i2p in i2_list:
            for diff, operation in zip(diff_list, operations):
                if i1p!=i2p:
                    K1 = i1p//k
                    i1 = i1p%k
                    K2 = i2p//k
                    i2 = i2p%k
                    if operation=="+":
                        vals_for_X = []
                        for i in range(k):
                            if values[i]-diff not in values:
                                vals_for_X.append(self.get_grid_value(K2, i2, K6, i))
                            if values[i]+diff not in values:
                                vals_for_X.append(self.get_grid_value(K1, i1, K6, i))
                        if K1!=K2:
                            vals_for_X.append(self.get_grid_value(K1, i1, K2, i2))
                        if any([val==1 for val in vals_for_X]):
                            break
                        sum_of_free = sum([val==0 for val in vals_for_X])
                        if sum_of_free>1:
                            clue_cand = {"typ":3, "K1":K1, "i1":i1, "K2":K2, "i2":i2, "K6": K6, "diff":diff, "oper": operation}
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                    elif operation=="*":
                        vals_for_X = []
                        for i in range(k):
                            if values[i]/diff not in values:
                                vals_for_X.append(self.get_grid_value(K2, i2, K6, i))
                            if values[i]*diff not in values:
                                vals_for_X.append(self.get_grid_value(K1, i1, K6, i))
                        if K1!=K2:
                            vals_for_X.append(self.get_grid_value(K1, i1, K2, i2))
                        if any([val==1 for val in vals_for_X]):
                            break
                        sum_of_free = sum([val==0 for val in vals_for_X])
                        if sum_of_free>1:
                            clue_cand = {"typ":3, "K1":K1, "i1":i1, "K2":K2, "i2":i2, "K6": K6, "diff":diff, "oper": operation}
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                    else:
                        raise Exception("Unknown operation type: "+operation+"!")
    #print("Program couldn't fit any clue of type no 3!")
    
def add_clue4(self):
    """
    Adding clue of type 4:
    If K1,i1 match K2,i2 then K3,i3 match K4,i4 otherwise K5,i5 match K6,i6.
    """
    K = self.K
    k = self.k
    
    K12_candidates = np.random.permutation([ key for key in self.grid ])
    K34_candidates = np.random.permutation([ key for key in self.grid ])
    K56_candidates = np.random.permutation([ key for key in self.grid ])
    
    i_candidates = [ i for i in range(k) ]
    i1_list = np.random.permutation(i_candidates)
    i2_list = np.random.permutation(i_candidates)
    i3_list = np.random.permutation(i_candidates)
    i4_list = np.random.permutation(i_candidates)
    i5_list = np.random.permutation(i_candidates)
    i6_list = np.random.permutation(i_candidates)
    
    for K12 in K12_candidates:
        for K34 in K34_candidates:
            if K34!=K12:
                los = np.random.randint(2)
                if los==0:
                    K56 = K34
                else:
                    for Kxy in K56_candidates:
                        if Kxy!=K34 and Kxy!=K12:
                            K56 = Kxy
                for i1 in i1_list:
                    for i2 in i2_list:
                        for i3 in i3_list:
                            for i4 in i4_list:
                                for i5 in i5_list:
                                    for i6 in i6_list:
                                        if K34==K56 and i3==i5 and i4==i6:
                                            pass
                                        else:
                                            K1 = int(K12.split(",")[0])
                                            K2 = int(K12.split(",")[1])
                                            K3 = int(K34.split(",")[0])
                                            K4 = int(K34.split(",")[1])
                                            K5 = int(K56.split(",")[0])
                                            K6 = int(K56.split(",")[1])

                                            if self.get_grid_value(K1, i1, K2, i2)==0 and self.get_grid_value(K3, i3, K4, i4)==0 and self.get_grid_value(K5, i5, K6, i6)==0:
                                                if K34==K56:
                                                    vals_for_X = []
                                                    if i3!=i5 and i4!=i6:
                                                        vals_for_X.append(self.get_grid_value(K3, i5, K4, i4))
                                                        vals_for_X.append(self.get_grid_value(K3, i3, K4, i6))
                                                    elif i3==i5:
                                                        for i in range(k):
                                                            if i!=i4 and i!=i6:
                                                                vals_for_X.append(self.get_grid_value(K3, i3, K4, i))
                                                    else:
                                                        for i in range(k):
                                                            if i!=i3 and i!=i5:
                                                                vals_for_X.append(self.get_grid_value(K3, i, K4, i4))

                                                    if any([val==1 for val in vals_for_X]):
                                                        break
                                                    sum_of_free = sum([val==0 for val in vals_for_X])
                                                    if sum_of_free>1:
                                                        self.clues.append({"typ":4, "K1":K1, "i1":i1, "K2":K2, "i2": i2, "K3":K3, "i3":i3, "K4":K4, "i4":i4, "K5":K5, "i5":i5, "K6": K6, "i6": i6})
                                                        return
                                                else:
                                                    self.clues.append({"typ":4, "K1":K1, "i1":i1, "K2":K2, "i2": i2, "K3":K3, "i3":i3, "K4":K4, "i4":i4, "K5":K5, "i5":i5, "K6": K6, "i6": i6})
                                                    return

def add_clue5(self):
    """
    Adding clue of type 5:
    Either K1,i1 match K2,i2 or K3,i3 match K4,i4.
    """
    K = self.K
    k = self.k
    
    K12_candidates = np.random.permutation([ key for key in self.grid ])
    K34_candidates = np.random.permutation([ key for key in self.grid ])
    
    i_candidates = [ i for i in range(k) ]
    i1_list = np.random.permutation(i_candidates)
    i2_list = np.random.permutation(i_candidates)
    i3_list = np.random.permutation(i_candidates)
    i4_list = np.random.permutation(i_candidates)
    
    for K12 in K12_candidates:
        los = np.random.randint(2)
        if los==0:
            K34 = K12
        else:
            for Kxy in K34_candidates:
                if Kxy!=K12:
                    K34 = Kxy
            
        for i1 in i1_list:
            for i2 in i2_list:
                for i3 in i3_list:
                    for i4 in i4_list:
                        if K12==K34 and (i1==i3 or i2==i4):
                            pass
                        else:
                            K1 = int(K12.split(",")[0])
                            K2 = int(K12.split(",")[1])
                            K3 = int(K34.split(",")[0])
                            K4 = int(K34.split(",")[1])
                            if self.get_grid_value(K1, i1, K2, i2)==0 and self.get_grid_value(K3, i3, K4, i4)==0:
                                if K12==K34:
                                    vals_for_X = []
                                    if i1!=i3 and i2!=i4:
                                        vals_for_X.append(self.get_grid_value(K1, i1, K2, i4))
                                        vals_for_X.append(self.get_grid_value(K1, i3, K2, i2))
                                    elif i1==i3:
                                        for i in range(k):
                                            if i!=i2 and i!=i4:
                                                vals_for_X.append(self.get_grid_value(K1, i1, K2, i))
                                    else:
                                        for i in range(k):
                                            if i!=i1 and i!=i3:
                                                vals_for_X.append(self.get_grid_value(K1, i, K2, i2))

                                    if any([val==1 for val in vals_for_X]):
                                        break
                                    sum_of_free = sum([val==0 for val in vals_for_X])
                                    if sum_of_free>1:
                                        self.clues.append({"typ":5, "K1":K1, "i1":i1, "K2":K2, "i2": i2, "K3":K3, "i3":i3, "K4":K4, "i4":i4})
                                        return
                                else:
                                    self.clues.append({"typ":5, "K1":K1, "i1":i1, "K2":K2, "i2": i2, "K3":K3, "i3":i3, "K4":K4, "i4":i4})
                                    return
                                
def add_clue6(self):
    """
    Adding clue of type 6:
    With respect to the Category K6(numerical or ordinal) K1,i1 is right next to K2,i2.
    """
    K = self.K
    k = self.k
    
    K6_candidates = [ i for i, cat in enumerate(self.categories) if cat[0] in ['numerical','ordinal'] ]
    K6 = np.random.choice(K6_candidates, 1)[0]
    
    i_candidates = [ i for i in range(K*k) if i//k!=K6 ]
    i1_list = np.random.choice(i_candidates, len(i_candidates), replace=False)
    i2_list = np.random.choice(i_candidates, len(i_candidates), replace=False)
              
    for i1p in i1_list:
        for i2p in i2_list:
            if i1p!=i2p:
                K1 = i1p//k
                i1 = i1p%k
                K2 = i2p//k
                i2 = i2p%k
                possible_pairs = 0
                for i in range(k):
                    if i!=0 and self.get_grid_value(K1, i1, K6, i)==0 and self.get_grid_value(K2, i2, K6, i-1)==0:
                        possible_pairs += 1
                    if i!=k-1 and self.get_grid_value(K1, i1, K6, i)==0 and self.get_grid_value(K2, i2, K6, i+1)==0:
                        possible_pairs += 1
                if possible_pairs>k-1:
                    clue_cand = {"typ":6, "K1":K1, "i1":i1, "K2":K2, "i2":i2, "K6": K6}
                    if self.is_forbidden(clue_cand):
                        break
                    self.clues.append(clue_cand)
                    return
                        
def use_clue1(self, c):
    clue = self.clues[c]
    self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i2"], "X")
    if "i3" in clue:
        self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i3"], "X")
        if "i4" in clue:
              self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i4"], "X")
                
def use_clue2(self, c):
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
            
def use_clue3(self, c):
    clue = self.clues[c]
    operation = clue["oper"]
    diff = clue["diff"]
    values = self.categories[clue["K6"]][1]
    
    if clue["K1"]!=clue["K2"]:
        self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i2"], "X")
    
    if operation=="+":
        for i in range(self.k):
            if values[i]-diff not in values or self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], values.index(values[i]-diff))==2:
                self.grid_insert(clue["K2"], clue["i2"], clue["K6"], i, "X")
            if values[i]+diff not in values or self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], values.index(values[i]+diff))==2:
                self.grid_insert(clue["K1"], clue["i1"], clue["K6"], i, "X")
    elif operation=="*":
        for i in range(self.k):
            if values[i]/diff not in values or self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], values.index(values[i]/diff))==2:
                self.grid_insert(clue["K2"], clue["i2"], clue["K6"], i, "X")
            if values[i]*diff not in values or self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], values.index(values[i]*diff))==2:
                self.grid_insert(clue["K1"], clue["i1"], clue["K6"], i, "X")            
            
def use_clue4(self, c):
    clue = self.clues[c]    
    
    K1 = clue["K1"]
    K2 = clue["K2"]
    K3 = clue["K3"]
    K4 = clue["K4"]
    K5 = clue["K5"]
    K6 = clue["K6"]
    i1 = clue["i1"]
    i2 = clue["i2"]
    i3 = clue["i3"]
    i4 = clue["i4"]
    i5 = clue["i5"]
    i6 = clue["i6"]
    
    if K3==K5 and K4==K6:
        if i3!=i5 and i4!=i6:
            self.grid_insert(K3, i5, K4, i4, "X")
            self.grid_insert(K3, i3, K4, i6, "X")
        elif i3==i5:
            for i in range(self.k):
                if i!=i4 and i!=i6:
                    self.grid_insert(K3, i3, K4, i, "X")
        else:
            for i in range(self.k):
                if i!=i3 and i!=i5:
                    self.grid_insert(K3, i, K4, i4, "X")
            
    if self.get_grid_value(K3, i3, K4, i4)==2:
        self.grid_insert(K1, i1, K2, i2, "X")
        
    if self.get_grid_value(K5, i5, K6, i6)==2:
        self.grid_insert(K1, i1, K2, i2, "O")
    
    if self.get_grid_value(K1, i1, K2, i2)==1:
        self.grid_insert(K3, i3, K4, i4, "O")
    elif self.get_grid_value(K1, i1, K2, i2)==2:
        self.grid_insert(K5, i5, K6, i6, "O")
        
def use_clue5(self, c):
    clue = self.clues[c]    
    
    K1 = clue["K1"]
    K2 = clue["K2"]
    K3 = clue["K3"]
    K4 = clue["K4"]
    i1 = clue["i1"]
    i2 = clue["i2"]
    i3 = clue["i3"]
    i4 = clue["i4"]
    
    if K1==K3 and K2==K4:
        if i1!=i3 and i2!=i4:
            self.grid_insert(K1, i3, K2, i2, "X")
            self.grid_insert(K1, i1, K2, i4, "X")
        elif i1==i3:
            for i in range(self.k):
                if i!=i2 and i!=i4:
                    self.grid_insert(K1, i1, K2, i, "X")
        else:
            for i in range(self.k):
                if i!=i1 and i!=i3:
                    self.grid_insert(K1, i, K2, i2, "X")
            
    if self.get_grid_value(K1, i1, K2, i2)==2:
        self.grid_insert(K3, i3, K4, i4, "O")
    elif self.get_grid_value(K3, i3, K4, i4)==2:
        self.grid_insert(K1, i1, K2, i2, "O")
    
def use_clue6(self, c):
    clue = self.clues[c]
    K1 = clue["K1"]
    K2 = clue["K2"]
    K6 = clue["K6"]
    i1 = clue["i1"]
    i2 = clue["i2"]
        
    for i in range(self.k):
        if self.get_grid_value(K1, i1, K6, i)==0:
            if (i==0 or self.get_grid_value(K2, i2, K6, i-1)==2) and (i==self.k-1 or self.get_grid_value(K2, i2, K6, i+1)==2):
                self.grid_insert(K1, i1, K6, i, "X")
        elif self.get_grid_value(K1, i1, K6, i)==1:
            for j in range(self.k):
                if j!=i-1 and j!=i+1:
                    self.grid_insert(K2, i2, K6, j, "X")
        if self.get_grid_value(K2, i2, K6, i)==0:
            if (i==0 or self.get_grid_value(K1, i1, K6, i-1)==2) and (i==self.k-1 or self.get_grid_value(K1, i1, K6, i+1)==2):
                self.grid_insert(K2, i2, K6, i, "X")
        elif self.get_grid_value(K2, i2, K6, i)==1:
            for j in range(self.k):
                if j!=i-1 and j!=i+1:
                    self.grid_insert(K1, i1, K6, j, "X")
    
def use_clue(self, c):
    if len(self.clues)<=c or c<0:
        raise Exception("Wrong clue id provided!") 
    if self.clues[c]["typ"] not in [1, 2, 3, 4, 5, 6]:
        raise Exception("Wrong clue type provided!") 
        
    typ = self.clues[c]["typ"]
    if typ==1:
        self.use_clue1(c)
    elif typ==2:
        self.use_clue2(c)
    elif typ==3:
        self.use_clue3(c)
    elif typ==4:
        self.use_clue4(c)
    elif typ==5:
        self.use_clue5(c)
    elif typ==6:
        self.use_clue6(c)
        
            
def is_grid_contradictory_with_clue2(self, c):
    if len(self.clues)<=c or c<0:
        raise Exception("Wrong clue id provided!")
    if self.clues[c]["typ"]!=2:
        raise Exception("Wrong clue type provided!")
       
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
          
def is_grid_contradictory_with_clue3(self, c):
    if len(self.clues)<=c or c<0:
        raise Exception("Wrong clue id provided!")
    if self.clues[c]["typ"]!=3:
        raise Exception("Wrong clue type provided!")
       
    clue = self.clues[c]
    operation = clue["oper"]
    diff = clue["diff"]
    values = self.categories[clue["K6"]][1]
    
    if operation=="+":
        for i in range(self.k):
            if values[i]+diff in values and self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], i)!=2 and self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], values.index(values[i]+diff))!=2:
                return False
    elif operation=="*":
        for i in range(self.k):
            if values[i]*diff in values and self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], i)!=2 and self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], values.index(values[i]*diff))!=2:
                return False
    return True

def is_grid_contradictory_with_clue4(self, c):
    if len(self.clues)<=c or c<0:
        raise Exception("Wrong clue id provided!")
    if self.clues[c]["typ"]!=4:
        raise Exception("Wrong clue type provided!")
       
    clue = self.clues[c]
    if self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"])==2 and self.get_grid_value(clue["K5"], clue["i5"], clue["K6"], clue["i6"])==2:
        return True
    if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"])==1 and self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"])==2:
        return True
    if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"])==2 and self.get_grid_value(clue["K5"], clue["i5"], clue["K6"], clue["i6"])==2:
        return True
    return False

def is_grid_contradictory_with_clue5(self, c):
    if len(self.clues)<=c or c<0:
        raise Exception("Wrong clue id provided!")
    if self.clues[c]["typ"]!=5:
        raise Exception("Wrong clue type provided!")
       
    clue = self.clues[c]
    if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"])==2 and self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"])==2:
        return True
    return False

def is_grid_contradictory_with_clue6(self, c):
    if len(self.clues)<=c or c<0:
        raise Exception("Wrong clue id provided!")
    if self.clues[c]["typ"]!=6:
        raise Exception("Wrong clue type provided!")
       
    clue = self.clues[c]
    k = self.k
    K1 = clue["K1"]
    K2 = clue["K2"]
    K6 = clue["K6"]
    i1 = clue["i1"]
    i2 = clue["i2"]
    
    possible_pairs = 0
    for i in range(k):
        if i!=0 and self.get_grid_value(K1, i1, K6, i)!=2 and self.get_grid_value(K2, i2, K6, i-1)!=2:
            possible_pairs += 1
            break
        if i!=k-1 and self.get_grid_value(K1, i1, K6, i)!=2 and self.get_grid_value(K2, i2, K6, i+1)!=2:
            possible_pairs += 1
            break
    if possible_pairs==0:
        return True
    for i in range(k):
        if self.get_grid_value(K1, i1, K6, i)==1:
            if (i==0 or self.get_grid_value(K2, i2, K6, i-1)==2) and (i==k-1 or self.get_grid_value(K2, i2, K6, i+1)==2):
                return True
        if self.get_grid_value(K2, i2, K6, i)==1:
            if (i==0 or self.get_grid_value(K1, i1, K6, i-1)==2) and (i==k-1 or self.get_grid_value(K1, i1, K6, i+1)==2):
                return True
            
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
            #print("Puzzle is contradictory with clue 2!")
            return True
    clues3 = [ i for i,clue in enumerate(self.clues) if clue["typ"]==3 ]
    for c in clues3:
        if self.is_grid_contradictory_with_clue3(c):
            #print("Puzzle is contradictory with clue 3!")
            return True
    clues4 = [ i for i,clue in enumerate(self.clues) if clue["typ"]==4 ]
    for c in clues4:
        if self.is_grid_contradictory_with_clue4(c):
            #print("Puzzle is contradictory with clue 4!")
            return True
    clues5 = [ i for i,clue in enumerate(self.clues) if clue["typ"]==5 ]
    for c in clues5:
        if self.is_grid_contradictory_with_clue5(c):
            #print("Puzzle is contradictory with clue 5!")
            return True
    clues6 = [ i for i,clue in enumerate(self.clues) if clue["typ"]==6 ]
    for c in clues6:
        if self.is_grid_contradictory_with_clue6(c):
            #print("Puzzle is contradictory with clue 6!")
            return True
    return False

def set_seed(self, seed):
    self.seed = seed
    np.random.seed(self.seed)

def draw_categories(self, diff=3):
    if not diff in [2,3,4]:
        raise Exception("Można losować zagadki tylko o liczbie gwiazdek równej 2, 3 albo 4!")
    self.categories = funs.losuj_kategorie(self.K, self.k, diff, self.seed)
    i = 0
    i_max = 100
    while funs.do_categories_repeat(self.categories):
        self.categories = funs.losuj_kategorie(self.K, self.k, diff, self.seed+i*1234567)
        i += 1
        if i>i_max:
            raise Exception("Program couldn't draw non-repeating categories!")

def try_to_solve2(self):
    clues1 = [ i for i,clue in enumerate(self.clues) if clue["typ"]==1 ]
    clues2 = [ i for i,clue in enumerate(self.clues) if clue["typ"]!=1 ]
    
    for c in clues1:
        self.use_clue1(c)
    self.grid_concile()
    
    self.changed = True
    while self.changed:
        self.changed = False
        for c in clues2:
            self.use_clue(c)
            self.grid_concile()
            if self.is_grid_contradictory() or self.is_grid_completed():
                return            
            
def try_to_solve(self):
    self.solved = False
    self.contradictory = False
    grid_main_copy = copy.deepcopy(self.grid)
    self.changed = True
    while self.changed:
        self.changed = False
        self.try_to_solve2()
        key_candidates = np.random.permutation(list(self.grid.keys()))
        for key in key_candidates:
            for i in range(self.k):
                for j in range(self.k):
                    K1 = int(key.split(",")[0])
                    K2 = int(key.split(",")[1])
                    if self.get_grid_value(K1, i, K2, j)==0:
                        grid_copy = copy.deepcopy(self.grid)
                        self.grid_insert(K1, i, K2, j, "O")
                        self.try_to_solve2()
                        if self.is_grid_contradictory():
                            self.grid = grid_copy
                            self.grid_insert(K1, i, K2, j, "X")
                            self.diff += 1
                            self.try_to_solve2()
                            if self.is_grid_contradictory():
                                self.contradictory = True
                                return
                            if self.is_grid_completed():
                                self.solved = True
                                return
                        else:
                            self.grid = grid_copy
    #self.grid = grid_main_copy
        
def draw_clues(self, trace=False):
    non_1_clues = int(np.ceil(self.k*self.K/2.3))
    for i in range(non_1_clues):
        typ = np.random.choice([2, 3, 4, 5, 6], 1, p=[0.2, 0.2, 0.2, 0.2, 0.2])[0]
        if trace:
            print("Trying to fit clue of type "+str(typ))
        if typ==2:
            self.add_clue2()
        elif typ==3:
            self.add_clue3()
        elif typ==4:
            self.add_clue4()
        elif typ==5:
            self.add_clue5()
        elif typ==6:
            self.add_clue6()
           
        if trace and len(self.clues)<i:
            print("Failed to draw clue of type "+str(typ))
        
        if len(self.clues)>0:
            self.use_clue(len(self.clues)-1)
            self.grid_concile()
            for j in range(len(self.clues)):
                self.use_clue(j)
            self.grid_concile()
        
        if trace:
            self.print_grid()
            self.print_info()
        
        if self.is_grid_completed() or self.is_grid_contradictory():
            break
    if trace:
        print("-------------- Started to fit clues of type 1 ---------")
    
    non_1_clues = len(self.clues)
    for i in range(100):
        self.add_clue1()
        self.use_clue(len(self.clues)-1)
        self.grid_concile()
        if trace:
            print("Clue of type 1 added")
        for j in range(non_1_clues):
            self.use_clue(j)
            self.grid_concile()
            if self.is_grid_completed() or self.is_grid_contradictory():
                return
        if trace:
            self.print_grid()
            self.print_info()

def try_to_restrict_clues(self):
    clues_copy = copy.deepcopy(self.clues)
    to_restrict = []
        
    clues1 = [ i for i, clue in enumerate(clues_copy) if clue["typ"]==1 ]
    clue_order = np.random.choice(clues1, len(clues1), replace=False)
    for i in clue_order:
        clues1_restricted = [ j for j in clues1 if j!=i ]
        self.clear_grid()
        self.clues = [ clue for j, clue in enumerate(clues_copy) if j in clues1_restricted or not j in clue_order ]
        self.try_to_solve()
        if self.is_grid_completed() and not self.is_grid_contradictory():
            to_restrict.append(i)
            clues1 = clues1_restricted
            
    clues_other = [ i for i, clue in enumerate(clues_copy) if clue["typ"]!=1 ]
    clue_order = np.random.permutation(clues_other)
    for i in clue_order:
        clues_restricted = [ j for j in clues_other if j!=i ]
        self.clear_grid()
        self.clues = [ clue for j, clue in enumerate(clues_copy) if j in clues_restricted or j in clues1 ]
        self.try_to_solve()
        if self.is_grid_completed() and not self.is_grid_contradictory():
            to_restrict.append(i)
            clues_other = clues_restricted        
            
    #print(to_restrict)
    self.clues = [ clue for j, clue in enumerate(clues_copy) if not j in to_restrict ]

def generate(self, seed=0, trace=False):
    self.set_seed(seed)
    if trace:
        print("Generating puzzle for seed="+str(seed))
        print("Drawing categories...")
    self.draw_categories()
    if trace:
        print("Categories drawn:")
        for c in self.categories:
            print(c)
    if trace:
        print("Drawing clues...")        
    i_max = 100
    for i in range(i_max):
        self.clear_grid()
        self.clues = []
        self.draw_clues()
        if self.is_grid_completed() and not self.is_grid_contradictory():
            break
        if trace and i==i_max-1:
            print("Failed to draw clues!!!")
    if trace:
        clues_counts = [ len([i for i in self.clues if i["typ"]==j]) for j in range(1,7)]
        print("No of clues drawn = "+str(len(self.clues))+str(clues_counts))
        print("Restricting clues...")
    self.try_to_restrict_clues() 
    if trace:
        print("Final difficulty assessment...")
    N = 5
    diffs = []
    for n in range(N):
        self.clear_grid()
        self.diff = 0
        self.try_to_solve()
        diffs.append(self.diff)
    if trace:
        print("Difficulty: "+str(np.mean(diffs))+str(diffs))
    self.diff = round(np.mean(diffs),2)

def print_info(self):
    print("Seed: "+str(self.seed)+", difficulty: "+str(self.diff))
    print("Completed: "+str(self.is_grid_completed())+", Contradictory: "+str(self.is_grid_contradictory()) )
    clues_counts = [ len([i for i in self.clues if i["typ"]==j]) for j in range(1,7)]
    print("K: "+str(self.K)+", k: "+str(self.k)+", No of clues: "+str(len(self.clues))+str(clues_counts))
    
    
# --------------------- class definition ------------------------------
    
class puzzle:
    def __init__(self, K, k):
        self.K = K
        self.k = k
        self.grid = { str(i)+","+str(j): np.zeros((k,k)) for i in range(K) for j in range(K) if i<j }
        self.changed = False
        self.solved = False
        self.contradictory = False
        self.categories = []
        self.clues = []
        self.seed = 0
        self.diff = 0
        
    get_grid_value = get_grid_value
    grid_insert = grid_insert
    print_grid = print_grid
    clear_grid = clear_grid
    is_grid_completed = is_grid_completed
    is_grid_contradictory = is_grid_contradictory
    print_info = print_info
   
    set_seed = set_seed
    draw_categories = draw_categories
    draw_clues = draw_clues
    
    is_line_completed = is_line_completed
    count_x_in_line = count_x_in_line
    grid_concile1 = grid_concile1
    grid_concile2 = grid_concile2
    grid_concile3 = grid_concile3
    grid_concile4 = grid_concile4
    grid_concile5 = grid_concile5
    grid_concile = grid_concile
    
    is_forbidden = is_forbidden
    add_clue1 = add_clue1
    add_clue2 = add_clue2
    add_clue3 = add_clue3
    add_clue4 = add_clue4
    add_clue5 = add_clue5
    add_clue6 = add_clue6
    
    use_clue = use_clue
    use_clue1 = use_clue1
    use_clue2 = use_clue2
    use_clue3 = use_clue3
    use_clue4 = use_clue4
    use_clue5 = use_clue5
    use_clue6 = use_clue6
    
    is_grid_contradictory_with_clue2 = is_grid_contradictory_with_clue2
    is_grid_contradictory_with_clue3 = is_grid_contradictory_with_clue3
    is_grid_contradictory_with_clue4 = is_grid_contradictory_with_clue4
    is_grid_contradictory_with_clue5 = is_grid_contradictory_with_clue5
    is_grid_contradictory_with_clue6 = is_grid_contradictory_with_clue6
    
    try_to_solve2 = try_to_solve2
    try_to_solve = try_to_solve
    try_to_restrict_clues = try_to_restrict_clues
    generate = generate
    