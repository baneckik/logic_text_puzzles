from numpy import random, unique, zeros, ceil, mean
import copy
import generating_categories_functions as funs
from collections import Counter


# ------------------ class methods ----------------------------


def grid_insert(self, K1, i1, K2, i2, val, solution_code=None, collect_solution=False):
    if K1 >= self.K or K2 >= self.K or K1 < 0 or K2 < 0 or K1 == K2:
        raise (Exception("Category index out of range!"))
    if i1 >= self.k or i2 >= self.k or i1 < 0 or i2 < 0:
        raise (Exception("Word in category index is out of range!"))
    if K1 < K2:
        j1 = i1
        j2 = i2
    else:
        j1 = i2
        j2 = i1
    if val == 0 or val == "-":
        val2 = 0
    elif val == 1 or val == "O":
        val2 = 1
    elif val == 2 or val == "X":
        val2 = 2
    else:
        raise (Exception("Wrong value format! value must be either one of {0,1,2} or {-,O,X}"))

    # if new value is being inserted:
    if self.grid[str(min(K1, K2)) + "," + str(max(K1, K2))][j1, j2] != val2:
        # collect info for solution:
        if collect_solution:
            self.solution += str(val2) + "," + str(K1) + "," + str(i1) + "," + str(K2) + "," + str(
                i2) + "," + solution_code + ";"
        # insertion:
        self.changed = True
        self.changed2 = True
        self.changed3 = True

        self.grid[str(min(K1, K2)) + "," + str(max(K1, K2))][j1, j2] = val2

        # adding clues to that need to be checked after insertion to the self.clues_to_check list:
        for i, clue_crit_squares in enumerate(self.critical_squares):
            for crit_s in clue_crit_squares:
                if crit_s[0] == K1 and crit_s[1] == i1 and crit_s[2] == K2 and crit_s[3] == i2:
                    self.clues_to_check.append(i)
                    break
                if crit_s[0] == K2 and crit_s[1] == i2 and crit_s[2] == K1 and crit_s[3] == i1:
                    self.clues_to_check.append(i)
                    break

        # further basic operation on the grid:
        if val2 == 1:
            for l in range(self.k):
                if l != i1:
                    self.grid_insert(K1, l, K2, i2, "X", "conc1", collect_solution)
                if l != i2:
                    self.grid_insert(K1, i1, K2, l, "X", "conc1", collect_solution)
        elif val2 == 2:
            if self.count_x_in_line(K1, i1, K2) == self.k - 1 and not self.is_line_completed(K1, i1, K2):
                for j in range(self.k):
                    if self.get_grid_value(K1, i1, K2, j) == 0:
                        self.grid_insert(K1, i1, K2, j, "O", "conc2", collect_solution)
                        break
            if self.count_x_in_line(K2, i2, K1) == self.k - 1 and not self.is_line_completed(K2, i2, K1):
                for j in range(self.k):
                    if self.get_grid_value(K2, i2, K1, j) == 0:
                        self.grid_insert(K2, i2, K1, j, "O", "conc2", collect_solution)
                        break


def print_grid(self):
    for K_row in range(self.K - 1):
        for row in range(self.k):
            line = ""
            for K_col in range(self.K - 1 - K_row):
                for col in range(self.k):
                    val = self.get_grid_value(K_row, row, self.K - 1 - K_col, col)
                    if val == 0:
                        line += "-"
                    elif val == 1:
                        line += "O"
                    else:
                        line += "X"
                line += " "
            print(line)
        print()


def clear_grid(self):
    for key in self.grid:
        self.grid[key] = zeros((self.k, self.k))


def get_grid_value(self, K1, i1, K2, i2):
    if K1 >= self.K or K2 >= self.K or K1 < 0 or K2 < 0 or K1 == K2:
        raise (Exception("Category index out of range!"))
    if i1 >= self.k or i2 >= self.k or i1 < 0 or i2 < 0:
        raise (Exception("Word in category index is out of range!"))
    if K1 < K2:
        j1 = i1
        j2 = i2
    else:
        j1 = i2
        j2 = i1
    return self.grid[str(min(K1, K2)) + "," + str(max(K1, K2))][j1, j2]


def is_line_completed(self, K1, i1, K2):
    if K1 < 0 or K1 >= self.K or K2 < 0 or K2 >= self.K:
        raise (Exception("Wrong category id!"))
    if i1 < 0 or i1 >= self.k:
        raise (Exception("Wrong row/column id!"))

    box = self.grid[str(min(K1, K2)) + "," + str(max(K1, K2))]
    x_count = 0
    o_count = 0
    if K1 < K2:
        for j in range(self.k):
            if box[i1, j] == 1:
                o_count += 1
            elif box[i1, j] == 2:
                x_count += 1
    else:
        for j in range(self.k):
            if box[j, i1] == 1:
                o_count += 1
            elif box[j, i1] == 2:
                x_count += 1
    return x_count == self.k - 1 and o_count == 1


def count_x_in_line(self, K1, i1, K2):
    if K1 < 0 or K1 >= self.K or K2 < 0 or K2 >= self.K:
        raise (Exception("Wrong category id!"))
    if i1 < 0 or i1 >= self.k:
        raise (Exception("Wrong row/column id!"))

    box = self.grid[str(min(K1, K2)) + "," + str(max(K1, K2))]
    x_count = 0
    if K1 < K2:
        for j in range(self.k):
            if box[i1, j] == 2:
                x_count += 1
    else:
        for j in range(self.k):
            if box[j, i1] == 2:
                x_count += 1
    return x_count


def is_line_possible_for_group(self, K1, i1, K2, group):
    box = self.grid[str(min(K1, K2)) + "," + str(max(K1, K2))]
    groups = self.categories[K2]["groups"]
    if K1 < K2:
        for j in range(self.k):
            if groups[j] == group and box[i1, j] != 2:
                return True
    else:
        for j in range(self.k):
            if groups[j] == group and box[j, i1] != 2:
                return True
    return False


def is_o_in_line_for_group(self, K1, i1, K2, group):
    box = self.grid[str(min(K1, K2)) + "," + str(max(K1, K2))]
    groups = self.categories[K2]["groups"]
    if K1 < K2:
        for j in range(self.k):
            if groups[j] == group and box[i1, j] == 1:
                return True
    else:
        for j in range(self.k):
            if groups[j] == group and box[j, i1] == 1:
                return True
    return False


def grid_concile1(self, collect_solution=False):
    """
    Conciliation no 1
    If there is an 'O' in the square add 'X's in all directions (cross like).
    """
    K = self.K
    k = self.k
    for key in self.grid:
        K1 = int(key.split(",")[0])
        K2 = int(key.split(",")[1])
        for i in range(k):
            for j in range(k):
                if self.grid[key][i, j] == 1:
                    for l in range(k):
                        if l != i:
                            self.grid_insert(K1, l, K2, j, "X", "conc1", collect_solution)
                        if l != j:
                            self.grid_insert(K1, i, K2, l, "X", "conc1", collect_solution)


def grid_concile2(self, collect_solution=False):
    """ 
    Conciliation no 2
    If there is only one blank square in row/column insert 'O' in it (and add 'X's in all directions from it).
    """
    for key in self.grid:
        K1 = int(key.split(",")[0])
        K2 = int(key.split(",")[1])
        for i in range(self.k):
            if self.count_x_in_line(K1, i, K2) == self.k - 1 and not self.is_line_completed(K1, i, K2):
                for j in range(self.k):
                    if self.get_grid_value(K1, i, K2, j) == 0:
                        self.grid_insert(K1, i, K2, j, "O", "conc2", collect_solution)
                        for i2 in range(self.k):
                            if i2 != i:
                                self.grid_insert(K1, i2, K2, j, "X", "conc2", collect_solution)
                        break

            if self.count_x_in_line(K2, i, K1) == self.k - 1 and not self.is_line_completed(K2, i, K1):
                for j in range(self.k):
                    if self.get_grid_value(K2, i, K1, j) == 0:
                        self.grid_insert(K2, i, K1, j, "O", "conc2", collect_solution)
                        for i2 in range(self.k):
                            if i2 != i:
                                self.grid_insert(K2, i2, K1, j, "X", "conc2", collect_solution)
                        break


def grid_concile3(self, collect_solution=False):
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
                if self.grid[key][i, j] == 1:
                    for K3 in range(K):
                        if K3 != K2 and K3 != K1:
                            for j2 in range(k):
                                if self.get_grid_value(K1, i, K3, j2) == 2:
                                    self.grid_insert(K2, j, K3, j2, "X", "conc3", collect_solution)
                                if self.get_grid_value(K2, j, K3, j2) == 2:
                                    self.grid_insert(K1, i, K3, j2, "X", "conc3", collect_solution)


def grid_concile4(self, collect_solution=False):
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
            if K2 != K1:
                for K3 in range(K2 + 1, K):
                    if K3 != K1:
                        for j2 in range(k):
                            for j3 in range(k):
                                contradictory_lines = True
                                for i in range(k):
                                    val1 = self.get_grid_value(K1, i, K2, j2)
                                    val2 = self.get_grid_value(K1, i, K3, j3)
                                    if val1 != 2 and val2 != 2:
                                        contradictory_lines = False
                                        break
                                if contradictory_lines:
                                    self.grid_insert(K2, j2, K3, j3, "X", "conc4", collect_solution)


def grid_concile5(self, collect_solution=False):
    """ 
    Conciliation no 5
    If two/three line's blank spaces are restricted only to two/three the same options, then no other line can 
    have 'O' on the level of that blank square.
    """
    K = self.K
    k = self.k
    if k < 4:
        return

    for K1 in range(K):
        for K2 in range(K):
            if K1 != K2:
                # double lines to concile
                for i1 in range(k):
                    for i2 in range(i1 + 1, k):
                        common_empty = []
                        concile = True
                        for j in range(k):
                            val1 = self.get_grid_value(K1, i1, K2, j)
                            val2 = self.get_grid_value(K1, i2, K2, j)
                            if val1 != val2 or val1 == 1 or val2 == 1:
                                concile = False
                                break
                            if val1 == 0 and val1 == val2:
                                common_empty.append(j)
                        if concile and len(common_empty) == 2:
                            for j in common_empty:
                                for i3 in range(k):
                                    if i3 != i1 and i3 != i2:
                                        self.grid_insert(K1, i3, K2, j, "X", "conc5", collect_solution)
                # triple lines to reconcile
                if k > 5:
                    for i1 in range(k):
                        for i2 in range(i1 + 1, k):
                            for i3 in range(i2 + 1, k):
                                common_empty = []
                                concile = True
                                for j in range(k):
                                    val1 = self.get_grid_value(K1, i1, K2, j)
                                    val2 = self.get_grid_value(K1, i2, K2, j)
                                    val3 = self.get_grid_value(K1, i3, K2, j)
                                    if val1 != val2 or val3 != val2 or val1 == 1 or val2 == 1 or val3 == 1:
                                        concile = False
                                        break
                                    if val1 == 0 and val1 == val2 and val2 == val3:
                                        common_empty.append(j)
                                if concile and len(common_empty) == 3:
                                    for j in common_empty:
                                        for i4 in range(k):
                                            if i4 != i1 and i4 != i2 and i4 != i3:
                                                self.grid_insert(K1, i4, K2, j, "X", "conc5", collect_solution)


def grid_concile(self, collect_solution=False):
    # changed_copy = self.changed
    self.changed = True
    while self.changed:
        self.changed = False
        # self.grid_concile1(collect_solution)
        # self.grid_concile2(collect_solution)
        self.grid_concile3(collect_solution)
        self.grid_concile4(collect_solution)
        self.grid_concile5(collect_solution)
        # if self.changed:
        #   changed_copy = True
    # self.changed = changed_copy


def get_critical_squares_from_between(self, clue, K1, i1, K2, i2):
    """
    Arguments are expected in the string form of K1="1", i1="3" etc.
    """
    critical = []
    # intersection between K1,i1 and K2,i2
    if clue["K" + K1] != clue["K" + K2]:
        if "i" + i1 in clue and "i" + i2 in clue:
            critical += [(clue["K" + K1], clue["i" + i1], clue["K" + K2], clue["i" + i2])]
        elif "i" + i1 in clue:
            for j in range(self.k):
                if self.categories[clue["K" + K2]]["groups"][j] == clue["g" + i2]:
                    critical += [(clue["K" + K1], clue["i" + i1], clue["K" + K2], j)]
        elif "i" + i2 in clue:
            for j in range(self.k):
                if self.categories[clue["K" + K1]]["groups"][j] == clue["g" + i1]:
                    critical += [(clue["K" + K1], j, clue["K" + K2], clue["i" + i2])]
        else:
            for i in range(self.k):
                if self.categories[clue["K" + K1]]["groups"][i] == clue["g" + i1]:
                    for j in range(self.k):
                        if self.categories[clue["K" + K2]]["groups"][j] == clue["g" + i2]:
                            critical += [(clue["K" + K1], i, clue["K" + K2], j)]
    return critical


def get_critical_squares_from_line(self, clue, K1, i1, K6):
    """
    Arguments are expected in the string form of K1="1", i1="3" etc.
    """
    critical = []
    # intersection between K1,i1 and K6, or all lines from g1 with K6
    if "i" + i1 in clue:
        for i in range(self.k):
            critical += [(clue["K" + K1], clue["i" + i1], clue["K" + K6], i)]
    else:
        for j in range(self.k):
            if self.categories[clue["K" + K1]]["groups"][j] == clue["g" + i1]:
                for i in range(self.k):
                    critical += [(clue["K" + K1], j, clue["K" + K6], i)]
    return critical


