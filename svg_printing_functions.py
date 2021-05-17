import svgwrite
import numpy as np
from math import pi, cos, sin
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
pdfmetrics.registerFont(TTFont('default_font', 'DejaVuSans.ttf'))

import generating_categories_functions as funs
from puzzle_class import puzzle
  
# Coordinate center is in the top-left corner.
# The size of the page is assumed: 616 x 870.
    
def star(dwg, xcenter, ycenter, radius):
    angle = (2*pi)*2/5.0
    startangle = pi/2.0
    pre_x = xcenter
    pre_y = ycenter-radius
    for vertex in range(5):
        nextangle = angle*(vertex+1)+startangle
        x = xcenter + radius*cos(nextangle)
        y = ycenter - radius*sin(nextangle)
        dwg.add(dwg.line( (pre_x, pre_y), (x, y),
            stroke="#000",
            fill="none",
            stroke_width=1)
        )
        pre_x = x
        pre_y = y

def draw_clues_on_canvas(categories, clue, dwg, X, Y, no, width):
    replace_polish = False
    if funs.do_categories_repeat(categories, with_bar=False):
        add_info = True    # additional (K0) with names in case of repeating names
    else:
        add_info = False
    text0 = str(no+1)+". "
    text1 = "error"
    if clue["typ"]==1:
        if "g1" in clue:
            text0 += "Zaden obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        if "i3" not in clue:
            text0 += " nie pasuje do "
            if "g2" in clue:
                text0 += "zadnego obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
            else:
                text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        else:
            text0 += " nie pasuje ani do "
            if "g2" in clue:
                text0 += "zadnego obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
            else:
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
        if "g3" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K3"])+"gr."+str(clue["g3"])
        else:
            text0 += funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)    
        text0 += "<"
        if "g2" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        text0 += "<"
        if "g1" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
    elif clue["typ"]==3:
        text0 += "Pod względem "
        text0 += "Kategorii "+str(clue["K6"])
        text0 += " zachodzi: "
        if "g2" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        text0 += " = "
        if "g1" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        if str(clue["diff"]).endswith(".0"):
            diff = str(clue["diff"])[:-2]
        else:
            diff = str(clue["diff"])
        text0 += " "+clue["oper"]+" "+diff
    elif clue["typ"]==4:
        text0 += "Jeśli "
        if "g1" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        if "g2" in clue:
            text0 += "jakiegos z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        text0 += ", to "
        if "g3" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K3"])+"gr."+str(clue["g3"])
        else:
            text0 += funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        if "g4" in clue:
            text0 += "jakiegos obiektu z Kat."+str(clue["K4"])+"gr."+str(clue["g4"])
        else:
            text0 += funs.get_string_name(categories, clue["K4"], clue["i4"], replace_polish, add_info=add_info)
        
        text1 = "W przeciwnym przypadku "
        if "g5" in clue:
            text1 += "jakis obiekt z Kat."+str(clue["K5"])+"gr."+str(clue["g5"])
        else:
            text1 += funs.get_string_name(categories, clue["K5"], clue["i5"], replace_polish, add_info=add_info)
        text1 += " pasuje do "
        if "g6" in clue:
            text1 += "jakiegos obiektu z Kat."+str(clue["K6"])+"gr."+str(clue["g6"])
        else:
            text1 += funs.get_string_name(categories, clue["K6"], clue["i6"], replace_polish, add_info=add_info)
    elif clue["typ"]==5:
        if "g1" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        if "g2" in clue:
            text0 += "jakiegos obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
        text0 += " lub "
        if "g3" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K3"])+"gr."+str(clue["g3"])
        else:
            text0 += funs.get_string_name(categories, clue["K3"], clue["i3"], replace_polish, add_info=add_info)
        text0 += " pasuje do "
        if "g4" in clue:
            text0 += "jakiegos obiektu z Kat."+str(clue["K4"])+"gr."+str(clue["g4"])
        else:
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
        if "g1" in clue:
            text0 += "jakis obiekt z Kat."+str(clue["K1"])+"gr."+str(clue["g1"])
        else:
            text0 += funs.get_string_name(categories, clue["K1"], clue["i1"], replace_polish, add_info=add_info)
        text0 += " jest tuż obok "
        if "g2" in clue:
            text0 += "jakiegos obiektu z Kat."+str(clue["K2"])+"gr."+str(clue["g2"])
        else:
            text0 += funs.get_string_name(categories, clue["K2"], clue["i2"], replace_polish, add_info=add_info)
    dwg.add(dwg.text(text0,
        insert=(X, Y),
        stroke='none',
        fill='black',
        font_size=width)
    )
    if clue["typ"]==4:
        dwg.add(dwg.text(text1,
            insert=(X, Y+width),
            stroke='none',
            fill='black',
            font_size=width)
        )

