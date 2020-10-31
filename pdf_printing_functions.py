import numpy as np
import pandas as pd
from pathlib import Path
import os
from reportlab.pdfgen import canvas
import random

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
pdfmetrics.registerFont(TTFont('sans-serif', 'FreeSans.ttf'))

import generating_cathegories_functions as funs
from puzzle_class import puzzle

# --------------------------------------- auxiliary functions ----------------------------------

def rysuj_pytanie(kategorie, clue, c, X, Y, no, width):
    normal_font = "sans-serif"
    special_font = "Times-Bold"
    replace_polish = True
    
    if clue["typ"]==1:
        x = X
        text0 = str(no+1)+". "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text0)
        textWidth = stringWidth(text0, normal_font, width) 
        x += textWidth + 1

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

# --------------------------------------- main printing function ----------------------------------

def rysuj_zagadke(puzzle1, c,X = 30, Y = 30, box_size = 100, text_box_size = 150):
    
    kategorie = puzzle1.cathegories
    clues = puzzle1.clues
    seed = puzzle1.seed
    
    K_cat = (len(kategorie)) # liczba kategorii
    k_cat = len(kategorie[0][1]) # liczba obiektów z każdej kategorii
    N_rows = K_cat-1
    width = box_size/k_cat

    cm = 20

    c.setLineWidth(2)
    for row in range(N_rows):
        c.rect( X, Y+row*box_size, text_box_size+(row+1)*box_size, box_size)
        c.rect( X+text_box_size+row*box_size, Y+row*box_size, box_size, text_box_size+(N_rows-row)*box_size)
    c.setLineWidth(1)
    for row in range(N_rows):
        for k in range(k_cat):
            c.rect( X, Y+row*box_size, text_box_size+(row+1)*box_size, k*box_size/k_cat)
            c.rect( X+text_box_size+row*box_size, Y+row*box_size, k*box_size/k_cat, text_box_size+(N_rows-row)*box_size)
    
    Xc = 30
    Yc = 830
    odstep = 0.15
    c.setFont("sans-serif", width*0.5)
    clue_order = np.random.choice(range(len(clues)), len(clues), replace=False)
    for i in range(len(clues)):
        rysuj_pytanie(kategorie, clues[clue_order[i]], c, Xc+odstep*width, Yc-width*i*0.5, i, width*0.5)
    
    c.drawString(X+text_box_size+box_size+10, Y, "seed: "+str(seed))
    
    c.setFont("sans-serif", width*0.4)
    c.drawString(450, 10, "Krzysztof Banecki, all rights reserved ©")
    
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