def get_critical_squares(self, clue, everything=False):
    """
    Function return critical squares of a certain clue. Critical squares are squares in which basing on 
    the clue one can immediately put 'X' there or if someone puts 'O' there some clue is completely/partially being solved.
    Version with everything==False is for squares to exclude when drawing another clue.
    Version with everything==True is for the solving algorithm to to know what clues are worth checking after insertion.
    """
    critical = []
    if clue["typ"] == 1:
        if not everything:
            if "i1" in clue and "i2" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i2"])]
            if "i1" in clue and "i3" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i3"])]
            if "i1" in clue and "i4" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i4"])]
        else:
            critical += self.get_critical_squares_from_between(clue, "1", "1", "2", "2")
            if "i3" in clue or "g3" in clue:
                critical += self.get_critical_squares_from_between(clue, "1", "1", "2", "3")
                if "i4" in clue or "g4" in clue:
                    critical += self.get_critical_squares_from_between(clue, "1", "1", "2", "4")

    elif clue["typ"] == 2:
        if not everything:
            if "i1" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K6"], 0)]
                critical += [(clue["K1"], clue["i1"], clue["K6"], 1)]
            if "i2" in clue:
                critical += [(clue["K2"], clue["i2"], clue["K6"], 0)]
                critical += [(clue["K2"], clue["i2"], clue["K6"], self.k - 1)]
            if "i3" in clue:
                critical += [(clue["K3"], clue["i3"], clue["K6"], self.k - 2)]
                critical += [(clue["K3"], clue["i3"], clue["K6"], self.k - 1)]

            if clue["K1"] != clue["K2"] and "i1" in clue and "i2" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i2"])]
            if clue["K1"] != clue["K3"] and "i1" in clue and "i3" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K3"], clue["i3"])]
            if clue["K2"] != clue["K3"] and "i2" in clue and "i3" in clue:
                critical += [(clue["K2"], clue["i2"], clue["K3"], clue["i3"])]
        else:
            # crucial lines
            critical += self.get_critical_squares_from_line(clue, "1", "1", "6")
            critical += self.get_critical_squares_from_line(clue, "2", "2", "6")
            critical += self.get_critical_squares_from_line(clue, "3", "3", "6")
            # intersections
            critical += self.get_critical_squares_from_between(clue, "1", "1", "2", "2")
            critical += self.get_critical_squares_from_between(clue, "1", "1", "3", "3")
            critical += self.get_critical_squares_from_between(clue, "2", "2", "3", "3")

    elif clue["typ"] == 3:
        operation = clue["oper"]
        diff = clue["diff"]
        if self.categories[clue["K6"]]["typ"] == "numerical":
            values = self.categories[clue["K6"]]['names']
        else:
            values = list(range(1, self.k + 1))

        if not everything:
            if clue["K1"] != clue["K2"] and "i1" in clue and "i2" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i2"])]

            if operation == "+":
                for i in range(self.k):
                    if values[i] - diff not in values and "i2" in clue:
                        critical += [(clue["K2"], clue["i2"], clue["K6"], i)]
                    if values[i] + diff not in values and "i1" in clue:
                        critical += [(clue["K1"], clue["i1"], clue["K6"], i)]
            elif operation == "*":
                for i in range(self.k):
                    if values[i] / diff not in values and "i2" in clue:
                        critical += [(clue["K2"], clue["i2"], clue["K6"], i)]
                    if values[i] * diff not in values and "i1" in clue:
                        critical += [(clue["K1"], clue["i1"], clue["K6"], i)]
        else:
            # crucial lines
            critical += self.get_critical_squares_from_line(clue, "1", "1", "6")
            critical += self.get_critical_squares_from_line(clue, "2", "2", "6")
            # intersections
            critical += self.get_critical_squares_from_between(clue, "1", "1", "2", "2")

    elif clue["typ"] == 4:
        if not everything:
            if "i1" in clue and "i2" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i2"])]
            if "i3" in clue and "i4" in clue:
                critical += [(clue["K3"], clue["i3"], clue["K4"], clue["i4"])]
            if "i5" in clue and "i6" in clue:
                critical += [(clue["K5"], clue["i5"], clue["K6"], clue["i6"])]

            if clue["K3"] == clue["K5"] and clue["K4"] == clue["K6"] \
                    and "i3" in clue and "i4" in clue and "i5" in clue and "i6" in clue:
                if clue["i3"] != clue["i5"] and clue["i4"] != clue["i6"]:
                    critical += [(clue["K3"], clue["i5"], clue["K4"], clue["i4"])]
                    critical += [(clue["K3"], clue["i3"], clue["K4"], clue["i6"])]
                elif clue["i3"] == clue["i5"]:
                    for i in range(self.k):
                        if i != clue["i4"] and i != clue["i6"]:
                            critical += [(clue["K3"], clue["i3"], clue["K4"], i)]
                else:
                    for i in range(self.k):
                        if i != clue["i3"] and i != clue["i5"]:
                            critical += [(clue["K3"], i, clue["K4"], clue["i4"])]
        else:
            critical += self.get_critical_squares_from_between(clue, "1", "1", "2", "2")
            critical += self.get_critical_squares_from_between(clue, "3", "3", "4", "4")
            critical += self.get_critical_squares_from_between(clue, "5", "5", "6", "6")

    elif clue["typ"] == 5:
        if not everything:
            if "i1" in clue and "i2" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i2"])]
            if "i3" in clue and "i4" in clue:
                critical += [(clue["K3"], clue["i3"], clue["K4"], clue["i4"])]

            if clue["K1"] == clue["K3"] and clue["K2"] == clue["K4"] \
                    and "i1" in clue and "i2" in clue and "i3" in clue and "i4" in clue:
                if clue["i1"] != clue["i3"] and clue["i2"] != clue["i4"]:
                    critical += [(clue["K1"], clue["i3"], clue["K2"], clue["i2"])]
                    critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i4"])]
                elif clue["i1"] == clue["i3"]:
                    for i in range(self.k):
                        if i != clue["i2"] and i != clue["i4"]:
                            critical += [(clue["K1"], clue["i1"], clue["K2"], i)]
                else:
                    for i in range(self.k):
                        if i != clue["i1"] and i != clue["i3"]:
                            critical += [(clue["K1"], i, clue["K2"], clue["i2"])]
        else:
            critical += self.get_critical_squares_from_between(clue, "1", "1", "2", "2")
            critical += self.get_critical_squares_from_between(clue, "3", "3", "4", "4")

    elif clue["typ"] == 6:
        if not everything:
            if clue["K1"] != clue["K2"] and "i1" in clue and "i2" in clue:
                critical += [(clue["K1"], clue["i1"], clue["K2"], clue["i2"])]
        else:
            critical += self.get_critical_squares_from_between(clue, "1", "1", "2", "2")
            critical += self.get_critical_squares_from_line(clue, "1", "1", "6")
            critical += self.get_critical_squares_from_line(clue, "2", "2", "6")

    return critical


def is_forbidden(self, clue_cand):
    """
    This function tests if a candidate for a clue has at least one critical square that is occupied already.
    Also detects too nested clues of type 2 or 3(only if k is small, otherwise nested clues 2 and 3 are allowed).
    """

    # checking if critical squares do not repeat
    critical1 = self.get_critical_squares(clue_cand)
    for clue_i, clue in enumerate(self.clues):
        critical2 = self.get_critical_squares(clue)
        for s1 in critical1:
            for s2 in critical2:
                if s1[0] == s2[0] and s1[1] == s2[1] and s1[2] == s2[2] and s1[3] == s2[3]:
                    return True
                if s1[0] == s2[2] and s1[1] == s2[3] and s1[2] == s2[0] and s1[3] == s2[1]:
                    return True

    if clue_cand["typ"] == 2 and self.k < 6:
        # checking if clue of type 2 do not solve any clue of type 2 immediately 
        for clue in [c for c in self.clues if c["typ"] == 2]:
            if clue["K6"] == clue_cand["K6"]:
                if "g1" not in clue and "g3" not in clue_cand:
                    if clue["K1"] == clue_cand["K3"] and clue["i1"] == clue_cand["i3"]:
                        return True
                if "g3" not in clue and "g1" not in clue_cand:
                    if clue["K3"] == clue_cand["K1"] and clue["i3"] == clue_cand["i1"]:
                        return True
                if self.k < 5:
                    if clue["K2"] == clue_cand["K3"] and "i2" in clue \
                            and "i3" in clue_cand and clue["i2"] == clue_cand["i3"]:
                        return True
                    if clue["K2"] == clue_cand["K1"] and "i2" in clue \
                            and "i1" in clue_cand and clue["i2"] == clue_cand["i1"]:
                        return True
                    if clue["K3"] == clue_cand["K2"] and "i3" in clue \
                            and "i2" in clue_cand and clue["i3"] == clue_cand["i2"]:
                        return True
                    if clue["K1"] == clue_cand["K2"] and "i1" in clue \
                            and "i2" in clue_cand and clue["i1"] == clue_cand["i2"]:
                        return True
        if self.k < 5:
            for clue in [c for c in self.clues if c["typ"] == 3]:
                if clue["K6"] == clue_cand["K6"]:
                    if clue["K1"] == clue_cand["K1"] and "i1" in clue \
                            and "i1" in clue_cand and clue["i1"] == clue_cand["i1"]:
                        return True
                    if clue["K2"] == clue_cand["K2"] and "i2" in clue \
                            and "i2" in clue_cand and clue["i2"] == clue_cand["i2"]:
                        return True
    elif clue_cand["typ"] == 3 and self.k < 5:
        # checking if clue of type 3 do not solve any clue of type 2 immediately 
        # assuming only one 'X' for either of two objects in clue 3
        for clue in [c for c in self.clues if c["typ"] == 2]:
            if clue["K6"] == clue_cand["K6"]:
                if clue["K1"] == clue_cand["K1"] and "i1" in clue \
                        and "i1" in clue_cand and clue["i1"] == clue_cand["i1"]:
                    return True
                if clue["K3"] == clue_cand["K2"] and "i3" in clue \
                        and "i2" in clue_cand and clue["i3"] == clue_cand["i2"]:
                    return True

    # checking if clue of type 2/3 do not solve any clue of type 2/3 immediately 
    # done via critical squares(taking into the account many 'X's for either of two objects in clue 3)
    if clue_cand["typ"] == 3 and self.k > 3:
        for clue in [c for c in self.clues if c["typ"] == 2]:
            if clue["K6"] == clue_cand["K6"]:
                if clue["K3"] == clue_cand["K2"] and "i3" in clue \
                        and "i2" in clue_cand and clue["i3"] == clue_cand["i2"]:
                    critical_sum = 0
                    critical1 = self.get_critical_squares(clue_cand)
                    critical2 = self.get_critical_squares(clue)
                    critical_list = critical1 + critical2
                    if "i3" in clue:
                        for i in range(self.k):
                            if (clue["K3"], clue["i3"], clue["K6"], i) in critical_list or (
                                    clue["K6"], i, clue["K3"], clue["i3"]) in critical_list:
                                critical_sum += 1
                        if critical_sum >= self.k - 1:
                            return True
                elif clue["K1"] == clue_cand["K1"] and "i1" in clue and "i1" in clue_cand and clue["i1"] == clue_cand[
                    "i1"]:
                    critical_sum = 0
                    critical1 = self.get_critical_squares(clue_cand)
                    critical2 = self.get_critical_squares(clue)
                    critical_list = critical1 + critical2
                    if "i1" in clue:
                        for i in range(self.k):
                            if (clue["K1"], clue["i1"], clue["K6"], i) in critical_list or (
                                    clue["K6"], i, clue["K1"], clue["i1"]) in critical_list:
                                critical_sum += 1
                        if critical_sum >= self.k - 1:
                            return True
    elif clue_cand["typ"] == 2 and self.k > 3:
        for clue in [c for c in self.clues if c["typ"] == 3]:
            if clue["K6"] == clue_cand["K6"]:
                if clue_cand["K3"] == clue["K2"] and "i3" in clue \
                        and "i2" in clue_cand and clue_cand["i3"] == clue["i2"]:
                    critical_sum = 0
                    critical1 = self.get_critical_squares(clue_cand)
                    critical2 = self.get_critical_squares(clue)
                    critical_list = critical1 + critical2
                    if "i2" in clue:
                        for i in range(self.k):
                            if (clue["K2"], clue["i2"], clue["K6"], i) in critical_list or (
                                    clue["K6"], i, clue["K2"], clue["i2"]) in critical_list:
                                critical_sum += 1
                        if critical_sum >= self.k - 1:
                            return True
                elif clue["K1"] == clue_cand["K1"] and "i1" in clue and "i1" in clue_cand and clue["i1"] == clue_cand[
                    "i1"]:
                    critical_sum = 0
                    critical1 = self.get_critical_squares(clue_cand)
                    critical2 = self.get_critical_squares(clue)
                    critical_list = critical1 + critical2
                    if "i1" in clue:
                        for i in range(self.k):
                            if (clue["K1"], clue["i1"], clue["K6"], i) in critical_list or (
                                    clue["K6"], i, clue["K1"], clue["i1"]) in critical_list:
                                critical_sum += 1
                        if critical_sum >= self.k - 1:
                            return True
    return False


