import drawSvg as draw
import numpy as np
from math import pi, cos, sin

import generating_categories_functions as funs
from puzzle_class import puzzle


def draw_svg(canvas, xcenter, ycenter, radius):
    r = draw.Rectangle(-80,0,40,45, stroke_width=2, stroke='black', fill_opacity=0)
    d.append(r)
    
    d.append(draw.Text('Basic text', 8, -10, 35, fill='blue'))
    d.append(draw.Text('Basic text', 8, 10, 10, transform='rotate(90)'))
    
def star(canvas, xcenter, ycenter, radius):
    angle = (2*pi)*2/5.0
    startangle = pi/2.0
    pre_x = xcenter
    pre_y = ycenter+radius
    for vertex in range(5):
        nextangle = angle*(vertex+1)+startangle
        x = xcenter + radius*cos(nextangle)
        y = ycenter + radius*sin(nextangle)
        canvas.append(draw.Lines(pre_x, pre_y, x, y, close=False, stroke='black'))
        pre_x = x
        pre_y = y

def draw_clues_on_canvas(categories, clue, canvas, X, Y, no, width):
    replace_polish = False
    if funs.do_categories_repeat(categories, with_bar=False):
        add_info = True    # additional (K0) with names in case of repeating names
    else:
        add_info = False
    text0 = str(no+1)+". "
    if clue["typ"]==1:
        text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        if "i3" not in clue:
            text0 += " nie pasuje do "
            text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        else:
            text0 += " nie pasuje ani do "
            text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
            text0 += " ani do "
            text0 += funs.get_string_name(categories, clue["K2"], clue["i3"], replace_polish, add_info=add_info)
            if "i4" in clue:
                text0 += " ani do "
                text0 += funs.get_string_name(categories, clue["K2"], clue["i4"], replace_polish, add_info=add_info)      
    elif clue["typ"]==2:
        text0 += "Pod względem "
        text0 += "Kategorii "+str(clue["K6"])
        text0 += " zachodzi: "
        text0 += funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)    
        text0 += "<"
        text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        text0 += "<"
        text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
    elif clue["typ"]==3:
        text0 += "Pod względem "
        text0 += "Kategorii "+str(clue["K6"])
        text0 += " zachodzi: "
        text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        text0 += " = "
        text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        if str(clue["diff"]).endswith(".0"):
            diff = str(clue["diff"])[:-2]
        else:
            diff = str(clue["diff"])
        text0 += " "+clue["oper"]+" "+diff
    elif clue["typ"]==4:
        text0 += "Jeśli "
        text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        text0 += ", to "
        text0 += funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        text0 += funs.get_string_name(categories, clue["K4"], clue["i4"], replace_polish, add_info=add_info)
        text0 += "\n"
        
        text0 += "W przeciwnym przypadku "
        text0 += funs.get_string_name(categories, clue["K5"], clue["i5"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        text0 += funs.get_string_name(categories, clue["K6"], clue["i6"], replace_polish, add_info=add_info)
    elif clue["typ"]==5:
        text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        text0 += " lub "
        text0 += funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        text0 += funs.get_string_name(categories, clue["K4"], clue["i4"], replace_polish, add_info=add_info)
        text0 += "(alt. nierozł.)"
#         text0 += "Albo "    
#         text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
#         text0 += " pasuje do "
#         text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
#         text0 += " albo "
#         text0 += funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
#         text0 += " pasuje do "
#         text0 += funs.get_string_name(categories, clue["K4"], clue["i4"], replace_polish, add_info=add_info)
#         text0 += " (alt. rozł.)"
    elif clue["typ"]==6:
        text0 += "Pod względem "
        text0 += "Kategorii "+str(clue["K6"])
        text0 += " obiekt "
        text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        text0 += " jest tuż obok "
        text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
    canvas.append(draw.Text(text0, width, X, Y, fill='black')) 

def draw_into_rectangle(c, X, Y, text, font, rec_h, rec_w):
    pass
        
def draw_grid(puzzle1, c, X = 30, Y = 30):
    pass
        
def draw_on_canvas(puzzle1, c, X = 30, Y = 30, puzzle_h = 400):
    categories = puzzle1.categories
    clues = puzzle1.clues
    seed = puzzle1.seed
    K_cat = puzzle1.K # liczba kategorii
    k_cat = puzzle1.k # liczba obiektów z każdej kategorii
    #puzzle_h - height of the puzzle grid
    
    box_size = puzzle_h/(K_cat+0.5)
    text_box_size = box_size*1.5
    
    N_rows = K_cat-1
    width = box_size/k_cat
    
    # ------------ drawing stars
    
    if puzzle1.diff<2:
        n = 1
    elif puzzle1.diff<5:
        n = 2
    elif puzzle1.diff<10:
        n = 3
    else:
        n = 4
        
    for i in range(n):
        star(c, X+box_size*1.5-15-i*25, Y+puzzle_h-box_size*1.5+15, 10)
    
    # ------------ drawing grid
    draw_grid(puzzle1=puzzle1, c=c, X=X, Y=Y)
    
    # ------------- drawing clues
    N_lines = len(puzzle1.clues)+len([c for c in puzzle1.clues if c["typ"]==4])
    if N_lines<=18:
        width_clue = 14
    elif N_lines<25:
        width_clue = 12
    else:
        width_clue = 10
    Xc = 25
    Yc = 810
    odstep = 0.15
    
    additional_rows = 0
    for i in range(len(clues)):
        draw_clues_on_canvas(categories, clues[i], c, Xc+odstep*width_clue, Yc-width_clue*(i+additional_rows), i, width_clue)
        if clues[i]["typ"]==4:
            additional_rows += 1
    
    