def textwidth(text, fontsize=14, fname="undefined.svg"):
    return stringWidth(text, 'default_font', fontsize)
    
def draw_into_rectangle(dwg, X, Y, text, rec_h, rec_w, angle=0, fname="undefined.svg"):
    width = rec_h
    length = textwidth(text, width, fname=fname) 
    while length>rec_w*0.88:
        width -= rec_h/100
        length = textwidth(text, width, fname=fname) 
    dwg.add(dwg.text(text,
        insert=(X, Y),
        stroke='none',
        font_size=width,
        transform='rotate('+str(angle)+','+str(X)+','+str(Y)+')')
    )
        
def draw_grid(puzzle1, dwg, X = 30, Y = 30, puzzle_h=400, fname="undefined.svg"):
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
    for row in range(N_rows):
        dwg.add(dwg.rect((X, 870-Y-(row+1)*box_size), (text_box_size+(row+1)*box_size, box_size),
            stroke='black', stroke_width=2, fill='none')
        )
        dwg.add(dwg.rect((X+text_box_size+row*box_size, 870-Y-(K_cat+0.5)*box_size), (box_size, text_box_size+(N_rows-row)*box_size),
            stroke='black', stroke_width=2, fill='none')
        )
    for row in range(N_rows):
        for k in range(k_cat):
            dwg.add(dwg.rect((X, 870-Y-(row+1)*box_size), (text_box_size+(row+1)*box_size, k*box_size/k_cat),
                stroke='black', stroke_width=1, fill='none')
            )
            dwg.add(dwg.rect((X+text_box_size+row*box_size, 870-Y-(K_cat+0.5)*box_size), (k*box_size/k_cat, text_box_size+(N_rows-row)*box_size),
                stroke='black', stroke_width=1, fill='none')
            )
    
    # ------------- typing categories names
    width2 = 10
    
    Xc = 430
    if k_cat<=5:
        Ycat = Y+puzzle_h+width2*(k_cat+1)
    else:
        Ycat = Y+puzzle_h+width2*6
        
    x_shift = 0
    for i in range(len(categories)):
        widths = []
        if puzzle1.K>6:
            text0 = "Kat. "+str(i)+":\n"
        else:
            text0 = "Kategoria "+str(i)+":\n"
        widths.append( textwidth(text0, width2, fname=fname) )
        
        nazwy = [ funs.get_string_name(categories, i, j) for j in range(len(categories[i]['names'])) ]
        dwg.add(dwg.text(text0,
            insert=(X+x_shift, 870-Ycat),
            stroke='black',
            font_size=width2
        ))
        for col, name in enumerate(nazwy):
            if k_cat>5 and col>3:
                dwg.add(dwg.text("...",
                    insert=(X+x_shift, 870-Ycat+width2*(col+1)),
                    stroke='none',
                    font_size=width2
                ))
                widths.append( textwidth("...", width2, fname=fname) )
                break
            if 'groups' in categories[i] and len(np.unique(categories[i]["groups"]))>1:
                name2 = name+" (gr. "+str(categories[i]["groups"][col])+")"
                dwg.add(dwg.text(name2,
                    insert=(X+x_shift, 870-Ycat+width2*(col+1)),
                    stroke='none',
                    font_size=width2
                ))
                widths.append( textwidth(name2, width2, fname=fname) )
            else:
                dwg.add(dwg.text(name,
                    insert=(X+x_shift, 870-Ycat+width2*(col+1)),
                    stroke='none',
                    font_size=width2
                ))
                widths.append( textwidth(name, width2, fname=fname) )
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
        odstep2 = 0 # only for categories with horizontal bars
        
        # if there is a horizontal bar to draw
        if category['cross_bar']!="":
            
            text = category['cross_bar']
            odstep2 = width
            
            # cross bar on the left
            if i!=1:
                if i!=0:
                    dwg.add(dwg.rect((X, 870-Y-(i-1)*box_size), (box_size/k_cat, box_size),
                        stroke='black', stroke_width=2, fill='white')
                    )
                else:
                    dwg.add(dwg.rect((X, 870-Y-(K_cat-1)*box_size), (box_size/k_cat, box_size),
                        stroke='black', stroke_width=2, fill='white')
                    )
            # cross bar at the top
            if i!=0:
                dwg.add(dwg.rect((X+text_box_size+box_size*(i-1), 870-Y-(K_cat-1)*box_size-text_box_size), (box_size, box_size/k_cat),
                    stroke='black', stroke_width=2, fill='white')
                )
            
            inter_width = textwidth(text, width, fname=fname) 
            # cross bar text at the top
            if i!=0:
                draw_into_rectangle(dwg, X+text_box_size+box_size*(i-1)+odstep*width, 870-Y-(K_cat-1)*box_size-text_box_size+box_size/k_cat-odstep*width, text.upper(), width, box_size, fname=fname)
            # cross bar text on the left
            if i!=1:
                if i!=0:
                    draw_into_rectangle(dwg, X+box_size/k_cat-odstep*width, 870-Y-(i-2)*box_size-odstep*width, text.upper(), width, box_size, angle=270, fname=fname)
                else:
                    draw_into_rectangle(dwg, X+box_size/k_cat-odstep*width, 870-Y-(K_cat-2)*box_size-odstep*width, text.upper(), width, box_size, angle=270, fname=fname)
        
        for i, name in enumerate(nazwy):
            if category['cross_bar']!="":
                space_size = text_box_size-box_size/k_cat
            else:
                space_size = text_box_size
            # rysowanie poziome:
            if miejsce==1:
                draw_into_rectangle(dwg, X+odstep*width+odstep2, 870-Y-(K_cat-1)*box_size+(i+1)*width-odstep*width, name.upper(), width, space_size, fname=fname)
            elif miejsce!=2:
                draw_into_rectangle(dwg, X+odstep*width+odstep2, 870-Y-(miejsce-2)*box_size+(i+1)*width-odstep*width, name.upper(), width, space_size, fname=fname)
            # rysowanie pionowe:
            if miejsce!=1:
                draw_into_rectangle(dwg, X+text_box_size+(i+1)*width-odstep*width+(miejsce-2)*box_size, 870-Y-(K_cat-1)*box_size-odstep*width, name.upper(), width, space_size, angle=270, fname=fname)

            