def propose_clue1_cand(self, clue_cand):
    """
    Function with probability prob_of_group changes some of the objects in clue of type 1 into gropus 
    (only if there are actually groups in this category).
    """
    prob_of_group = 0.2

    if "groups" in self.categories[clue_cand["K1"]] and "i3" not in clue_cand and len(
            unique(self.categories[clue_cand["K1"]]["groups"])) != 1 and random.uniform(0, 1) < prob_of_group:
        cnt = dict(Counter(self.categories[clue_cand["K1"]]["groups"]))
        possible_groups = [k for k in cnt.keys() if
                           cnt[k] < self.k - 1]  # excluding groups that will exclude too much options
        group = random.choice(possible_groups, 1)[0]
        del clue_cand["i1"]
        clue_cand["g1"] = group
    elif "groups" in self.categories[clue_cand["K2"]] and "i3" not in clue_cand and len(
            unique(self.categories[clue_cand["K2"]]["groups"])) != 1 and random.uniform(0, 1) < prob_of_group:
        cnt = dict(Counter(self.categories[clue_cand["K2"]]["groups"]))
        possible_groups = [k for k in cnt.keys() if
                           cnt[k] < self.k - 1]  # excluding groups that will exclude too much options
        group = random.choice(possible_groups, 1)[0]
        del clue_cand["i2"]
        clue_cand["g2"] = group

    return clue_cand


def propose_clue2_cand(self, clue_cand):
    """
    Function with probability prob_of_group changes some of the objects in clue of type 1 into groups
    (only if there are actually groups in this category).
    """
    prob_of_group = 0.2

    order = random.permutation(["1", "2", "3"])
    for i in order:
        if "groups" in self.categories[clue_cand["K" + i]] and len(
                unique(self.categories[clue_cand["K" + i]]["groups"])) != 1 and random.uniform(0, 1) < prob_of_group:
            cnt = dict(Counter(self.categories[clue_cand["K" + i]]["groups"]))
            possible_groups = [k for k in cnt.keys() if cnt[k] > 1]  # excluding groups with only one member
            group = random.choice(possible_groups, 1)[0]
            del clue_cand["i" + i]
            clue_cand["g" + i] = group

    return clue_cand


def propose_clue3_cand(self, clue_cand):
    """
    Function with probability prob_of_group changes some of the objects in clue of type 1 into groups
    (only if there are actually groups in this category).
    """
    prob_of_group = 0.2
    order = random.permutation(["1", "2"])
    for i in order:
        if "groups" in self.categories[clue_cand["K" + i]] and len(
                unique(self.categories[clue_cand["K" + i]]["groups"])) != 1 and random.uniform(0, 1) < prob_of_group:
            cnt = dict(Counter(self.categories[clue_cand["K" + i]]["groups"]))
            possible_groups = [k for k in cnt.keys() if cnt[k] > 1]  # excluding groups with only one member
            group = random.choice(possible_groups, 1)[0]
            del clue_cand["i" + i]
            clue_cand["g" + i] = group

    return clue_cand


def propose_clue4_cand(self, clue_cand):
    """
    Function with probability prob_of_group changes some of the objects in clue of type 1 into groups
    (only if there are actually groups in this category).
    """
    prob_of_group = 0.8
    order = random.permutation(["1", "2", "3", "4", "5", "6"])
    for i in order:
        if "groups" in self.categories[clue_cand["K" + i]] and len(
                unique(self.categories[clue_cand["K" + i]]["groups"])) != 1 and random.uniform(0, 1) < prob_of_group:
            cnt = dict(Counter(self.categories[clue_cand["K" + i]]["groups"]))
            possible_groups = [k for k in cnt.keys() if cnt[k] > 1]  # excluding groups with only one member
            group = random.choice(possible_groups, 1)[0]
            del clue_cand["i" + i]
            clue_cand["g" + i] = group

    return clue_cand


def propose_clue5_cand(self, clue_cand):
    """
    Function with probability prob_of_group changes some of the objects in clue of type 1 into groups
    (only if there are actually groups in this category).
    """
    prob_of_group = 0.8
    order = random.permutation(["1", "2", "3", "4"])
    for i in order:
        if "groups" in self.categories[clue_cand["K" + i]] and len(
                unique(self.categories[clue_cand["K" + i]]["groups"])) != 1 and random.uniform(0, 1) < prob_of_group:
            cnt = dict(Counter(self.categories[clue_cand["K" + i]]["groups"]))
            possible_groups = [k for k in cnt.keys() if cnt[k] > 1]  # excluding groups with only one member
            group = random.choice(possible_groups, 1)[0]
            del clue_cand["i" + i]
            clue_cand["g" + i] = group

    return clue_cand


def propose_clue6_cand(self, clue_cand):
    """
    Function with probability prob_of_group changes some of the objects in clue of type 1 into gropus 
    (only if there are actually groups in this category).
    """
    prob_of_group = 0.2
    order = random.permutation(["1", "2"])
    for i in order:
        if "groups" in self.categories[clue_cand["K" + i]] and len(
                unique(self.categories[clue_cand["K" + i]]["groups"])) != 1 and random.uniform(0, 1) < prob_of_group:
            cnt = dict(Counter(self.categories[clue_cand["K" + i]]["groups"]))
            possible_groups = [k for k in cnt.keys() if cnt[k] > 1]  # excluding groups with only one member
            group = random.choice(possible_groups, 1)[0]
            del clue_cand["i" + i]
            clue_cand["g" + i] = group

    return clue_cand


