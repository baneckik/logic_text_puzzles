import numpy as np
import pandas as pd
from pathlib import Path
import os
from reportlab.pdfgen import canvas
import random
from math import pi, cos, sin

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
pdfmetrics.registerFont(TTFont('sans-serif', 'FreeSans.ttf'))

import generating_categories_functions as funs
from puzzle_class import puzzle

# --------------------------------------- auxiliary functions ----------------------------------

def star(canvas, xcenter, ycenter, radius):
    p = canvas.beginPath()
    p.moveTo(xcenter,ycenter+radius)
    angle = (2*pi)*2/5.0
    startangle = pi/2.0
    for vertex in range(5-1):
        nextangle = angle*(vertex+1)+startangle
        x = xcenter + radius*cos(nextangle)
        y = ycenter + radius*sin(nextangle)
        p.lineTo(x,y)
    p.close()
    canvas.drawPath(p)

def rysuj_pytanie(kategorie, clue, c, X, Y, no, width):
    normal_font = "sans-serif"
    special_font = "Times-Bold"
    replace_polish = True
    
    x = X
    text0 = str(no+1)+". "
    c.setFont(normal_font, width)
    c.drawString(x, Y, text0)
    textWidth = stringWidth(text0, normal_font, width) 
    x += textWidth + 1
    
    if clue["typ"]==1:
        text1 = funs.get_string_name(kategorie, clue["K1"], clue["i1"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text1)
        textWidth = stringWidth(text1, special_font, width) 
        x += textWidth + 1

        if "i3" not in clue:
            text2 = " nie pasuje do "
            c.setFont(normal_font, width)
            c.drawString(x, Y, text2)
            textWidth = stringWidth(text2, normal_font, width) 
            x += textWidth + 1
            
            text3 = funs.get_string_name(kategorie, clue["K2"], clue["i2"], replace_polish)
            c.setFont(special_font, width)
            c.drawString(x, Y, text3)
        else:
            text2 = " nie pasuje ani do "
            c.setFont(normal_font, width)
            c.drawString(x, Y, text2)
            textWidth = stringWidth(text2, normal_font, width) 
            x += textWidth + 1

            text3 = funs.get_string_name(kategorie, clue["K2"], clue["i2"], replace_polish)
            c.setFont(special_font, width)
            c.drawString(x, Y, text3)
            textWidth = stringWidth(text3, special_font, width) 
            x += textWidth + 1

            text4 = " ani do "
            c.setFont(normal_font, width)
            c.drawString(x, Y, text4)
            textWidth = stringWidth(text4, normal_font, width) 
            x += textWidth + 1

            text5 = funs.get_string_name(kategorie, clue["K2"], clue["i3"], replace_polish)
            c.setFont(special_font, width)
            c.drawString(x, Y, text5)
            textWidth = stringWidth(text5, special_font, width) 
            x += textWidth + 1
            if "i4" in clue:
                text6 = " ani do "
                c.setFont(normal_font, width)
                c.drawString(x, Y, text6)
                textWidth = stringWidth(text6, normal_font, width) 
                x += textWidth + 1

                text7 = funs.get_string_name(kategorie, clue["K2"], clue["i4"], replace_polish)
                c.setFont(special_font, width)
                c.drawString(x, Y, text7)
    elif clue["typ"]==2:
        text1 = "Pod względem "
        c.drawString(x, Y, text1)
        textWidth = stringWidth(text1, normal_font, width) 
        x += textWidth + 1
        
        text2 = "Kategorii "+str(clue["K6"])
        c.setFont(special_font, width)
        c.drawString(x, Y, text2)
        textWidth = stringWidth(text2, special_font, width) 
        x += textWidth + 1
        
        text3 = " zachodzi: "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text3)
        textWidth = stringWidth(text3, normal_font, width) 
        x += textWidth + 1
        
        text4 = funs.get_string_name(kategorie, clue["K3"], clue["i3"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = "<"
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        text6 = funs.get_string_name(kategorie, clue["K2"], clue["i2"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        text7 = funs.get_string_name(kategorie, clue["K1"], clue["i1"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text7)
    elif clue["typ"]==3:
        text1 = "Pod względem "
        c.drawString(x, Y, text1)
        textWidth = stringWidth(text1, normal_font, width) 
        x += textWidth + 1
        
        text2 = "Kategorii "+str(clue["K6"])
        c.setFont(special_font, width)
        c.drawString(x, Y, text2)
        textWidth = stringWidth(text2, special_font, width) 
        x += textWidth + 1
        
        text3 = " zachodzi: "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text3)
        textWidth = stringWidth(text3, normal_font, width) 
        x += textWidth + 1
        
        text4 = funs.get_string_name(kategorie, clue["K2"], clue["i2"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = " = "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        text6 = funs.get_string_name(kategorie, clue["K1"], clue["i1"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
        if str(clue["diff"]).endswith(".0"):
            diff = str(clue["diff"])[:-2]
        else:
            diff = str(clue["diff"])
        text7 = " "+clue["oper"]+" "+diff
        c.setFont(normal_font, width)
        c.drawString(x, Y, text7)
    elif clue["typ"]==4:
        text1 = "Jeśli "
        c.drawString(x, Y, text1)
        textWidth = stringWidth(text1, normal_font, width) 
        x += textWidth + 1
        
        text2 = funs.get_string_name(kategorie, clue["K1"], clue["i1"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text2)
        textWidth = stringWidth(text2, special_font, width) 
        x += textWidth + 1
        
        text3 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text3)
        textWidth = stringWidth(text3, normal_font, width) 
        x += textWidth + 1
        
        text4 = funs.get_string_name(kategorie, clue["K2"], clue["i2"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = ", to "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        text6 = funs.get_string_name(kategorie, clue["K3"], clue["i3"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
        text7 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text7)
        textWidth = stringWidth(text7, normal_font, width) 
        x += textWidth + 1
        
        text8 = funs.get_string_name(kategorie, clue["K4"], clue["i4"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text8)
        
        textWidth = stringWidth(text0, normal_font, width) 
        x = X + textWidth + 1
        
        text9 = "W przeciwnym przypadku "
        c.setFont(normal_font, width)
        c.drawString(x, Y-width, text9)
        textWidth = stringWidth(text9, normal_font, width) 
        x += textWidth + 1
        
        text10 = funs.get_string_name(kategorie, clue["K5"], clue["i5"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y-width, text10)
        textWidth = stringWidth(text10, special_font, width) 
        x += textWidth + 1
        
        text11 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y-width, text11)
        textWidth = stringWidth(text11, normal_font, width) 
        x += textWidth + 1
        
        text12 = funs.get_string_name(kategorie, clue["K6"], clue["i6"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y-width, text12)
    elif clue["typ"]==5:
        text1 = "Albo "
        c.drawString(x, Y, text1)
        textWidth = stringWidth(text1, normal_font, width) 
        x += textWidth + 1
        
        text2 = funs.get_string_name(kategorie, clue["K1"], clue["i1"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text2)
        textWidth = stringWidth(text2, special_font, width) 
        x += textWidth + 1
        
        text3 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text3)
        textWidth = stringWidth(text3, normal_font, width) 
        x += textWidth + 1
        
        text4 = funs.get_string_name(kategorie, clue["K2"], clue["i2"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = " albo "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        text6 = funs.get_string_name(kategorie, clue["K3"], clue["i3"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
        text7 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text7)
        textWidth = stringWidth(text7, normal_font, width) 
        x += textWidth + 1
        
        text8 = funs.get_string_name(kategorie, clue["K4"], clue["i4"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text8)
        textWidth = stringWidth(text8, special_font, width) 
        x += textWidth + 1
        
        text9 = " (alternatywa)"
        c.setFont(normal_font, width)
        c.drawString(x, Y, text9)
        textWidth = stringWidth(text9, normal_font, width) 
        x += textWidth + 1
    elif clue["typ"]==6:
        text1 = "Pod względem "
        c.drawString(x, Y, text1)
        textWidth = stringWidth(text1, normal_font, width) 
        x += textWidth + 1
        
        text2 = "Kategorii "+str(clue["K6"])
        c.setFont(special_font, width)
        c.drawString(x, Y, text2)
        textWidth = stringWidth(text2, special_font, width) 
        x += textWidth + 1
        
        text3 = " obiekt "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text3)
        textWidth = stringWidth(text3, normal_font, width) 
        x += textWidth + 1
        
        text4 = funs.get_string_name(kategorie, clue["K1"], clue["i1"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = " jest tuż obok "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        text6 = funs.get_string_name(kategorie, clue["K2"], clue["i2"], replace_polish)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
        
        
# --------------------------------------- main printing function ----------------------------------

def rysuj_zagadke(puzzle1, c, X = 30, Y = 30, box_size = None):
    
    kategorie = puzzle1.categories
    clues = puzzle1.clues
    seed = puzzle1.seed
    K_cat = puzzle1.K # liczba kategorii
    k_cat = puzzle1.k # liczba obiektów z każdej kategorii
    puzzle_h = 400 # height of the puzzle grid
    
    if box_size == None:
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
    
    # ------------ drawing boxes
    c.setLineWidth(2)
    for row in range(N_rows):
        c.rect( X, Y+row*box_size, text_box_size+(row+1)*box_size, box_size)
        c.rect( X+text_box_size+row*box_size, Y+row*box_size, box_size, text_box_size+(N_rows-row)*box_size)
    c.setLineWidth(1)
    for row in range(N_rows):
        for k in range(k_cat):
            c.rect( X, Y+row*box_size, text_box_size+(row+1)*box_size, k*box_size/k_cat)
            c.rect( X+text_box_size+row*box_size, Y+row*box_size, k*box_size/k_cat, text_box_size+(N_rows-row)*box_size)
    
    # ------------- drawing clues
    N_lines = len(puzzle1.clues)+len([c for c in puzzle1.clues if c["typ"]==4])
    if N_lines<=18:
        width_clue = 14
    elif N_lines<25:
        width_clue = 12
    else:
        width_clue = 10
    Xc = 30
    Yc = 810
    odstep = 0.15
    
    c.setFont("sans-serif", width_clue)
    clue_order = np.random.choice(range(len(clues)), len(clues), replace=False)
    additional_rows = 0
    for i in range(len(clues)):
        rysuj_pytanie(kategorie, clues[clue_order[i]], c, Xc+odstep*width_clue, Yc-width_clue*(i+additional_rows), i, width_clue)
        if clues[clue_order[i]]["typ"]==4:
            additional_rows += 1
    
    # ------------- drawing footnote and info
    width_foot = 8
    c.setFont("sans-serif", width_foot)
    
    c.drawString(X+text_box_size+box_size+10, Y+3*width_foot, "diff: "+str(puzzle1.diff))
    
    if puzzle1.is_grid_contradictory():
        c.setFillColorRGB(1,0,0)
    c.drawString(X+text_box_size+box_size+10, Y+2*width_foot, "Contradictory: "+str(puzzle1.is_grid_contradictory()))
    c.setFillColorRGB(0,0,0)
    
    if not puzzle1.is_grid_completed():
        c.setFillColorRGB(1,0,0)
    c.drawString(X+text_box_size+box_size+10, Y+width_foot, "Solvable: "+str(puzzle1.is_grid_completed()))
    c.setFillColorRGB(0,0,0)
    
    c.drawString(X+text_box_size+box_size+10, Y, "seed: "+str(seed))

    c.drawString(450, 10, "Krzysztof Banecki, all rights reserved ©")
    
    # ------------- drawing solution
    c.saveState()
    c.rotate( 270 )
    X_sol = -Y-350
    Y_sol = 570
    
    width_sol = 8
    c.setFont("Times-Bold", width_sol)
    c.drawString(X_sol, Y_sol, "Solution:")
    c.setFont("sans-serif", width_sol)
    for i in range(k_cat):
        linijka = funs.get_string_name(kategorie, 0, i, replace_polish=False)
        for k2 in range(1, K_cat):
            for j in range(k_cat):
                if puzzle1.get_grid_value(0, i, k2, j)==1:
                    break
            linijka += " ~ "+funs.get_string_name(kategorie, k2, j, replace_polish=False)
        c.drawString(X_sol, Y_sol-(i+1)*width_sol,linijka)
    
    c.restoreState()
    
    # ------------- typing categories names
    width2 = 10
    
    normal_font = "sans-serif"
    special_font = "Times-Bold"
    c.setFont(normal_font, width2)
    
    Xc = 430
    if k_cat<=5:
        Ycat = Y+puzzle_h+width2*(k_cat+1)
    else:
        Ycat = Y+puzzle_h+width2*6
        
    x_shift = 0
    for i in range(len(kategorie)):
        widths = []
        c.setFont(special_font, width2)
        text0 = "Kategoria "+str(i)+":"
        widths.append( stringWidth(text0, special_font, width2) )
        
        nazwy = [ funs.get_string_name(kategorie, i, j, False) for j in range(len(kategorie[i][1])) ]
        c.drawString(X+x_shift, Ycat, text0)
        c.setFont(normal_font, width2)
        for col, name in enumerate(nazwy):
            if k_cat>5 and col>3:
                c.drawString(X+x_shift, Ycat-width2*(col+1), "...")
                widths.append( stringWidth("...", normal_font, width2) )
                break
            c.drawString(X+x_shift, Ycat-width2*(col+1), name)
            widths.append( stringWidth(name, normal_font, width2) )
        x_shift += int(np.max(widths))+10
            
    
    # ------------- typing categories names into boxes
    
    for i, kategoria in enumerate(kategorie):
        nazwy = [ str(k) for k in kategoria[1] ]
        if kategoria[0]=='numerical':
            nazwy = [ k[:-2] if k.endswith(".0") else k for k in nazwy ]
            if "@" in kategoria[3]:
                a = kategoria[3].split("@")
                nazwy = [ k.join(a) for k in nazwy ]
        
        miejsce = i+1
        odstep = 0.15
        for i, name in enumerate(nazwy):
            if len(name) > 7+(k_cat-3)*3:
                c.setFont("sans-serif", width*(7+(k_cat-3)*3)/len(name))
            else:
                c.setFont("sans-serif", width)
            # rysowanie poziome:
            if miejsce==1:
                c.drawString(X+odstep*width, Y+(K_cat-1)*box_size-(i+1)*width+odstep*width, name)
            elif miejsce!=2:
                c.drawString(X+odstep*width, Y+(miejsce-2)*box_size-(i+1)*width+odstep*width, name)
            c.saveState()
            # rysowanie pionowe:
            c.rotate( 90 )
            if miejsce==2:
                c.drawString(Y+(K_cat-1)*box_size+odstep*width, -X-text_box_size-(i+1)*width+odstep*width, name)
            elif miejsce!=1:
                c.drawString(Y+(K_cat-1)*box_size+odstep*width, -X-text_box_size-(miejsce-2)*box_size-(i+1)*width+odstep*width, name)

            c.restoreState()