def draw_on_canvas(puzzle1, dwg, fname="undefined.svg", X = 30, Y = 30, puzzle_h = 400):
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
        star(dwg, X+box_size*1.5-15-i*25, 870-Y-puzzle_h+text_box_size-15, 10)
    
    # ------------ drawing grid
    draw_grid(puzzle1=puzzle1, dwg=dwg, X=X, Y=Y, puzzle_h=puzzle_h, fname=fname)
    
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
        draw_clues_on_canvas(categories, clues[i], dwg, Xc+odstep*width_clue, 840-Yc+width_clue*(i+additional_rows), i, width_clue)
        if clues[i]["typ"]==4:
            additional_rows += 1
    
    # ------------- drawing info
    width_foot = 8
    dwg.add(dwg.text("diff: "+str(puzzle1.diff),
        insert=(X+text_box_size+box_size+10, 870-Y-3*width_foot ),
        stroke='none',
        font_size=width_foot
    ))
    
    if puzzle1.is_grid_contradictory():
        dwg.add(dwg.text("Contradictory: "+str(puzzle1.is_grid_contradictory()),
            insert=(X+text_box_size+box_size+10, 870-Y-2*width_foot),
            stroke='red',
            font_size=width_foot
        ))
    else:
        dwg.add(dwg.text("Contradictory: "+str(puzzle1.is_grid_contradictory()),
            insert=(X+text_box_size+box_size+10, 870-Y-2*width_foot),
            stroke='none',
            font_size=width_foot
        ))
    
    if not puzzle1.is_grid_completed():
        dwg.add(dwg.text("Solvable: "+str(puzzle1.is_grid_completed()),
            insert=(X+text_box_size+box_size+10, 870-Y-width_foot),
            stroke='red',
            font_size=width_foot
        ))
    else:
        dwg.add(dwg.text("Solvable: "+str(puzzle1.is_grid_completed()),
            insert=(X+text_box_size+box_size+10, 870-Y-width_foot),
            stroke='none',
            font_size=width_foot
        ))
    dwg.add(dwg.text("Seed: "+str(seed),
        insert=(X+text_box_size+box_size+10, 870-Y),
        stroke='none',
        font_size=width_foot
    ))
    
    dwg.add(dwg.text("Krzysztof Banecki, all rights reserved ©",
        insert=(450, 870-10),
        stroke='none',
        font_size=width_foot
    ))
            
    # ------------- drawing solution
    X_sol = 450
    Y_sol = 350
    width_sol = 8
    
    if funs.do_categories_repeat(puzzle1.categories, with_bar=False):
        add_info = True    # additional (K0) with names in case of repeating names
    else:
        add_info = False
    
    sol_text = "Solution:"
    dwg.add(dwg.text(sol_text,
        insert=(X_sol, 870-Y_sol),
        stroke='none',
        font_size=width_sol
    ))
    for i in range(k_cat):
        linijka = funs.get_string_name(categories, 0, i, replace_polish=False, add_info=add_info)
        for k2 in range(1, K_cat):
            for j in range(k_cat):
                if puzzle1.get_grid_value(0, i, k2, j)==1:
                    break
            linijka += " ~ "+funs.get_string_name(categories, k2, j, replace_polish=False)
        dwg.add(dwg.text(linijka,
            insert=(X_sol, 870-Y_sol+(i+1)*width_sol),
            stroke='none',
            font_size=width_sol
        ))
    
    
    
    