def add_clue1(self):
    """
    Adding clue of type 1:
    Single/double or triple 'X' in the grid.
    """
    no_of_x = random.choice([1, 2, 3], 1, p=[0.8, 0.15, 0.05])
    K = self.K
    k = self.k
    key_list = random.choice(range(K * (K - 1) // 2), K * (K - 1) // 2, replace=False)
    i_list = random.choice(range(k), k, replace=False)
    j_list = random.choice(range(k), k, replace=False)

    boxes = []
    for key in self.grid:
        boxes.append(key)

    for key in key_list:
        K1 = int(boxes[key].split(",")[0])
        K2 = int(boxes[key].split(",")[1])
        for i in i_list:
            for j in j_list:
                if self.get_grid_value(K1, i, K2, j) == 0:
                    if no_of_x == 1:
                        clue_cand = {"typ": 1, "K1": K1, "i1": i, "K2": K2, "i2": j}
                        clue_cand = propose_clue1_cand(self, clue_cand)
                        if self.is_forbidden(clue_cand):
                            break
                        self.clues.append(clue_cand)
                        return
                    other_i = []
                    other_j = []
                    for i2 in range(k):
                        if self.get_grid_value(K1, i2, K2, j) == 0 and i2 != i:
                            other_i.append(i2)
                    for j2 in range(k):
                        if self.get_grid_value(K1, i, K2, j2) == 0 and j2 != j:
                            other_j.append(j2)
                    if len(other_i) <= no_of_x - 1 and len(other_j) <= no_of_x - 1:
                        clue_cand = {"typ": 1, "K1": K1, "i1": i, "K2": K2, "i2": j}
                        clue_cand = propose_clue1_cand(self, clue_cand)
                        if self.is_forbidden(clue_cand):
                            break
                        self.clues.append(clue_cand)
                        return
                    elif len(other_i) > no_of_x - 1 and len(other_j) > no_of_x - 1:
                        if random.randint(2) == 0:
                            to_fill = random.choice(other_i, no_of_x - 1, replace=False)
                            if no_of_x == 2:
                                clue_cand = {"typ": 1, "K1": K2, "i1": j, "K2": K1, "i2": i, "i3": to_fill[0]}
                                clue_cand = propose_clue1_cand(self, clue_cand)
                                if self.is_forbidden(clue_cand):
                                    break
                                self.clues.append(clue_cand)
                                return
                            else:
                                clue_cand = {"typ": 1, "K1": K2, "i1": j, "K2": K1, "i2": i, "i3": to_fill[0],
                                             "i4": to_fill[1]}
                                clue_cand = propose_clue1_cand(self, clue_cand)
                                if self.is_forbidden(clue_cand):
                                    break
                                self.clues.append(clue_cand)
                                return
                        else:
                            to_fill = random.choice(other_j, no_of_x - 1, replace=False)
                            if no_of_x == 2:
                                clue_cand = {"typ": 1, "K1": K1, "i1": i, "K2": K2, "i2": j, "i3": to_fill[0]}
                                clue_cand = propose_clue1_cand(self, clue_cand)
                                if self.is_forbidden(clue_cand):
                                    break
                                self.clues.append(clue_cand)
                                return
                            else:
                                clue_cand = {"typ": 1, "K1": K1, "i1": i, "K2": K2, "i2": j, "i3": to_fill[0],
                                             "i4": to_fill[1]}
                                clue_cand = propose_clue1_cand(self, clue_cand)
                                if self.is_forbidden(clue_cand):
                                    break
                                self.clues.append(clue_cand)
                                return
                    elif len(other_i) > no_of_x - 1:
                        to_fill = random.choice(other_i, no_of_x - 1, replace=False)
                        if no_of_x == 2:
                            clue_cand = {"typ": 1, "K1": K2, "i1": j, "K2": K1, "i2": i, "i3": to_fill[0]}
                            clue_cand = propose_clue1_cand(self, clue_cand)
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                        else:
                            clue_cand = {"typ": 1, "K1": K2, "i1": j, "K2": K1, "i2": i, "i3": to_fill[0],
                                         "i4": to_fill[1]}
                            clue_cand = propose_clue1_cand(self, clue_cand)
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                    else:
                        to_fill = random.choice(other_j, no_of_x - 1, replace=False)
                        if no_of_x == 2:
                            clue_cand = {"typ": 1, "K1": K1, "i1": i, "K2": K2, "i2": j, "i3": to_fill[0]}
                            clue_cand = propose_clue1_cand(self, clue_cand)
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                        else:
                            clue_cand = {"typ": 1, "K1": K1, "i1": i, "K2": K2, "i2": j, "i3": to_fill[0],
                                         "i4": to_fill[1]}
                            clue_cand = propose_clue1_cand(self, clue_cand)
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

    K6_candidates = [i for i, cat in enumerate(self.categories) if cat['typ'] in ['numerical', 'ordinal']]
    K6 = random.choice(K6_candidates, 1)[0]

    i_candidates = [i for i in range(K * k) if i // k != K6]
    i1_list = random.choice(i_candidates, len(i_candidates), replace=False)
    i2_list = random.choice(i_candidates, len(i_candidates), replace=False)
    i3_list = random.choice(i_candidates, len(i_candidates), replace=False)

    for i1p in i1_list:
        for i2p in i2_list:
            for i3p in i3_list:
                if i1p != i2p and i1p != i3p and i2p != i3p:
                    K1 = i1p // k
                    i1 = i1p % k
                    K2 = i2p // k
                    i2 = i2p % k
                    K3 = i3p // k
                    i3 = i3p % k
                    val0 = self.get_grid_value(K1, i1, K6, 0)
                    val1 = self.get_grid_value(K1, i1, K6, 1)
                    val2 = self.get_grid_value(K2, i2, K6, 0)
                    val3 = self.get_grid_value(K2, i2, K6, k - 1)
                    val4 = self.get_grid_value(K3, i3, K6, k - 2)
                    val5 = self.get_grid_value(K3, i3, K6, k - 1)

                    values = [val0, val1, val2, val3, val4, val5]

                    if K1 != K2:
                        values.append(self.get_grid_value(K1, i1, K2, i2))
                    if K1 != K3:
                        values.append(self.get_grid_value(K1, i1, K3, i3))
                    if K2 != K3:
                        values.append(self.get_grid_value(K2, i2, K3, i3))

                    if any([val == 1 for val in values]):
                        break
                    sum_of_free = sum([val == 0 for val in values])
                    if sum_of_free > 5:
                        clue_cand = {"typ": 2, "K1": K1, "i1": i1, "K2": K2, "i2": i2, "K3": K3, "i3": i3, "K6": K6}
                        clue_cand = propose_clue2_cand(self, clue_cand)
                        if self.is_forbidden(clue_cand):
                            break
                        self.clues.append(clue_cand)
                        return


def add_clue3(self):
    """
    Adding clue of type 3:
    With respect to the Category K6 (numerical) we have 'K2,i2 = K1,i1 oper diff'.
    oper is one of {+, *}.
    """
    K = self.K
    k = self.k

    K6_candidates = [i for i, cat in enumerate(self.categories) if "pre_clues" in cat and len(cat["pre_clues"]) > 0]
    K6 = random.choice(K6_candidates, 1)[0]
    if self.categories[K6]["typ"] == "numerical":
        values = self.categories[K6]['names']
    else:
        values = list(range(1, self.k + 1))

    possible_randomized = random.permutation(list(self.categories[K6]['pre_clues']))
    diff_list = [float(diff_string.split("y")[-1][1:]) for diff_string in possible_randomized]
    operations = [diff_string.split("y")[-1][0] for diff_string in possible_randomized]

    i_candidates = [i for i in range(K * k) if i // k != K6]
    i1_list = random.permutation(i_candidates)
    i2_list = random.permutation(i_candidates)

    for i1p in i1_list:
        for i2p in i2_list:
            for diff, operation in zip(diff_list, operations):
                if i1p != i2p:
                    K1 = i1p // k
                    i1 = i1p % k
                    K2 = i2p // k
                    i2 = i2p % k
                    if operation == "+":
                        vals_for_X = []
                        for i in range(k):
                            if values[i] - diff not in values:
                                vals_for_X.append(self.get_grid_value(K2, i2, K6, i))
                            if values[i] + diff not in values:
                                vals_for_X.append(self.get_grid_value(K1, i1, K6, i))
                        if K1 != K2:
                            vals_for_X.append(self.get_grid_value(K1, i1, K2, i2))
                        if any([val == 1 for val in vals_for_X]):
                            break
                        sum_of_free = sum([val == 0 for val in vals_for_X])
                        if sum_of_free > 1:
                            clue_cand = {"typ": 3, "K1": K1, "i1": i1, "K2": K2, "i2": i2, "K6": K6, "diff": diff,
                                         "oper": operation}
                            clue_cand = propose_clue3_cand(self, clue_cand)
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                    elif operation == "*":
                        vals_for_X = []
                        for i in range(k):
                            if round(values[i] / diff, 12) not in values:
                                vals_for_X.append(self.get_grid_value(K2, i2, K6, i))
                            if round(values[i] * diff, 12) not in values:
                                vals_for_X.append(self.get_grid_value(K1, i1, K6, i))
                        if K1 != K2:
                            vals_for_X.append(self.get_grid_value(K1, i1, K2, i2))
                        if any([val == 1 for val in vals_for_X]):
                            break
                        sum_of_free = sum([val == 0 for val in vals_for_X])
                        if sum_of_free > 1:
                            clue_cand = {"typ": 3, "K1": K1, "i1": i1, "K2": K2, "i2": i2, "K6": K6, "diff": diff,
                                         "oper": operation}
                            clue_cand = propose_clue3_cand(self, clue_cand)
                            if self.is_forbidden(clue_cand):
                                break
                            self.clues.append(clue_cand)
                            return
                    else:
                        raise Exception("Unknown operation type: " + operation + "!")


def add_clue4(self):
    """
    Adding clue of type 4:
    If K1,i1 match K2,i2 then K3,i3 match K4,i4 otherwise K5,i5 match K6,i6.
    """
    K = self.K
    k = self.k

    K12_candidates = random.permutation([key for key in self.grid])
    K34_candidates = random.permutation([key for key in self.grid])
    K56_candidates = random.permutation([key for key in self.grid])

    i_candidates = [i for i in range(k)]
    i1_list = random.permutation(i_candidates)
    i2_list = random.permutation(i_candidates)
    i3_list = random.permutation(i_candidates)
    i4_list = random.permutation(i_candidates)
    i5_list = random.permutation(i_candidates)
    i6_list = random.permutation(i_candidates)

    for K12 in K12_candidates:
        for K34 in K34_candidates:
            if K34 != K12:
                los = random.randint(2)
                if los == 0:
                    K56 = K34
                else:
                    for Kxy in K56_candidates:
                        if Kxy != K34 and Kxy != K12:
                            K56 = Kxy
                for i1 in i1_list:
                    for i2 in i2_list:
                        for i3 in i3_list:
                            for i4 in i4_list:
                                for i5 in i5_list:
                                    for i6 in i6_list:
                                        if K34 == K56 and i3 == i5 and i4 == i6:
                                            pass
                                        else:
                                            K1 = int(K12.split(",")[0])
                                            K2 = int(K12.split(",")[1])
                                            K3 = int(K34.split(",")[0])
                                            K4 = int(K34.split(",")[1])
                                            K5 = int(K56.split(",")[0])
                                            K6 = int(K56.split(",")[1])

                                            if self.get_grid_value(K1, i1, K2, i2) == 0 and self.get_grid_value(K3, i3,
                                                                                                                K4,
                                                                                                                i4) == 0 and self.get_grid_value(
                                                K5, i5, K6, i6) == 0:
                                                if K34 == K56:
                                                    vals_for_X = []
                                                    if i3 != i5 and i4 != i6:
                                                        vals_for_X.append(self.get_grid_value(K3, i5, K4, i4))
                                                        vals_for_X.append(self.get_grid_value(K3, i3, K4, i6))
                                                    elif i3 == i5:
                                                        for i in range(k):
                                                            if i != i4 and i != i6:
                                                                vals_for_X.append(self.get_grid_value(K3, i3, K4, i))
                                                    else:
                                                        for i in range(k):
                                                            if i != i3 and i != i5:
                                                                vals_for_X.append(self.get_grid_value(K3, i, K4, i4))

                                                    if any([val == 1 for val in vals_for_X]):
                                                        break
                                                    sum_of_free = sum([val == 0 for val in vals_for_X])
                                                    if sum_of_free > 1:
                                                        clue_cand = {"typ": 4, "K1": K1, "i1": i1, "K2": K2, "i2": i2,
                                                                     "K3": K3, "i3": i3, "K4": K4, "i4": i4, "K5": K5,
                                                                     "i5": i5, "K6": K6, "i6": i6}
                                                        clue_cand = propose_clue4_cand(self, clue_cand)
                                                        if self.is_forbidden(clue_cand):
                                                            break
                                                        self.clues.append(clue_cand)
                                                        return
                                                else:
                                                    clue_cand = {"typ": 4, "K1": K1, "i1": i1, "K2": K2, "i2": i2,
                                                                 "K3": K3, "i3": i3, "K4": K4, "i4": i4, "K5": K5,
                                                                 "i5": i5, "K6": K6, "i6": i6}
                                                    clue_cand = propose_clue4_cand(self, clue_cand)
                                                    if self.is_forbidden(clue_cand):
                                                        break
                                                    self.clues.append(clue_cand)
                                                    return


def add_clue5(self):
    """
    Adding clue of type 5:
    Either K1,i1 match K2,i2 or K3,i3 match K4,i4.
    If 'exclusive==True' 'exclusive or' is assumed, normal 'or' otherwise.
    """
    los = random.randint(2)
    if los == 1:
        exclusive = True
    else:
        exclusive = False

    K = self.K
    k = self.k

    K12_candidates = random.permutation([key for key in self.grid])
    K34_candidates = random.permutation([key for key in self.grid])

    i_candidates = [i for i in range(k)]
    i1_list = random.permutation(i_candidates)
    i2_list = random.permutation(i_candidates)
    i3_list = random.permutation(i_candidates)
    i4_list = random.permutation(i_candidates)

    for K12 in K12_candidates:
        los = random.randint(2)
        if los == 0:
            K34 = K12
        else:
            for Kxy in K34_candidates:
                if Kxy != K12:
                    K34 = Kxy

        for i1 in i1_list:
            for i2 in i2_list:
                for i3 in i3_list:
                    for i4 in i4_list:
                        if K12 == K34 and (i1 == i3 or i2 == i4):
                            pass
                        else:
                            K1 = int(K12.split(",")[0])
                            K2 = int(K12.split(",")[1])
                            K3 = int(K34.split(",")[0])
                            K4 = int(K34.split(",")[1])
                            if self.get_grid_value(K1, i1, K2, i2) == 0 and self.get_grid_value(K3, i3, K4, i4) == 0:
                                if K12 == K34:
                                    vals_for_X = []
                                    if i1 != i3 and i2 != i4:
                                        vals_for_X.append(self.get_grid_value(K1, i1, K2, i4))
                                        vals_for_X.append(self.get_grid_value(K1, i3, K2, i2))
                                    elif i1 == i3:
                                        for i in range(k):
                                            if i != i2 and i != i4:
                                                vals_for_X.append(self.get_grid_value(K1, i1, K2, i))
                                    else:
                                        for i in range(k):
                                            if i != i1 and i != i3:
                                                vals_for_X.append(self.get_grid_value(K1, i, K2, i2))

                                    if any([val == 1 for val in vals_for_X]):
                                        break
                                    sum_of_free = sum([val == 0 for val in vals_for_X])
                                    if sum_of_free > 1:
                                        clue_cand = {"typ": 5, "K1": K1, "i1": i1, "K2": K2, "i2": i2, "K3": K3,
                                                     "i3": i3, "K4": K4, "i4": i4, "exclusive": exclusive}
                                        clue_cand = propose_clue5_cand(self, clue_cand)
                                        if self.is_forbidden(clue_cand):
                                            break
                                        self.clues.append(clue_cand)
                                        return
                                else:
                                    clue_cand = {"typ": 5, "K1": K1, "i1": i1, "K2": K2, "i2": i2, "K3": K3, "i3": i3,
                                                 "K4": K4, "i4": i4, "exclusive": exclusive}
                                    clue_cand = propose_clue5_cand(self, clue_cand)
                                    if self.is_forbidden(clue_cand):
                                        break
                                    self.clues.append(clue_cand)
                                    return


def add_clue6(self):
    """
    Adding clue of type 6:
    With respect to the Category K6(numerical or ordinal) K1,i1 is right next to K2,i2.
    """
    K = self.K
    k = self.k

    K6_candidates = [i for i, cat in enumerate(self.categories) if cat['typ'] in ['numerical', 'ordinal']]
    K6 = random.choice(K6_candidates, 1)[0]

    i_candidates = [i for i in range(K * k) if i // k != K6]
    i1_list = random.choice(i_candidates, len(i_candidates), replace=False)
    i2_list = random.choice(i_candidates, len(i_candidates), replace=False)

    for i1p in i1_list:
        for i2p in i2_list:
            if i1p != i2p:
                K1 = i1p // k
                i1 = i1p % k
                K2 = i2p // k
                i2 = i2p % k
                possible_pairs = 0
                for i in range(k):
                    if i != 0 and self.get_grid_value(K1, i1, K6, i) == 0 and self.get_grid_value(K2, i2, K6,
                                                                                                  i - 1) == 0:
                        possible_pairs += 1
                    if i != k - 1 and self.get_grid_value(K1, i1, K6, i) == 0 and self.get_grid_value(K2, i2, K6,
                                                                                                      i + 1) == 0:
                        possible_pairs += 1
                if possible_pairs > k - 1:
                    clue_cand = {"typ": 6, "K1": K1, "i1": i1, "K2": K2, "i2": i2, "K6": K6}
                    clue_cand = propose_clue6_cand(self, clue_cand)
                    if self.is_forbidden(clue_cand):
                        break
                    self.clues.append(clue_cand)
                    return


def use_clue1(self, c, collect_solution=False):
    clue = self.clues[c]
    if "g1" not in clue and "g2" not in clue:  # with no groups
        self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i2"], "X", "clue1_" + str(c), collect_solution)
        if "i3" in clue:
            self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i3"], "X", "clue1_" + str(c), collect_solution)
            if "i4" in clue:
                self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i4"], "X", "clue1_" + str(c),
                                 collect_solution)
    else:  # with groups
        if "g1" in clue:
            for i in range(self.k):
                if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                    self.grid_insert(clue["K1"], i, clue["K2"], clue["i2"], "X", "clue1_" + str(c), collect_solution)
        if "g2" in clue:
            for i in range(self.k):
                if self.categories[clue["K2"]]["groups"][i] == clue["g2"]:
                    self.grid_insert(clue["K1"], clue["i1"], clue["K2"], i, "X", "clue1_" + str(c), collect_solution)


def use_clue2(self, c, collect_solution=False):
    clue = self.clues[c]
    if "i1" in clue:
        self.grid_insert(clue["K1"], clue["i1"], clue["K6"], 0, "X", "clue2_" + str(c), collect_solution)
        self.grid_insert(clue["K1"], clue["i1"], clue["K6"], 1, "X", "clue2_" + str(c), collect_solution)
    if "i2" in clue:
        self.grid_insert(clue["K2"], clue["i2"], clue["K6"], 0, "X", "clue2_" + str(c), collect_solution)
        self.grid_insert(clue["K2"], clue["i2"], clue["K6"], self.k - 1, "X", "clue2_" + str(c), collect_solution)
    if "i3" in clue:
        self.grid_insert(clue["K3"], clue["i3"], clue["K6"], self.k - 2, "X", "clue2_" + str(c), collect_solution)
        self.grid_insert(clue["K3"], clue["i3"], clue["K6"], self.k - 1, "X", "clue2_" + str(c), collect_solution)

    if clue["K1"] != clue["K2"] and "i1" in clue and "i2" in clue:
        self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i2"], "X", "clue2_" + str(c), collect_solution)
    if clue["K1"] != clue["K3"] and "i1" in clue and "i3" in clue:
        self.grid_insert(clue["K1"], clue["i1"], clue["K3"], clue["i3"], "X", "clue2_" + str(c), collect_solution)
    if clue["K2"] != clue["K3"] and "i2" in clue and "i3" in clue:
        self.grid_insert(clue["K2"], clue["i2"], clue["K3"], clue["i3"], "X", "clue2_" + str(c), collect_solution)

    if "i3" in clue:
        for j in range(self.k - 2):
            if self.get_grid_value(clue["K3"], clue["i3"], clue["K6"], j) == 2:
                if "i2" in clue:
                    self.grid_insert(clue["K2"], clue["i2"], clue["K6"], j + 1, "X", "clue2_" + str(c),
                                     collect_solution)
                if "i1" in clue:
                    self.grid_insert(clue["K1"], clue["i1"], clue["K6"], j + 2, "X", "clue2_" + str(c),
                                     collect_solution)
            else:
                break
    if "i2" in clue:
        for j in range(self.k - 1):
            if self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], j) == 2:
                if "i1" in clue:
                    self.grid_insert(clue["K1"], clue["i1"], clue["K6"], j + 1, "X", "clue2_" + str(c),
                                     collect_solution)
            else:
                break

    if "i1" in clue:
        for j in range(self.k - 2):
            if self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], self.k - j - 1) == 2:
                if "i2" in clue:
                    self.grid_insert(clue["K2"], clue["i2"], clue["K6"], self.k - j - 2, "X", "clue2_" + str(c),
                                     collect_solution)
                if "i3" in clue:
                    self.grid_insert(clue["K3"], clue["i3"], clue["K6"], self.k - j - 3, "X", "clue2_" + str(c),
                                     collect_solution)
            else:
                break

    if "i2" in clue:
        for j in range(self.k - 1):
            if self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], self.k - j - 1) == 2:
                if "i3" in clue:
                    self.grid_insert(clue["K3"], clue["i3"], clue["K6"], self.k - j - 2, "X", "clue2_" + str(c),
                                     collect_solution)
            else:
                break


