from numpy import unique
from pathlib import Path
from reportlab.pdfgen import canvas
from math import pi, cos, sin

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
pdfmetrics.registerFont(TTFont('default_font', 'DejaVuSans.ttf'))
from reportlab.lib import colors

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

def draw_clues_on_canvas(categories, clue, c, X, Y, no, width):
    normal_font = "default_font"
    special_font = "Times-Bold"
    replace_polish = True
    if funs.do_categories_repeat(categories, with_bar=False):
        add_info = True    # additional (K0) with names in case of repeating names
    else:
        add_info = False
    
    x = X
    text0 = str(no+1)+". "
    c.setFont(normal_font, width)
    c.drawString(x, Y, text0)
    textWidth = stringWidth(text0, normal_font, width) 
    x += textWidth + 1
    
    if clue["typ"]==1:
        if "g1" in clue:
            text1 = "Zaden obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text1 = funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
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
            
            if "g2" in clue:
                text3 = "zadnego obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
            else:
                text3 = funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
            c.setFont(special_font, width)
            c.drawString(x, Y, text3)
        else:
            text2 = " nie pasuje ani do "
            c.setFont(normal_font, width)
            c.drawString(x, Y, text2)
            textWidth = stringWidth(text2, normal_font, width) 
            x += textWidth + 1

            if "g2" in clue:
                text3 = "zadnego obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
            else:
                text3 = funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
            c.setFont(special_font, width)
            c.drawString(x, Y, text3)
            textWidth = stringWidth(text3, special_font, width) 
            x += textWidth + 1

            text4 = " ani do "
            c.setFont(normal_font, width)
            c.drawString(x, Y, text4)
            textWidth = stringWidth(text4, normal_font, width) 
            x += textWidth + 1

            text5 = funs.get_string_name(categories, clue["K2"], clue["i3"], replace_polish, add_info=add_info)
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

                text7 = funs.get_string_name(categories, clue["K2"], clue["i4"], replace_polish, add_info=add_info)
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
        
        if "g3" in clue:
            text4 = "obiekt z Kat."+str(clue["K3"])+"gr."+str(clue["g3"])
        else:
            text4 = funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = "<"
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        
        if "g2" in clue:
            text6 = "obiekt z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text6 = funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        if "g1" in clue:
            text7 = "obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text7 = funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
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
        
        if "g2" in clue:
            text4 = "obiekt z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text4 = funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = " = "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        if "g1" in clue:
            text6 = "obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text6 = funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
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
        
        if "g1" in clue:
            text2 = "obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text2 = funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text2)
        textWidth = stringWidth(text2, special_font, width) 
        x += textWidth + 1
        
        text3 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text3)
        textWidth = stringWidth(text3, normal_font, width) 
        x += textWidth + 1
        
        if "g2" in clue:
            text4 = "obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text4 = funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = ", to "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        if "g3" in clue:
            text6 = "obiekt z Kat."+str(clue["K3"])+"gr."+str(clue["g3"])
        else:
            text6 = funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
        text7 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text7)
        textWidth = stringWidth(text7, normal_font, width) 
        x += textWidth + 1
        
        if "g4" in clue:
            text8 = "obiektu z Kat."+str(clue["K4"])+"gr."+str(clue["g4"])
        else:
            text8 = funs.get_string_name(categories, clue["K4"], clue["i4"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text8)
        
        textWidth = stringWidth(text0, normal_font, width) 
        x = X + textWidth + 1
        
        text9 = "W przeciwnym przypadku "
        c.setFont(normal_font, width)
        c.drawString(x, Y-width, text9)
        textWidth = stringWidth(text9, normal_font, width) 
        x += textWidth + 1
        
        if "g5" in clue:
            text10 = "obiekt z Kat."+str(clue["K5"])+"gr."+str(clue["g5"])
        else:
            text10 = funs.get_string_name(categories, clue["K5"], clue["i5"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y-width, text10)
        textWidth = stringWidth(text10, special_font, width) 
        x += textWidth + 1
        
        text11 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y-width, text11)
        textWidth = stringWidth(text11, normal_font, width) 
        x += textWidth + 1
        
        if "g6" in clue:
            text12 = "obiektu z Kat."+str(clue["K6"])+"gr."+str(clue["g6"])
        else:
            text12 = funs.get_string_name(categories, clue["K6"], clue["i6"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y-width, text12)
    elif clue["typ"]==5:
        if "g1" in clue:
            text2 = "obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text2 = funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text2)
        textWidth = stringWidth(text2, special_font, width) 
        x += textWidth + 1
        
        text3 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text3)
        textWidth = stringWidth(text3, normal_font, width) 
        x += textWidth + 1
        
        if "g2" in clue:
            text4 = "obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text4 = funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = " lub "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        if "g3" in clue:
            text6 = "obiekt z Kat."+str(clue["K3"])+"gr."+str(clue["g3"])
        else:
            text6 = funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
        text7 = " pasuje do "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text7)
        textWidth = stringWidth(text7, normal_font, width) 
        x += textWidth + 1
        
        if "g4" in clue:
            text8 = "obiektu z Kat."+str(clue["K4"])+"gr."+str(clue["g4"])
        else:
            text8 = funs.get_string_name(categories, clue["K4"], clue["i4"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text8)
        textWidth = stringWidth(text8, special_font, width) 
        x += textWidth + 1
        
        text9 = "(alt. nierozł.)"
        c.setFont(normal_font, width*0.7)
        c.drawString(x, Y, text9)
        textWidth = stringWidth(text9, normal_font, width) 
        x += textWidth + 1
#         text1 = "Albo "
#         c.drawString(x, Y, text1)
#         textWidth = stringWidth(text1, normal_font, width) 
#         x += textWidth + 1
        
#         text2 = funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
#         c.setFont(special_font, width)
#         c.drawString(x, Y, text2)
#         textWidth = stringWidth(text2, special_font, width) 
#         x += textWidth + 1
        
#         text3 = " pasuje do "
#         c.setFont(normal_font, width)
#         c.drawString(x, Y, text3)
#         textWidth = stringWidth(text3, normal_font, width) 
#         x += textWidth + 1
        
#         text4 = funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
#         c.setFont(special_font, width)
#         c.drawString(x, Y, text4)
#         textWidth = stringWidth(text4, special_font, width) 
#         x += textWidth + 1
        
#         text5 = " albo "
#         c.setFont(normal_font, width)
#         c.drawString(x, Y, text5)
#         textWidth = stringWidth(text5, normal_font, width) 
#         x += textWidth + 1
        
#         text6 = funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
#         c.setFont(special_font, width)
#         c.drawString(x, Y, text6)
#         textWidth = stringWidth(text6, special_font, width) 
#         x += textWidth + 1
        
#         text7 = " pasuje do "
#         c.setFont(normal_font, width)
#         c.drawString(x, Y, text7)
#         textWidth = stringWidth(text7, normal_font, width) 
#         x += textWidth + 1
        
#         text8 = funs.get_string_name(categories, clue["K4"], clue["i4"], replace_polish, add_info=add_info)
#         c.setFont(special_font, width)
#         c.drawString(x, Y, text8)
#         textWidth = stringWidth(text8, special_font, width) 
#         x += textWidth + 1
        
#         text9 = " (alt. rozł.)"
#         c.setFont(normal_font, width)
#         c.drawString(x, Y, text9)
#         textWidth = stringWidth(text9, normal_font, width) 
#         x += textWidth + 1
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
        
        if "g1" in clue:
            text4 = "obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text4 = funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text4)
        textWidth = stringWidth(text4, special_font, width) 
        x += textWidth + 1
        
        text5 = " jest tuż obok "
        c.setFont(normal_font, width)
        c.drawString(x, Y, text5)
        textWidth = stringWidth(text5, normal_font, width) 
        x += textWidth + 1
        
        if "g2" in clue:
            text6 = "obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text6 = funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        c.setFont(special_font, width)
        c.drawString(x, Y, text6)
        textWidth = stringWidth(text6, special_font, width) 
        x += textWidth + 1
        
def draw_into_rectangle(c, X, Y, text, font, rec_h, rec_w):
    width = rec_h
    length = stringWidth(text, font, width) 
    while length>rec_w*0.94:
        width -= rec_h/100
        length = stringWidth(text, font, width) 
    c.setFont(font, width)
    c.drawString(X, Y, text)
        
# --------------------------------------- main printing function ----------------------------------

def draw_grid(puzzle1, c, X = 30, Y = 30, puzzle_h=400):
    categories = puzzle1.categories
    clues = puzzle1.clues
    seed = puzzle1.seed
    K_cat = puzzle1.K # liczba kategorii
    k_cat = puzzle1.k # liczba obiektów z każdej kategorii
    # puzzle_h - height of the puzzle grid
    
    box_size = puzzle_h/(K_cat+0.5)
    text_box_size = box_size*1.5
    
    N_rows = K_cat-1
    width = box_size/k_cat
    
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
    
    # ------------- typing categories names
    width2 = 10
    
    normal_font = "default_font"
    special_font = "Times-Bold"
    c.setFont(normal_font, width2)
    
    Xc = 430
    if k_cat<=5:
        Ycat = Y+puzzle_h+width2*(k_cat+1)
    else:
        Ycat = Y+puzzle_h+width2*6
        
    x_shift = 0
    for i in range(len(categories)):
        widths = []
        c.setFont(special_font, width2)
        if puzzle1.K>6:
            text0 = "Kat. "+str(i)+":"
        else:
            text0 = "Kategoria "+str(i)+":"
        widths.append( stringWidth(text0, special_font, width2) )
        
        nazwy = [ funs.get_string_name(categories, i, j) for j in range(len(categories[i]['names'])) ]
        c.drawString(X+x_shift, Ycat, text0)
        c.setFont(normal_font, width2)
        for col, name in enumerate(nazwy):
            if k_cat>5 and col>3:
                c.drawString(X+x_shift, Ycat-width2*(col+1), "...")
                widths.append( stringWidth("...", normal_font, width2) )
                break
            if 'groups' in categories[i] and len(unique(categories[i]["groups"]))>1:
                name2 = name+" (gr. "+str(categories[i]["groups"][col])+")"
                c.drawString(X+x_shift, Ycat-width2*(col+1), name2)
                widths.append( stringWidth(name2, normal_font, width2) )
            else:
                c.drawString(X+x_shift, Ycat-width2*(col+1), name)
                widths.append( stringWidth(name, normal_font, width2) )
        x_shift += int(max(widths))+10
            
    
    # ------------- typing categories names into boxes
    
    for i, category in enumerate(categories):
        nazwy = [ str(k) for k in category['names'] ]
        if category['typ']=='numerical':
            nazwy = [ k[:-2] if k.endswith(".0") else k for k in nazwy ]
            if "@" in category['interpretation']:
                a = category['interpretation'].split("@")
                nazwy = [ k.join(a) for k in nazwy ]
        
        miejsce = i+1
        odstep = 0.15
        odstep2 = 0 # only for categories with cross bar text
        
        # if there is a horizontal bar to draw
        if category['cross_bar']!="":
            
            text = category['cross_bar']
            odstep2 = width
            c.saveState()
            c.setLineWidth(2)
            c.setFillColor(colors.white)
            # horizontal bar on the left
            if i!=1:
                if i!=0:
                    c.rect( X, Y+(i-2)*box_size, box_size/k_cat, box_size, fill=1)
                else:
                    c.rect( X, Y+(K_cat-2)*box_size, box_size/k_cat, box_size, fill=1)
            # horizontal bar at the top
            if i!=0:
                c.rect( X+text_box_size+box_size*(i-1), Y+(K_cat-1)*box_size+text_box_size-box_size/k_cat, box_size, box_size/k_cat, fill=1)
            c.restoreState()
            
            inter_width = stringWidth(text, "default_font", width) 
            c.setFont("default_font", min([width, width*(1-odstep)*box_size/inter_width]))
            # horizontal bar text at the top
            if i!=0:
                draw_into_rectangle(c, X+text_box_size+box_size*(i-1)+odstep*width, Y+(K_cat-1)*box_size+text_box_size-box_size/k_cat+odstep*width, text.upper(), "default_font", width, box_size)
            # horizontal bar text on the left
            if i!=1:
                c.saveState()
                c.rotate( 90 )
                if i!=0:
                    draw_into_rectangle(c, Y+(i-2)*box_size+odstep*width, -X+odstep*width-box_size/k_cat, text.upper(), "default_font", width, box_size)
                else:
                    draw_into_rectangle(c, Y+(K_cat-2)*box_size+odstep*width, -X+odstep*width-box_size/k_cat, text.upper(), "default_font", width, box_size)
                c.restoreState()
        
        for i, name in enumerate(nazwy):
            if category['cross_bar']!="":
                space_size = text_box_size-box_size/k_cat
            else:
                space_size = text_box_size
            # rysowanie poziome:
            if miejsce==1:
                draw_into_rectangle(c, X+odstep*width+odstep2, Y+(K_cat-1)*box_size-(i+1)*width+odstep*width, name.upper(), "default_font", width, space_size)
            elif miejsce!=2:
                draw_into_rectangle(c, X+odstep*width+odstep2, Y+(miejsce-2)*box_size-(i+1)*width+odstep*width, name.upper(), "default_font", width, space_size)
            c.saveState()
            # rysowanie pionowe:
            c.rotate( 90 )
            if miejsce==2:
                draw_into_rectangle(c, Y+(K_cat-1)*box_size+odstep*width, -X-text_box_size-(i+1)*width+odstep*width, name.upper(), "default_font", width, space_size)
            elif miejsce!=1:
                draw_into_rectangle(c, Y+(K_cat-1)*box_size+odstep*width, -X-text_box_size-(miejsce-2)*box_size-(i+1)*width+odstep*width, name.upper(), "default_font", width, space_size)

            c.restoreState()
    
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
    
    if puzzle1.diff<1:
        n = 1
    elif puzzle1.diff<3:
        n = 2
    elif puzzle1.diff<5:
        n = 3
    else:
        n = 4
        
    for i in range(n):
        star(c, X+box_size*1.5-15-i*25, Y+puzzle_h-box_size*1.5+15, 10)
    
    # ------------ drawing grid
    
    draw_grid(puzzle1=puzzle1, c=c, X=X, Y=Y, puzzle_h=puzzle_h)
    
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
    
    c.setFont("default_font", width_clue)
    additional_rows = 0
    for i in range(len(clues)):
        draw_clues_on_canvas(categories, clues[i], c, Xc+odstep*width_clue, Yc-width_clue*(i+additional_rows), i, width_clue)
        if clues[i]["typ"]==4:
            additional_rows += 1
    
    # ------------- drawing footnote and info
    width_foot = 8
    c.setFont("default_font", width_foot)
    
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

    c.drawString(430, 10, "Krzysztof Banecki, all rights reserved ©")
    
    # ------------- drawing solution
    c.saveState()
    c.rotate( 270 )
    X_sol = -Y-350
    Y_sol = 570
    width_sol = 8
    
    if funs.do_categories_repeat(puzzle1.categories, with_bar=False):
        add_info = True    # additional (K0) with names in case of repeating names
    else:
        add_info = False
    
    c.setFont("Times-Bold", width_sol)
    c.drawString(X_sol, Y_sol, "Solution:")
    c.setFont("default_font", width_sol)
    for i in range(k_cat):
        linijka = funs.get_string_name(categories, 0, i, replace_polish=False, add_info=add_info)
        for k2 in range(1, K_cat):
            for j in range(k_cat):
                if puzzle1.get_grid_value(0, i, k2, j)==1:
                    break
            linijka += " ~ "+funs.get_string_name(categories, k2, j, replace_polish=False)
        c.drawString(X_sol, Y_sol-(i+1)*width_sol,linijka)
    
    c.restoreState()
    
def draw_sign(puzzle1, c, sign, K1, i1, K2, i2, X=30, Y=30, red=False, puzzle_h=400):
    if K1>K2:
        K1u = K2
        K2u = K1
        i1u = i2
        i2u = i1
    else:
        K1u = K1
        K2u = K2
        i1u = i1
        i2u = i2
        
    box_size = puzzle_h/(puzzle1.K+0.5)
    k = puzzle1.k
    K = puzzle1.K
    margin = 0.13
    if K1u==0:
        Xu = X+box_size*(1.5+K2u-1)+box_size/k*i2u + box_size/k*margin
        Yu = Y+box_size*(K-1)-box_size/k*(i1u+1) + box_size/k*margin
    else:
        Xu = X+box_size*(1.5+K1u-1)+box_size/k*i1u + box_size/k*margin
        Yu = Y+box_size*(K2u-1)-box_size/k*(i2u+1) + box_size/k*margin
    
    c.setFont("default_font", box_size/k)
    if red:
        c.setFillColorRGB(1,0,0)
    c.drawString(Xu, Yu, sign)
    c.setFillColorRGB(0,0,0)
    
def draw_solution(puzzle1, c, X=30, Y=30, puzzle_h=400):
    width_krok = 20
    signs_list = []
    prev_val = puzzle1.solution.split(";")[0].split(",")[-1]
    draw_grid(puzzle1=puzzle1, c=c, X=X, Y=Y)
    krok = 1
    c.setFont("default_font", width_krok)
    c.drawString(30, 800, "Krok "+str(krok)+":")
    
    for step in puzzle1.solution.split(";")[:-1]:
        step2 = step.split(",")
        if step2[0]=='1':
            step2[0] = "O"
        else:
            step2[0] = "X"
        #print(prev_val , step2[-1])
        if not(step2[-1] in ["conc1","conc2"] and prev_val in ["conc1","conc2"]) and step2[-1]!=prev_val:
            c.showPage()
            krok += 1
            c.setFont("default_font", width_krok)
            c.drawString(30, 800, "Krok "+str(krok)+":")
            
            draw_grid(puzzle1=puzzle1, c=c, X=X, Y=Y)
            for step3 in signs_list:
                draw_sign(puzzle1, c, step3[0], int(step3[1]), int(step3[2]), int(step3[3]), int(step3[4]), X=X, Y=Y, red=False)
        draw_sign(puzzle1, c, step2[0], int(step2[1]), int(step2[2]), int(step2[3]), int(step2[4]), X=X, Y=Y, red=True)
        signs_list.append(step2)
        prev_val = step2[-1]
        
        Xc = 20
        Yc = 600
        code = step2[-1]
        width2 = 10
        c.setFont("default_font", width2)
        if code[:4]=='conc':
            text1 = " Wynika to z zasady:"
            if code[-1]=='1':
                line2 = "\"Gdzieś w jest znak \'O\'\" lub \"Jedyne wolne miejsce w wierszu/kolumnie\""
            elif code[-1]=='2':
                line2 = "\"Gdzieś w jest znak \'O\'\" lub \"Jedyne wolne miejsce w wierszu/kolumnie\""
            elif code[-1]=='3':
                line2 = "\"Gdzieś na planszy jest \'O\'. Uzgodnienie znaków \'X\' dwóch połączonych obiektów.\""
            elif code[-1]=='4':
                line2 = "\"Wykluczenie tego pola ze względu na to, że dane obiekty mają wzajemnie wykluczające się wiersze/kolumny.\""
            elif code[-1]=='5':
                line2 = "\"2/3 wiersze/kolumny w boxie mają dostępne 2/3 pola dla tych samych kolumn/wierszy."
                line3 = "Stąd wykluczenie tych kolumn/wierszy dla innych wierszy/kolumn\""
                c.drawString(Xc, Yc-2*width2, line3)
            c.setFillColorRGB(1,0,0)
            c.drawString(Xc, Yc, text1)
            c.setFillColorRGB(0,0,0)
            c.drawString(Xc, Yc-width2, line2)
        elif code=='contr':
            text1 = " Wynika to z tego, że:"
            line2 = "\"Wstawienie \'O\' w to pole skutkowałoby sprzecznością. Stąd wstaw \'X\'.\""
            c.setFillColorRGB(1,0,0)
            c.drawString(Xc, Yc, text1)
            c.setFillColorRGB(0,0,0)
            c.drawString(Xc, Yc-width2, line2)
        elif code[:4]=='clue':
            text1 = " Wynika to ze wskazówki:"
            n = int(code.split("_")[-1])
            c.setFillColorRGB(1,0,0)
            c.drawString(Xc, Yc, text1)
            c.setFillColorRGB(0,0,0)
            draw_clues_on_canvas(puzzle1.categories, puzzle1.clues[n], c, Xc, Yc-width2, no=n, width=width2)
    c.showPage()  
            
            
            
            
            
            
            