def use_clue3(self, c, collect_solution=False):
    clue = self.clues[c]
    operation = clue["oper"]
    diff = clue["diff"]
    if self.categories[clue["K6"]]["typ"] == "numerical":
        values = self.categories[clue["K6"]]['names']
    else:
        values = list(range(1, self.k + 1))

    if clue["K1"] != clue["K2"] and "i1" in clue and "i2" in clue:
        self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i2"], "X", "clue3_" + str(c), collect_solution)

    if operation == "+":
        if "i1" in clue:
            if "i2" in clue:
                for i in range(self.k):
                    if values[i] - diff not in values or self.get_grid_value(clue["K1"], clue["i1"], clue["K6"],
                                                                             values.index(values[i] - diff)) == 2:
                        self.grid_insert(clue["K2"], clue["i2"], clue["K6"], i, "X", "clue3_" + str(c),
                                         collect_solution)
            else:
                for i in range(self.k):
                    if values[i] + diff not in values:
                        self.grid_insert(clue["K1"], clue["i1"], clue["K6"], i, "X", "clue3_" + str(c),
                                         collect_solution)
                # if K1,i1 is already determined we can put some 'X's outside group K2,g2:
                for i in range(self.k):
                    if self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], i) == 1 and values[i] + diff in values:
                        i6 = values.index(values[i] + diff)
                        for j in range(self.k):
                            if self.categories[clue["K2"]]["groups"][j] != clue["g2"]:
                                self.grid_insert(clue["K2"], j, clue["K6"], i6, "X", "clue3_" + str(c),
                                                 collect_solution)
                        break
        if "i2" in clue:
            if "i1" in clue:
                for i in range(self.k):
                    if values[i] + diff not in values or self.get_grid_value(clue["K2"], clue["i2"], clue["K6"],
                                                                             values.index(values[i] + diff)) == 2:
                        self.grid_insert(clue["K1"], clue["i1"], clue["K6"], i, "X", "clue3_" + str(c),
                                         collect_solution)
            else:
                for i in range(self.k):
                    if values[i] - diff not in values:
                        self.grid_insert(clue["K2"], clue["i2"], clue["K6"], i, "X", "clue3_" + str(c),
                                         collect_solution)
                # if K1,i1 is already determined we can put some 'X's outside group K2,g2:
                for i in range(self.k):
                    if self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], i) == 1 and values[i] - diff in values:
                        i6 = values.index(values[i] - diff)
                        for j in range(self.k):
                            if self.categories[clue["K1"]]["groups"][j] != clue["g1"]:
                                self.grid_insert(clue["K1"], j, clue["K6"], i6, "X", "clue3_" + str(c),
                                                 collect_solution)
                        break
    elif operation == "*":
        if "i1" in clue:
            if "i2" in clue:
                for i in range(self.k):
                    if round(values[i] / diff, 12) not in values or self.get_grid_value(clue["K1"], clue["i1"],
                                                                                        clue["K6"], values.index(
                                values[i] / diff)) == 2:
                        self.grid_insert(clue["K2"], clue["i2"], clue["K6"], i, "X", "clue3_" + str(c),
                                         collect_solution)
            else:
                for i in range(self.k):
                    if round(values[i] * diff, 12) not in values:
                        self.grid_insert(clue["K1"], clue["i1"], clue["K6"], i, "X", "clue3_" + str(c),
                                         collect_solution)
                # if K1,i1 is already determined we can put some 'X's outside group K2,g2:
                for i in range(self.k):
                    if self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], i) == 1 and round(values[i] * diff,
                                                                                                 12) in values:
                        i6 = values.index(round(values[i] * diff, 12))
                        for j in range(self.k):
                            if self.categories[clue["K2"]]["groups"][j] != clue["g2"]:
                                self.grid_insert(clue["K2"], j, clue["K6"], i6, "X", "clue3_" + str(c),
                                                 collect_solution)
                        break
        if "i2" in clue:
            if "i1" in clue:
                for i in range(self.k):
                    if round(values[i] * diff, 12) not in values or self.get_grid_value(clue["K2"], clue["i2"],
                                                                                        clue["K6"], values.index(
                                values[i] * diff)) == 2:
                        self.grid_insert(clue["K1"], clue["i1"], clue["K6"], i, "X", "clue3_" + str(c),
                                         collect_solution)
            else:
                for i in range(self.k):
                    if round(values[i] / diff, 12) not in values:
                        self.grid_insert(clue["K2"], clue["i2"], clue["K6"], i, "X", "clue3_" + str(c),
                                         collect_solution)
                # if K1,i1 is already determined we can put some 'X's outside group K2,g2:
                for i in range(self.k):
                    if self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], i) == 1 and round(values[i] / diff,
                                                                                                 12) in values:
                        i6 = values.index(round(values[i] / diff, 12))
                        for j in range(self.k):
                            if self.categories[clue["K1"]]["groups"][j] != clue["g1"]:
                                self.grid_insert(clue["K1"], j, clue["K6"], i6, "X", "clue3_" + str(c),
                                                 collect_solution)
                        break


def use_clue4(self, c, collect_solution=False):
    clue = self.clues[c]

    K1 = clue["K1"]
    K2 = clue["K2"]
    K3 = clue["K3"]
    K4 = clue["K4"]
    K5 = clue["K5"]
    K6 = clue["K6"]

    if K3 == K5 and K4 == K6:
        if "i3" in clue and "i4" in clue and "i5" in clue and "i6" in clue:
            i3 = clue["i3"]
            i4 = clue["i4"]
            i5 = clue["i5"]
            i6 = clue["i6"]
            if i3 != i5 and i4 != i6:
                self.grid_insert(K3, i5, K4, i4, "X", "clue4_" + str(c), collect_solution)
                self.grid_insert(K3, i3, K4, i6, "X", "clue4_" + str(c), collect_solution)
            elif i3 == i5:
                for i in range(self.k):
                    if i != i4 and i != i6:
                        self.grid_insert(K3, i3, K4, i, "X", "clue4_" + str(c), collect_solution)
            else:
                for i in range(self.k):
                    if i != i3 and i != i5:
                        self.grid_insert(K3, i, K4, i4, "X", "clue4_" + str(c), collect_solution)

    # condition12: premise is false
    if "i1" in clue and "i2" in clue:
        condition12 = self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 2
    elif "i1" in clue:
        condition12 = not self.is_line_possible_for_group(clue["K1"], clue["i1"], clue["K2"], clue["g2"])
    elif "i2" in clue:
        condition12 = not self.is_line_possible_for_group(clue["K2"], clue["i2"], clue["K1"], clue["g1"])
    else:  # if both are group type
        condition12 = True
        for i in range(self.k):
            if self.categories[clue["K2"]]["groups"][i] == clue["g2"] and self.is_line_possible_for_group(clue["K1"],
                                                                                                          clue["g1"],
                                                                                                          clue["K2"],
                                                                                                          i):
                condition12 = False
                break

    # condition12anti: premise is true
    if "i1" in clue and "i2" in clue:
        condition12anti = self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 1
    elif "i1" in clue:
        condition12anti = False
        for i in range(self.k):
            if self.categories[clue["K2"]]["groups"][i] == clue["g2"]:
                if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], i) == 1:
                    condition12anti = True
                    break
    elif "i2" in clue:
        condition12anti = False
        for i in range(self.k):
            if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                if self.get_grid_value(clue["K2"], clue["i2"], clue["K1"], i) == 1:
                    condition12anti = True
                    break
    else:  # both are group type
        condition12anti = False
        for i in range(self.k):
            if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                for j in range(self.k):
                    if self.categories[clue["K2"]]["groups"][j] == clue["g2"]:
                        if self.get_grid_value(clue["K1"], i, clue["K2"], j) == 1:
                            condition12anti = True
                            break

    # condition34: positive conclusion is false
    if "i3" in clue and "i4" in clue:
        condition34 = self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"]) == 2
    elif "i3" in clue:
        condition34 = not self.is_line_possible_for_group(clue["K3"], clue["i3"], clue["K4"], clue["g4"])
    elif "i4" in clue:
        condition34 = not self.is_line_possible_for_group(clue["K4"], clue["i4"], clue["K3"], clue["g3"])
    else:  # both are group type
        condition34 = True
        for i in range(self.k):
            if self.categories[clue["K4"]]["groups"][i] == clue["g4"] and self.is_line_possible_for_group(clue["K3"],
                                                                                                          clue["g3"],
                                                                                                          clue["K4"],
                                                                                                          i):
                condition34 = False
                break

    # condition56: negative conclusion is false
    if "i5" in clue and "i6" in clue:
        condition56 = self.get_grid_value(clue["K5"], clue["i5"], clue["K6"], clue["i6"]) == 2
    elif "i5" in clue:
        condition56 = not self.is_line_possible_for_group(clue["K5"], clue["i5"], clue["K6"], clue["g6"])
    elif "i6" in clue:
        condition56 = not self.is_line_possible_for_group(clue["K6"], clue["i6"], clue["K5"], clue["g5"])
    else:  # both are group type
        condition56 = True
        for i in range(self.k):
            if self.categories[clue["K6"]]["groups"][i] == clue["g6"] and self.is_line_possible_for_group(clue["K5"],
                                                                                                          clue["g5"],
                                                                                                          clue["K6"],
                                                                                                          i):
                condition56 = False
                break

    # if positive conclusion is false:
    if condition34 and "i1" in clue and "i2" in clue:
        self.grid_insert(K1, clue["i1"], K2, clue["i2"], "X", "clue4_" + str(c), collect_solution)
    elif condition34 and "i1" in clue:
        for j in range(self.k):
            if self.categories[clue["K2"]]["groups"][j] == clue["g2"]:
                self.grid_insert(K1, clue["i1"], K2, j, "X", "clue4_" + str(c), collect_solution)
    elif condition34 and "i2" in clue:
        for j in range(self.k):
            if self.categories[clue["K1"]]["groups"][j] == clue["g1"]:
                self.grid_insert(K2, clue["i2"], K1, j, "X", "clue4_" + str(c), collect_solution)
    elif condition34:
        for i in range(self.k):
            if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                for j in range(self.k):
                    if self.categories[clue["K2"]]["groups"][j] == clue["g2"]:
                        self.grid_insert(K1, i, K2, j, "X", "clue4_" + str(c), collect_solution)

    if condition34 and "i5" in clue and "i6" in clue:
        self.grid_insert(K5, clue["i5"], K6, clue["i6"], "O", "clue4_" + str(c), collect_solution)
    elif condition34 and "i5" in clue:
        for j in range(self.k):
            if self.categories[clue["K6"]]["groups"][j] != clue["g6"]:
                self.grid_insert(K5, clue["i5"], K6, j, "X", "clue4_" + str(c), collect_solution)
    elif condition34 and "i6" in clue:
        for j in range(self.k):
            if self.categories[clue["K5"]]["groups"][j] != clue["g5"]:
                self.grid_insert(K6, clue["i6"], K5, j, "X", "clue4_" + str(c), collect_solution)

    # if negative conclusion is false:
    if condition56 and "i1" in clue and "i2" in clue:
        self.grid_insert(K1, clue["i1"], K2, clue["i2"], "O", "clue4_" + str(c), collect_solution)
    elif condition56 and "i1" in clue:
        for j in range(self.k):
            if self.categories[clue["K2"]]["groups"][j] != clue["g2"]:
                self.grid_insert(K1, clue["i1"], K2, j, "X", "clue4_" + str(c), collect_solution)
    elif condition56 and "i2" in clue:
        for j in range(self.k):
            if self.categories[clue["K1"]]["groups"][j] != clue["g1"]:
                self.grid_insert(K2, clue["i2"], K1, j, "X", "clue4_" + str(c), collect_solution)

    if condition56 and "i3" in clue and "i4" in clue:
        self.grid_insert(K3, clue["i3"], K4, clue["i4"], "O", "clue4_" + str(c), collect_solution)
    elif condition56 and "i3" in clue:
        for j in range(self.k):
            if self.categories[clue["K4"]]["groups"][j] != clue["g4"]:
                self.grid_insert(K3, clue["i3"], K4, j, "X", "clue4_" + str(c), collect_solution)
    elif condition56 and "i4" in clue:
        for j in range(self.k):
            if self.categories[clue["K3"]]["groups"][j] != clue["g3"]:
                self.grid_insert(K4, clue["i4"], K3, j, "X", "clue4_" + str(c), collect_solution)

    # if premise is true:
    if condition12anti and "i3" in clue and "i4" in clue:
        self.grid_insert(K3, clue["i3"], K4, clue["i4"], "O", "clue4_" + str(c), collect_solution)
    elif condition12anti and "i3" in clue:
        for j in range(self.k):
            if self.categories[clue["K4"]]["groups"][j] != clue["g4"]:
                self.grid_insert(K3, clue["i3"], K4, j, "X", "clue4_" + str(c), collect_solution)
    elif condition12anti and "i4" in clue:
        for j in range(self.k):
            if self.categories[clue["K3"]]["groups"][j] != clue["g3"]:
                self.grid_insert(K4, clue["i4"], K3, j, "X", "clue4_" + str(c), collect_solution)

    # if premise is false:            
    if condition12 and "i5" in clue and "i6" in clue:
        self.grid_insert(K5, clue["i5"], K6, clue["i6"], "O", "clue4_" + str(c), collect_solution)
    elif condition12 and "i5" in clue:
        for j in range(self.k):
            if self.categories[clue["K6"]]["groups"][j] != clue["g6"]:
                self.grid_insert(K5, clue["i5"], K6, j, "X", "clue4_" + str(c), collect_solution)
    elif condition12 and "i6" in clue:
        for j in range(self.k):
            if self.categories[clue["K5"]]["groups"][j] != clue["g5"]:
                self.grid_insert(K6, clue["i6"], K5, j, "X", "clue4_" + str(c), collect_solution)


def use_clue5(self, c, collect_solution=False):
    clue = self.clues[c]
    K1 = clue["K1"]
    K2 = clue["K2"]
    K3 = clue["K3"]
    K4 = clue["K4"]

    if K1 == K3 and K2 == K4:
        if "i1" in clue and "i2" in clue and "i3" in clue and "i4" in clue:
            i1 = clue["i1"]
            i2 = clue["i2"]
            i3 = clue["i3"]
            i4 = clue["i4"]
            if i1 != i3 and i2 != i4:
                self.grid_insert(K1, i3, K2, i2, "X", "clue5_" + str(c), collect_solution)
                self.grid_insert(K1, i1, K2, i4, "X", "clue5_" + str(c), collect_solution)
            elif i1 == i3:
                for i in range(self.k):
                    if i != i2 and i != i4:
                        self.grid_insert(K1, i1, K2, i, "X", "clue5_" + str(c), collect_solution)
            else:
                for i in range(self.k):
                    if i != i1 and i != i3:
                        self.grid_insert(K1, i, K2, i2, "X", "clue5_" + str(c), collect_solution)

    # false12 - objects 1 and 2 cannot fit
    if "i1" in clue and "i2" in clue:
        false12 = self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 2
    elif "i1" in clue:
        false12 = not self.is_line_possible_for_group(clue["K1"], clue["i1"], clue["K2"], clue["g2"])
    elif "i2" in clue:
        false12 = not self.is_line_possible_for_group(clue["K2"], clue["i2"], clue["K1"], clue["g1"])
    else:  # both are group type
        false12 = True
        for i in range(self.k):
            if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                if self.is_line_possible_for_group(clue["K1"], i, clue["K2"], clue["g2"]):
                    false12 = False
                    break

    # false34 - objects 3 and 4 cannot fit
    if "i3" in clue and "i4" in clue:
        false34 = self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"]) == 2
    elif "i3" in clue:
        false34 = not self.is_line_possible_for_group(clue["K3"], clue["i3"], clue["K4"], clue["g4"])
    elif "i4" in clue:
        false34 = not self.is_line_possible_for_group(clue["K4"], clue["i4"], clue["K3"], clue["g3"])
    else:  # both are group type
        false34 = True
        for i in range(self.k):
            if self.categories[clue["K3"]]["groups"][i] == clue["g3"]:
                if self.is_line_possible_for_group(clue["K3"], i, clue["K4"], clue["g4"]):
                    false34 = False
                    break

    if clue["exclusive"]:
        # true12 - objects 1 and 2 are already connected
        if "i1" in clue and "i2" in clue:
            true12 = self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 1
        elif "i1" in clue:
            true12 = self.is_o_in_line_for_group(clue["K1"], clue["i1"], clue["K2"], clue["g2"])
        elif "i2" in clue:
            true12 = self.is_o_in_line_for_group(clue["K2"], clue["i2"], clue["K1"], clue["g1"])
        else:  # both are group type
            true12 = False
            for i in range(self.k):
                if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                    if self.is_o_in_line_for_group(clue["K1"], i, clue["K2"], clue["g2"]):
                        true12 = True
                        break
        # true34 - objects 1 and 2 are already connected
        if "i3" in clue and "i4" in clue:
            true34 = self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"]) == 1
        elif "i3" in clue:
            true34 = self.is_o_in_line_for_group(clue["K3"], clue["i3"], clue["K4"], clue["g4"])
        elif "i4" in clue:
            true34 = self.is_o_in_line_for_group(clue["K4"], clue["i4"], clue["K3"], clue["g3"])
        else:  # both are group type
            true34 = False
            for i in range(self.k):
                if self.categories[clue["K3"]]["groups"][i] == clue["g3"]:
                    if self.is_o_in_line_for_group(clue["K3"], i, clue["K4"], clue["g4"]):
                        true34 = True
                        break

    # if condition 1,2 is not fulfilled then the other one must be
    if false12 and "i3" in clue and "i4" in clue:
        self.grid_insert(K3, clue["i3"], K4, clue["i4"], "O", "clue5_" + str(c), collect_solution)
    elif false12 and "i3" in clue:
        for j in range(self.k):
            if self.categories[clue["K4"]]["groups"][j] != clue["g4"]:
                self.grid_insert(K3, clue["i3"], K4, j, "X", "clue5_" + str(c), collect_solution)
    elif false12 and "i4" in clue:
        for j in range(self.k):
            if self.categories[clue["K3"]]["groups"][j] != clue["g3"]:
                self.grid_insert(K4, clue["i4"], K3, j, "X", "clue5_" + str(c), collect_solution)
    # if condition 3,4 is not fulfilled then the other one must be
    if false34 and "i1" in clue and "i2" in clue:
        self.grid_insert(K1, clue["i1"], K2, clue["i2"], "O", "clue5_" + str(c), collect_solution)
    elif false34 and "i1" in clue:
        for j in range(self.k):
            if self.categories[clue["K2"]]["groups"][j] != clue["g2"]:
                self.grid_insert(K1, clue["i1"], K2, j, "X", "clue5_" + str(c), collect_solution)
    elif false34 and "i2" in clue:
        for j in range(self.k):
            if self.categories[clue["K1"]]["groups"][j] != clue["g1"]:
                self.grid_insert(K2, clue["i2"], K1, j, "X", "clue5_" + str(c), collect_solution)

    if clue["exclusive"]:
        # if condition 1,2 is fulfilled then the other one must not be
        if true12 and "i3" in clue and "i4" in clue:
            self.grid_insert(K3, clue["i3"], K4, clue["i4"], "X", "clue5_" + str(c), collect_solution)
        elif true12 and "i3" in clue:
            for j in range(self.k):
                if self.categories[clue["K4"]]["groups"][j] == clue["g4"]:
                    self.grid_insert(K3, clue["i3"], K4, j, "X", "clue5_" + str(c), collect_solution)
        elif true12 and "i4" in clue:
            for j in range(self.k):
                if self.categories[clue["K3"]]["groups"][j] == clue["g3"]:
                    self.grid_insert(K4, clue["i4"], K3, j, "X", "clue5_" + str(c), collect_solution)
        elif true12:
            for i in range(self.k):
                for j in range(self.k):
                    if self.categories[clue["K3"]]["groups"][i] == clue["g3"] and \
                            self.categories[clue["K4"]]["groups"][j] == clue["g4"]:
                        self.grid_insert(K3, i, K4, j, "X", "clue5_" + str(c), collect_solution)

        # if condition 3,4 is fulfilled then the other one must not be
        if true34 and "i1" in clue and "i2" in clue:
            self.grid_insert(K1, clue["i1"], K2, clue["i2"], "X", "clue5_" + str(c), collect_solution)
        elif true34 and "i1" in clue:
            for j in range(self.k):
                if self.categories[clue["K2"]]["groups"][j] == clue["g2"]:
                    self.grid_insert(K1, clue["i1"], K2, j, "X", "clue5_" + str(c), collect_solution)
        elif true34 and "i2" in clue:
            for j in range(self.k):
                if self.categories[clue["K1"]]["groups"][j] == clue["g1"]:
                    self.grid_insert(K2, clue["i2"], K1, j, "X", "clue5_" + str(c), collect_solution)
        elif true34:
            for i in range(self.k):
                for j in range(self.k):
                    if self.categories[clue["K1"]]["groups"][i] == clue["g1"] and \
                            self.categories[clue["K2"]]["groups"][j] == clue["g2"]:
                        self.grid_insert(K1, i, K2, j, "X", "clue5_" + str(c), collect_solution)


def use_clue6(self, c, collect_solution=False):
    clue = self.clues[c]
    K1 = clue["K1"]
    K2 = clue["K2"]
    K6 = clue["K6"]

    if clue["K1"] != clue["K2"] and "i1" in clue and "i2" in clue:
        self.grid_insert(clue["K1"], clue["i1"], clue["K2"], clue["i2"], "X", "clue6_" + str(c), collect_solution)

    for i in range(self.k):
        if "i1" in clue:
            if "i2" in clue:
                if self.get_grid_value(K1, clue["i1"], K6, i) == 0:
                    if (i == 0 or self.get_grid_value(K2, clue["i2"], K6, i - 1) == 2) and (
                            i == self.k - 1 or self.get_grid_value(K2, clue["i2"], K6, i + 1) == 2):
                        self.grid_insert(K1, clue["i1"], K6, i, "X", "clue6_" + str(c), collect_solution)
                elif self.get_grid_value(K1, clue["i1"], K6, i) == 1:
                    for j in range(self.k):
                        if j != i - 1 and j != i + 1:
                            self.grid_insert(K2, clue["i2"], K6, j, "X", "clue6_" + str(c), collect_solution)
            else:
                if self.get_grid_value(K1, clue["i1"], K6, i) == 0:
                    if (i == 0 or not self.is_line_possible_for_group(K6, i - 1, K2, clue["g2"])) and (
                            i == self.k - 1 or not self.is_line_possible_for_group(K6, i + 1, K2, clue["g2"])):
                        self.grid_insert(K1, clue["i1"], K6, i, "X", "clue6_" + str(c), collect_solution)

        if "i2" in clue:
            if "i1" in clue:
                if self.get_grid_value(K2, clue["i2"], K6, i) == 0:
                    if (i == 0 or self.get_grid_value(K1, clue["i1"], K6, i - 1) == 2) and (
                            i == self.k - 1 or self.get_grid_value(K1, clue["i1"], K6, i + 1) == 2):
                        self.grid_insert(K2, clue["i2"], K6, i, "X", "clue6_" + str(c), collect_solution)
                elif self.get_grid_value(K2, clue["i2"], K6, i) == 1:
                    for j in range(self.k):
                        if j != i - 1 and j != i + 1:
                            self.grid_insert(K1, clue["i1"], K6, j, "X", "clue6_" + str(c), collect_solution)
            else:
                if self.get_grid_value(K2, clue["i2"], K6, i) == 0:
                    if (i == 0 or not self.is_line_possible_for_group(K6, i - 1, K1, clue["g1"])) and (
                            i == self.k - 1 or not self.is_line_possible_for_group(K6, i + 1, K1, clue["g1"])):
                        self.grid_insert(K2, clue["i2"], K6, i, "X", "clue6_" + str(c), collect_solution)


def use_clue(self, c, collect_solution=False):
    if len(self.clues) <= c or c < 0:
        raise Exception("Wrong clue id provided: " + str(c) + "!")
    if self.clues[c]["typ"] not in [1, 2, 3, 4, 5, 6]:
        raise Exception("Wrong clue type provided!")

    typ = self.clues[c]["typ"]
    if typ == 1:
        self.use_clue1(c, collect_solution)
    elif typ == 2:
        self.use_clue2(c, collect_solution)
    elif typ == 3:
        self.use_clue3(c, collect_solution)
    elif typ == 4:
        self.use_clue4(c, collect_solution)
    elif typ == 5:
        self.use_clue5(c, collect_solution)
    elif typ == 6:
        self.use_clue6(c, collect_solution)


def is_grid_contradictory_with_clue1(self, c):
    clue = self.clues[c]
    if "g1" not in clue and "g2" not in clue:  # with no groups
        if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 1:
            return True
        if "i3" in clue:
            if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i3"]) == 1:
                return True
            if "i4" in clue:
                if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i4"]) == 1:
                    return True
    else:  # with groups
        if "g1" in clue:
            for i in range(self.k):
                if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                    if self.get_grid_value(clue["K1"], i, clue["K2"], clue["i2"]) == 1:
                        return True
        if "g2" in clue:
            for i in range(self.k):
                if self.categories[clue["K2"]]["groups"][i] == clue["g2"]:
                    if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], i) == 1:
                        return True


def is_grid_contradictory_with_clue2(self, c):
    clue = self.clues[c]
    i1 = None
    i2 = None
    i3 = None
    for j in range(self.k):
        if "i3" in clue:
            condition3 = self.get_grid_value(clue["K3"], clue["i3"], clue["K6"], j) != 2
        else:
            condition3 = self.is_line_possible_for_group(clue["K6"], j, clue["K3"], clue["g3"])
        if "i2" in clue:
            condition2 = self.get_grid_value(clue["K2"], clue["i2"], clue["K6"], j) != 2
        else:
            condition2 = self.is_line_possible_for_group(clue["K6"], j, clue["K2"], clue["g2"])
        if "i1" in clue:
            condition1 = self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], j) != 2
        else:
            condition1 = self.is_line_possible_for_group(clue["K6"], j, clue["K1"], clue["g1"])

        if i3 is None and condition3:
            i3 = j
        elif i2 is None and i3 is not None and condition2:
            i2 = j
        elif i2 is not None and condition1:
            i1 = j
            break
    if i1 is None:
        return True
    else:
        return False


def is_grid_contradictory_with_clue3(self, c):
    clue = self.clues[c]
    operation = clue["oper"]
    diff = clue["diff"]
    if self.categories[clue["K6"]]["typ"] == "numerical":
        values = self.categories[clue["K6"]]['names']
    else:
        values = list(range(1, self.k + 1))

    if operation == "+":
        for i in range(self.k):
            if "i1" in clue:
                condition1 = self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], i) != 2
            else:
                condition1 = self.is_line_possible_for_group(clue["K6"], i, clue["K1"], clue["g1"])
            if "i2" in clue:
                condition2 = values[i] + diff in values and self.get_grid_value(clue["K2"], clue["i2"], clue["K6"],
                                                                                values.index(values[i] + diff)) != 2
            else:
                condition2 = values[i] + diff in values and self.is_line_possible_for_group(clue["K6"], values.index(
                    values[i] + diff), clue["K2"], clue["g2"])

            if condition1 and condition2:
                return False
    elif operation == "*":
        for i in range(self.k):
            if "i1" in clue:
                condition1 = self.get_grid_value(clue["K1"], clue["i1"], clue["K6"], i) != 2
            else:
                condition1 = self.is_line_possible_for_group(clue["K6"], i, clue["K1"], clue["g1"])
            if "i2" in clue:
                condition2 = round(values[i] * diff, 12) in values and self.get_grid_value(clue["K2"], clue["i2"],
                                                                                           clue["K6"], values.index(
                        round(values[i] * diff, 12))) != 2
            else:
                condition2 = round(values[i] * diff, 12) in values \
                             and self.is_line_possible_for_group(clue["K6"],
                                                                 values.index(round(values[i] * diff, 12)), clue["K2"],
                                                                 clue["g2"])

            if condition1 and condition2:
                return False
    return True


def is_grid_contradictory_with_clue4(self, c):
    clue = self.clues[c]

    # condition12: premise is false
    if "i1" in clue and "i2" in clue:
        condition12 = self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 2
    elif "i1" in clue:
        condition12 = not self.is_line_possible_for_group(clue["K1"], clue["i1"], clue["K2"], clue["g2"])
    elif "i2" in clue:
        condition12 = not self.is_line_possible_for_group(clue["K2"], clue["i2"], clue["K1"], clue["g1"])
    else:  # if both are group type
        condition12 = True
        for i in range(self.k):
            if self.categories[clue["K2"]]["groups"][i] == clue["g2"] and self.is_line_possible_for_group(clue["K1"],
                                                                                                          clue["g1"],
                                                                                                          clue["K2"],
                                                                                                          i):
                condition12 = False
                break

    # condition12anti: premise is true
    if "i1" in clue and "i2" in clue:
        condition12anti = self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 1
    elif "i1" in clue:
        condition12anti = False
        for i in range(self.k):
            if self.categories[clue["K2"]]["groups"][i] == clue["g2"]:
                if self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], i) == 1:
                    condition12anti = True
                    break
    elif "i2" in clue:
        condition12anti = False
        for i in range(self.k):
            if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                if self.get_grid_value(clue["K2"], clue["i2"], clue["K1"], i) == 1:
                    condition12anti = True
                    break
    else:  # both are group type
        condition12anti = False
        for i in range(self.k):
            if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                for j in range(self.k):
                    if self.categories[clue["K2"]]["groups"][j] == clue["g2"]:
                        if self.get_grid_value(clue["K1"], i, clue["K2"], j) == 1:
                            condition12anti = True
                            break

    # condition34: positive conclusion is false
    if "i3" in clue and "i4" in clue:
        condition34 = self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"]) == 2
    elif "i3" in clue:
        condition34 = not self.is_line_possible_for_group(clue["K3"], clue["i3"], clue["K4"], clue["g4"])
    elif "i4" in clue:
        condition34 = not self.is_line_possible_for_group(clue["K4"], clue["i4"], clue["K3"], clue["g3"])
    else:  # both are group type
        condition34 = True
        for i in range(self.k):
            if self.categories[clue["K4"]]["groups"][i] == clue["g4"] and self.is_line_possible_for_group(clue["K3"],
                                                                                                          clue["g3"],
                                                                                                          clue["K4"],
                                                                                                          i):
                condition34 = False
                break

    # condition56: negative conclusion is false
    if "i5" in clue and "i6" in clue:
        condition56 = self.get_grid_value(clue["K5"], clue["i5"], clue["K6"], clue["i6"]) == 2
    elif "i5" in clue:
        condition56 = not self.is_line_possible_for_group(clue["K5"], clue["i5"], clue["K6"], clue["g6"])
    elif "i6" in clue:
        condition56 = not self.is_line_possible_for_group(clue["K6"], clue["i6"], clue["K5"], clue["g5"])
    else:  # both are group type
        condition56 = True
        for i in range(self.k):
            if self.categories[clue["K6"]]["groups"][i] == clue["g6"] and self.is_line_possible_for_group(clue["K5"],
                                                                                                          clue["g5"],
                                                                                                          clue["K6"],
                                                                                                          i):
                condition56 = False
                break

    # checking conditions:
    if condition34 and condition56:
        return True
    if condition12anti and condition34:
        return True
    if condition12 and condition56:
        return True
    return False


def is_grid_contradictory_with_clue5(self, c):
    clue = self.clues[c]

    # false12 - objects 1 and 2 cannot fit
    if "i1" in clue and "i2" in clue:
        false12 = self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 2
    elif "i1" in clue:
        false12 = not self.is_line_possible_for_group(clue["K1"], clue["i1"], clue["K2"], clue["g2"])
    elif "i2" in clue:
        false12 = not self.is_line_possible_for_group(clue["K2"], clue["i2"], clue["K1"], clue["g1"])
    else:  # both are group type
        false12 = True
        for i in range(self.k):
            if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                if self.is_line_possible_for_group(clue["K1"], i, clue["K2"], clue["g2"]):
                    false12 = False
                    break

    # false34 - objects 3 and 4 cannot fit
    if "i3" in clue and "i4" in clue:
        false34 = self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"]) == 2
    elif "i3" in clue:
        false34 = not self.is_line_possible_for_group(clue["K3"], clue["i3"], clue["K4"], clue["g4"])
    elif "i4" in clue:
        false34 = not self.is_line_possible_for_group(clue["K4"], clue["i4"], clue["K3"], clue["g3"])
    else:  # both are group type
        false34 = True
        for i in range(self.k):
            if self.categories[clue["K3"]]["groups"][i] == clue["g3"]:
                if self.is_line_possible_for_group(clue["K3"], i, clue["K4"], clue["g4"]):
                    false34 = False
                    break

    if clue["exclusive"]:
        # true12 - objects 1 and 2 are already connected
        if "i1" in clue and "i2" in clue:
            true12 = self.get_grid_value(clue["K1"], clue["i1"], clue["K2"], clue["i2"]) == 1
        elif "i1" in clue:
            true12 = self.is_o_in_line_for_group(clue["K1"], clue["i1"], clue["K2"], clue["g2"])
        elif "i2" in clue:
            true12 = self.is_o_in_line_for_group(clue["K2"], clue["i2"], clue["K1"], clue["g1"])
        else:  # both are group type
            true12 = False
            for i in range(self.k):
                if self.categories[clue["K1"]]["groups"][i] == clue["g1"]:
                    if self.is_o_in_line_for_group(clue["K1"], i, clue["K2"], clue["g2"]):
                        true12 = True
                        break
        # true34 - objects 1 and 2 are already connected
        if "i3" in clue and "i4" in clue:
            true34 = self.get_grid_value(clue["K3"], clue["i3"], clue["K4"], clue["i4"]) == 1
        elif "i3" in clue:
            true34 = self.is_o_in_line_for_group(clue["K3"], clue["i3"], clue["K4"], clue["g4"])
        elif "i4" in clue:
            true34 = self.is_o_in_line_for_group(clue["K4"], clue["i4"], clue["K3"], clue["g3"])
        else:  # both are group type
            true34 = False
            for i in range(self.k):
                if self.categories[clue["K3"]]["groups"][i] == clue["g3"]:
                    if self.is_o_in_line_for_group(clue["K3"], i, clue["K4"], clue["g4"]):
                        true34 = True
                        break

    if false12 and false34:
        return True
    if clue["exclusive"]:
        if true12 and true34:
            return True
    return False


def is_grid_contradictory_with_clue6(self, c):
    clue = self.clues[c]
    k = self.k
    K1 = clue["K1"]
    K2 = clue["K2"]
    K6 = clue["K6"]

    # checking if there is possible pair
    possible_pairs = 0
    if "i1" in clue and "i2" in clue:
        for i in range(k):
            if i != 0 and self.get_grid_value(K1, clue["i1"], K6, i) != 2 \
                    and self.get_grid_value(K2, clue["i2"], K6, i - 1) != 2:
                possible_pairs += 1
                break
            if i != k - 1 and self.get_grid_value(K1, clue["i1"], K6, i) != 2 \
                    and self.get_grid_value(K2, clue["i2"], K6, i + 1) != 2:
                possible_pairs += 1
                break
    elif "i1" in clue:
        for i in range(k):
            if i != 0 and self.get_grid_value(K1, clue["i1"], K6, i) != 2 \
                    and self.is_line_possible_for_group(K6, i - 1, K2, clue["g2"]):
                possible_pairs += 1
                break
            if i != k - 1 and self.get_grid_value(K1, clue["i1"], K6, i) != 2 \
                    and self.is_line_possible_for_group(K6, i + 1, K2, clue["g2"]):
                possible_pairs += 1
                break
    elif "i2" in clue:
        for i in range(k):
            if i != 0 and self.is_line_possible_for_group(K6, i, K1, clue["g1"]) \
                    and self.get_grid_value(K2, clue["i2"], K6, i - 1) != 2:
                possible_pairs += 1
                break
            if i != k - 1 and self.is_line_possible_for_group(K6, i, K1, clue["g1"]) \
                    and self.get_grid_value(K2, clue["i2"], K6, i + 1) != 2:
                possible_pairs += 1
                break
    else:  # both are group type
        for i in range(k):
            if i != 0 and self.is_line_possible_for_group(K6, i, K1, clue["g1"]) \
                    and self.is_line_possible_for_group(K6, i - 1, K2, clue["g2"]):
                possible_pairs += 1
                break
            if i != 0 and self.is_line_possible_for_group(K6, i, K2, clue["g2"]) \
                    and self.is_line_possible_for_group(K6, i - 1, K1, clue["g1"]):
                possible_pairs += 1
                break
    if possible_pairs == 0:
        return True

    # checking when there is already 'O' somewhere
    if "i1" in clue and "i2" in clue:
        i1 = clue["i1"]
        i2 = clue["i2"]
        for i in range(k):
            if self.get_grid_value(K1, i1, K6, i) == 1:
                if (i == 0 or self.get_grid_value(K2, i2, K6, i - 1) == 2) and (
                        i == k - 1 or self.get_grid_value(K2, i2, K6, i + 1) == 2):
                    return True
            if self.get_grid_value(K2, i2, K6, i) == 1:
                if (i == 0 or self.get_grid_value(K1, i1, K6, i - 1) == 2) and (
                        i == k - 1 or self.get_grid_value(K1, i1, K6, i + 1) == 2):
                    return True


def is_grid_completed(self):
    for box in self.grid.values():
        for i in range(self.k):
            for j in range(self.k):
                if box[i, j] == 0:
                    return False
    return True


def is_grid_contradictory(self):
    for box in self.grid.values():
        for i in range(self.k):
            o_count = 0
            x_count = 0
            for j in range(self.k):
                if box[i, j] == 1:
                    o_count += 1
                if box[i, j] == 2:
                    x_count += 1
            if o_count > 1 or x_count == self.k:
                return True
        for j in range(self.k):
            o_count = 0
            x_count = 0
            for i in range(self.k):
                if box[i, j] == 1:
                    o_count += 1
                if box[i, j] == 2:
                    x_count += 1
            if o_count > 1 or x_count == self.k:
                return True

    clues1 = [i for i, clue in enumerate(self.clues) if clue["typ"] == 1]
    for c in clues1:
        if self.is_grid_contradictory_with_clue1(c):
            # print("Puzzle is contradictory with clue 2!")
            return True
    clues2 = [i for i, clue in enumerate(self.clues) if clue["typ"] == 2]
    for c in clues2:
        if self.is_grid_contradictory_with_clue2(c):
            # print("Puzzle is contradictory with clue 2!")
            return True
    clues3 = [i for i, clue in enumerate(self.clues) if clue["typ"] == 3]
    for c in clues3:
        if self.is_grid_contradictory_with_clue3(c):
            # print("Puzzle is contradictory with clue 3!")
            return True
    clues4 = [i for i, clue in enumerate(self.clues) if clue["typ"] == 4]
    for c in clues4:
        if self.is_grid_contradictory_with_clue4(c):
            # print("Puzzle is contradictory with clue 4!")
            return True
    clues5 = [i for i, clue in enumerate(self.clues) if clue["typ"] == 5]
    for c in clues5:
        if self.is_grid_contradictory_with_clue5(c):
            # print("Puzzle is contradictory with clue 5!")
            return True
    clues6 = [i for i, clue in enumerate(self.clues) if clue["typ"] == 6]
    for c in clues6:
        if self.is_grid_contradictory_with_clue6(c):
            # print("Puzzle is contradictory with clue 6!")
            return True
    return False


def remove_unused_groups(self):
    for K, cat in enumerate(self.categories):
        if cat["typ"] == "categorical" and len(unique(cat["groups"])) > 1:
            remove = True
            for clue in self.clues:
                if clue["typ"] == 1 or clue["typ"] == 3 or clue["typ"] == 6:
                    if ("g1" in clue and clue["K1"] == K) or ("g2" in clue and clue["K2"] == K):
                        remove = False
                        break
                elif clue["typ"] == 2:
                    if ("g1" in clue and clue["K1"] == K) or ("g2" in clue and clue["K2"] == K) or (
                            "g3" in clue and clue["K3"] == K):
                        remove = False
                        break
                elif clue["typ"] == 5:
                    if ("g1" in clue and clue["K1"] == K) or ("g2" in clue and clue["K2"] == K) or (
                            "g3" in clue and clue["K3"] == K) or ("g4" in clue and clue["K4"] == K):
                        remove = False
                        break
                elif clue["typ"] == 4:
                    if ("g1" in clue and clue["K1"] == K) or ("g2" in clue and clue["K2"] == K) or (
                            "g3" in clue and clue["K3"] == K) or ("g4" in clue and clue["K4"] == K) or (
                            "g5" in clue and clue["K5"] == K) or ("g6" in clue and clue["K6"] == K):
                        remove = False
                        break
            if remove:
                cat["groups"] = [0] * self.k


def set_seed(self, seed):
    self.seed = seed
    random.seed(self.seed)


def draw_categories(self, diff=3, seed=None):
    if diff not in [2, 3, 4]:
        raise Exception("Difficulty must be either 2, 3 or 4!")
    if seed is None:
        self.categories = funs.draw_category(self.K, self.k, diff, self.seed)
    else:
        self.categories = funs.draw_category(self.K, self.k, diff, seed)
    i = 0
    i_max = 100
    while funs.do_categories_repeat(self.categories):
        self.categories = funs.draw_category(self.K, self.k, diff, self.seed + i * 1234567)
        i += 1
        if i > i_max:
            raise Exception("Program couldn't draw non-repeating categories!")


def draw_clues(self, trace=False):
    non_1_clues = int(ceil(self.k * self.K / 2.3))
    are_ordinal = any([cat['typ'] == 'ordinal' for cat in self.categories])
    are_numerical = any(["pre_clues" in cat and len(cat["pre_clues"]) > 0 for cat in self.categories])
    for i in range(non_1_clues):
        if are_numerical:
            typ = random.choice([2, 3, 4, 5, 6], 1, p=[0.2, 0.2, 0.2, 0.2, 0.2])[0]
        elif are_ordinal:
            typ = random.choice([2, 4, 5, 6], 1, p=[0.25, 0.25, 0.25, 0.25])[0]
        else:
            typ = random.choice([4, 5], 1, p=[0.5, 0.5])[0]
        if trace:
            print("Trying to fit clue of type " + str(typ))
        if typ == 2:
            self.add_clue2()
        elif typ == 3:
            self.add_clue3()
        elif typ == 4:
            self.add_clue4()
        elif typ == 5:
            self.add_clue5()
        elif typ == 6:
            self.add_clue6()

        if trace and len(self.clues) < i:
            print("Failed to draw clue of type " + str(typ))

        if len(self.clues) > 0:
            self.use_clue(len(self.clues) - 1)
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
        self.use_clue(len(self.clues) - 1)
        self.grid_concile()
        if trace:
            print("Clue of type 1 added")
        for j in range(non_1_clues):
            self.use_clue(j)
            self.grid_concile()
            if self.is_grid_completed() or self.is_grid_contradictory():
                self.critical_squares = []
                self.clues_to_check = []
                for clue in self.clues:
                    self.critical_squares.append(self.get_critical_squares(clue, everything=True))
                return
        if trace:
            self.print_grid()
            self.print_info()

    # if it fails to draw clues:
    self.critical_squares = []
    self.clues_to_check = []


def try_to_solve2(self, collect_solution=False):
    clues1 = [i for i, clue in enumerate(self.clues) if clue["typ"] == 1]
    clues2 = [i for i, clue in enumerate(self.clues) if clue["typ"] != 1]

    for c in clues1:
        self.use_clue1(c, collect_solution)
    self.grid_concile(collect_solution)
    for c in clues2:
        self.use_clue(c, collect_solution)
        self.grid_concile(collect_solution)

    # changed_copy = self.changed
    self.changed2 = True
    while self.changed2:
        self.changed2 = False
        for i in range(2):
            clues_to_check = self.clues_to_check
            self.clues_to_check = []
            for clue_id in unique(clues_to_check):
                self.use_clue(clue_id, collect_solution)
                self.grid_concile(collect_solution)
        for c in clues2:
            self.use_clue(c, collect_solution)
            self.grid_concile(collect_solution)
            if self.is_grid_contradictory() or self.is_grid_completed():
                # if changed_copy and not self.changed:
                #    self.changed = changed_copy
                return

        # for i in range(2):

        # if self.changed:
        #    changed_copy = True
    # self.changed = changed_copy


def try_to_solve(self, max_iter=None, collect_solution=False):
    self.solved = False
    self.contradictory = False
    # grid_main_copy = copy.deepcopy(self.grid)
    self.changed = True

    it = 0
    while self.changed:
        self.changed = False
        self.try_to_solve2(collect_solution)
        if self.is_grid_contradictory():
            self.contradictory = True
            return
        if self.is_grid_completed():
            self.solved = True
            return

        # if brute force guessing is needed:
        key_candidates = random.permutation(list(self.grid.keys()))
        for key in key_candidates:
            for i in range(self.k):
                for j in range(self.k):
                    K1 = int(key.split(",")[0])
                    K2 = int(key.split(",")[1])
                    if self.get_grid_value(K1, i, K2, j) == 0:
                        grid_copy = copy.deepcopy(self.grid)
                        self.grid_insert(K1, i, K2, j, "O")
                        self.try_to_solve2()
                        if self.is_grid_contradictory():
                            self.grid = grid_copy
                            self.grid_insert(K1, i, K2, j, "X", "contr", collect_solution)
                            self.diff += 1
                            self.try_to_solve2(collect_solution)
                            if self.is_grid_contradictory():
                                self.contradictory = True
                                return
                            if self.is_grid_completed():
                                self.solved = True
                                return
                        else:
                            self.grid = grid_copy
        if max_iter is not None and it >= max_iter:
            return
        it += 1
    # self.grid = grid_main_copy


def try_to_restrict_clues(self, trace=False, max_iter=None):
    clues_copy = copy.deepcopy(self.clues)
    to_restrict = []

    trace_i = 1
    trace_clue_count = len(self.clues)
    clues1 = [i for i, clue in enumerate(clues_copy) if clue["typ"] == 1]
    clue_order = random.choice(clues1, len(clues1), replace=False)
    for i in clue_order:
        clues1_restricted = [j for j in clues1 if j != i]
        self.clear_grid()
        self.clues = [clue for j, clue in enumerate(clues_copy) if j in clues1_restricted or j not in clue_order]
        self.critical_squares = []
        self.clues_to_check = []
        for clue in self.clues:
            self.critical_squares.append(self.get_critical_squares(clue))

        self.try_to_solve(max_iter)
        if self.is_grid_completed() and not self.is_grid_contradictory():
            to_restrict.append(i)
            clues1 = clues1_restricted
            if trace:
                print("Restricting clue " + str(trace_i) + "/" + str(trace_clue_count) + ", type: 1 OUT")
                trace_i += 1
        elif trace:
            print("Restricting clue " + str(trace_i) + "/" + str(trace_clue_count) + ", type: 1")
            trace_i += 1

    clues_other = [i for i, clue in enumerate(clues_copy) if clue["typ"] != 1]
    clue_order = random.permutation(clues_other)
    for i in clue_order:
        clues_restricted = [j for j in clues_other if j != i]
        self.clear_grid()
        self.clues = [clue for j, clue in enumerate(clues_copy) if j in clues_restricted or j in clues1]
        self.critical_squares = []
        self.clues_to_check = []
        for clue in self.clues:
            self.critical_squares.append(self.get_critical_squares(clue))

        self.try_to_solve(max_iter)
        if self.is_grid_completed() and not self.is_grid_contradictory():
            to_restrict.append(i)
            clues_other = clues_restricted
            if trace:
                print("Restricting clue " + str(trace_i) + "/" + str(trace_clue_count) + ", type: " + str(
                    clues_copy[i]["typ"]) + " OUT")
                trace_i += 1
        elif trace:
            print("Restricting clue " + str(trace_i) + "/" + str(trace_clue_count) + ", type: " + str(
                clues_copy[i]["typ"]))
            trace_i += 1

    self.clues = [clue for j, clue in enumerate(clues_copy) if j not in to_restrict]
    self.critical_squares = []
    self.clues_to_check = []
    for clue in self.clues:
        self.critical_squares.append(self.get_critical_squares(clue))


def generate(self, seed=0, trace=False, max_iter=None):
    self.set_seed(seed)
    if trace:
        print("Generating puzzle for seed=" + str(seed))
        print("Drawing categories...")
    if trace:
        print("Drawing clues...")

    i_max = 20
    j_max = 5
    for j in range(j_max):
        self.draw_categories(seed=self.seed + 123456 * j)
        for i in range(i_max):
            self.clear_grid()
            self.clues = []
            self.draw_clues()
            if self.is_grid_completed() and not self.is_grid_contradictory():
                break
            self.critical_squares = []
            self.clues_to_check = []

            if trace and i == i_max - 1 and j == j_max - 1:
                print("Failed to draw clues!!!")

    if trace:
        print("Categories drawn:")
        for c in self.categories:
            print(c)

    if trace:
        clues_counts = [len([i for i in self.clues if i["typ"] == j]) for j in range(1, 7)]
        print("No of clues drawn = " + str(len(self.clues)) + str(clues_counts))
        print("Restricting clues...")

    self.try_to_restrict_clues(trace=trace, max_iter=max_iter)
    self.clues = list(random.permutation(self.clues))

    if trace:
        print("Final difficulty assessment...")
    N = 5
    diffs = []
    best_solution = ""
    lowest_diff = 1000000
    for n in range(N):
        self.clear_grid()
        self.diff = 0

        self.solution = ""
        self.try_to_solve(collect_solution=True)

        if self.diff < lowest_diff:
            best_solution = self.solution
            lowest_diff = self.diff

        diffs.append(self.diff)
    self.solution = best_solution
    if trace:
        print("Difficulty: " + str(mean(diffs)) + str(diffs))
    self.diff = round(mean(diffs), 2)


def print_info(self):
    print("Seed: " + str(self.seed) + ", difficulty: " + str(self.diff))
    print("Completed: " + str(self.is_grid_completed()) + ", Contradictory: " + str(self.is_grid_contradictory()))
    clues_counts = [len([i for i in self.clues if i["typ"] == j]) for j in range(1, 7)]
    print("K: " + str(self.K) + ", k: " + str(self.k) + ", No of clues: " + str(len(self.clues)) + str(clues_counts))


# --------------------- class definition ------------------------------


class puzzle:
    def __init__(self, K, k):
        self.K = K
        self.k = k
        self.grid = {str(i) + "," + str(j): zeros((k, k)) for i in range(K) for j in range(K) if i < j}
        self.critical_squares = []
        self.clues_to_check = []
        self.changed = False
        self.changed2 = False
        self.changed3 = False
        self.solved = False
        self.contradictory = False
        self.categories = []
        self.clues = []
        self.seed = 0
        self.diff = 0
        self.solution = ""

    get_grid_value = get_grid_value
    grid_insert = grid_insert
    print_grid = print_grid
    clear_grid = clear_grid
    is_grid_completed = is_grid_completed
    is_grid_contradictory = is_grid_contradictory
    print_info = print_info
    remove_unused_groups = remove_unused_groups

    set_seed = set_seed
    draw_categories = draw_categories
    draw_clues = draw_clues

    is_line_completed = is_line_completed
    count_x_in_line = count_x_in_line
    is_line_possible_for_group = is_line_possible_for_group

    grid_concile1 = grid_concile1  # deprecated
    grid_concile2 = grid_concile2  # deprecated
    grid_concile3 = grid_concile3
    grid_concile4 = grid_concile4
    grid_concile5 = grid_concile5
    grid_concile = grid_concile

    get_critical_squares = get_critical_squares
    get_critical_squares_from_between = get_critical_squares_from_between
    get_critical_squares_from_line = get_critical_squares_from_line
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

    is_grid_contradictory_with_clue1 = is_grid_contradictory_with_clue1
    is_grid_contradictory_with_clue2 = is_grid_contradictory_with_clue2
    is_grid_contradictory_with_clue3 = is_grid_contradictory_with_clue3
    is_grid_contradictory_with_clue4 = is_grid_contradictory_with_clue4
    is_grid_contradictory_with_clue5 = is_grid_contradictory_with_clue5
    is_grid_contradictory_with_clue6 = is_grid_contradictory_with_clue6

    try_to_solve2 = try_to_solve2
    try_to_solve = try_to_solve
    try_to_restrict_clues = try_to_restrict_clues
    generate = generate
