import drawSvg as draw
import numpy as np
from math import pi, cos, sin

import generating_categories_functions as funs
from puzzle_class import puzzle
    
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

def textwidth(text, fontsize=14, fname="undefined.svg"):
    try:
        import cairo
    except:
        return len(text) * fontsize
    surface = cairo.SVGSurface(fname, 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
    return width
    
def draw_into_rectangle(c, X, Y, text, rec_h, rec_w, angle=0, fname="undefined.svg"):
    width = rec_h
    length = textwidth(text, width, fname=fname) 
    while length>rec_w*0.88:
        width -= rec_h/100
        length = textwidth(text, width, fname=fname) 
    c.append(draw.Text(text, width, X, Y, fill='black', transform='rotate('+str(angle)+')')) 
        
def draw_grid(puzzle1, c, X = 30, Y = 30, puzzle_h=400, fname="undefined.svg"):
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
        c.append(draw.Rectangle( X, Y+row*box_size, text_box_size+(row+1)*box_size, box_size, fill='none', stroke_width=2, stroke='black'))
        c.append(draw.Rectangle( X+text_box_size+row*box_size, Y+row*box_size, box_size, text_box_size+(N_rows-row)*box_size, fill='none', stroke_width=2, stroke='black'))
    for row in range(N_rows):
        for k in range(k_cat):
            c.append(draw.Rectangle( X, Y+row*box_size, text_box_size+(row+1)*box_size, k*box_size/k_cat, fill='none', stroke_width=1, stroke='black'))
            c.append(draw.Rectangle( X+text_box_size+row*box_size, Y+row*box_size, k*box_size/k_cat, text_box_size+(N_rows-row)*box_size, fill='none', stroke_width=1, stroke='black'))
    
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
        
        nazwy = [ funs.get_string_name(categories, i, j) for j in range(len(categories[i][1])) ]
        for col, name in enumerate(nazwy):
            if k_cat>5 and col>3:
                text0 += "...\n"
                widths.append( textwidth("...", width2, fname=fname) )
                break
            text0 += name+"\n"
            widths.append( textwidth(name, width2, fname=fname) )
        c.append(draw.Text( text0, width2, X+x_shift, Ycat ))
        x_shift += int(np.max(widths))+10
        
    
    # ------------- typing categories names into boxes
    
    for i, category in enumerate(categories):
        nazwy = [ str(k) for k in category[1] ]
        if category[0]=='numerical':
            nazwy = [ k[:-2] if k.endswith(".0") else k for k in nazwy ]
            if "@" in category[3]:
                a = category[3].split("@")
                nazwy = [ k.join(a) for k in nazwy ]
        
        miejsce = i+1
        odstep = 0.15
        odstep2 = 0 # only for categories with horizontal bars
        
        # if there is a horizontal bar to draw
        if (category[0]=='numerical' and category[4]!="") or (category[0]!='numerical' and category[2]!=""):
            
            if category[0]=='numerical':
                text = category[4]
            else:
                text = category[2]
            odstep2 = width
            
            # horizontal bar on the left
            if i!=1:
                if i!=0:
                    c.append(draw.Rectangle( X, Y+(i-2)*box_size, box_size/k_cat, box_size, fill='white', stroke_width=2, stroke='black'))
                else:
                    c.append(draw.Rectangle( X, Y+(K_cat-2)*box_size, box_size/k_cat, box_size, fill='white', stroke_width=2, stroke='black'))
            # horizontal bar at the top
            if i!=0:
                c.append(draw.Rectangle( X+text_box_size+box_size*(i-1), Y+(K_cat-1)*box_size+text_box_size-box_size/k_cat, box_size, box_size/k_cat, fill='white', stroke_width=2, stroke='black'))
            
            inter_width = textwidth(text, width, fname=fname) 
            # horizontal bar text at the top
            if i!=0:
                draw_into_rectangle(c, X+text_box_size+box_size*(i-1)+odstep*width, Y+(K_cat-1)*box_size+text_box_size-box_size/k_cat+odstep*width, text, width, box_size, fname=fname)
            # horizontal bar text on the left
            if i!=1:
                if i!=0:
                    draw_into_rectangle(c, Y+(i-2)*box_size+odstep*width, -X+odstep*width-box_size/k_cat, text, width, box_size, angle=270, fname=fname)
                else:
                    draw_into_rectangle(c, Y+(K_cat-2)*box_size+odstep*width, -X+odstep*width-box_size/k_cat, text, width, box_size, angle=270, fname=fname)
        
        for i, name in enumerate(nazwy):
            if (category[0]=='numerical' and category[4]!="") or (category[0]!='numerical' and category[2]!=""):
                space_size = text_box_size-box_size/k_cat
            else:
                space_size = text_box_size
            # rysowanie poziome:
            if miejsce==1:
                draw_into_rectangle(c, X+odstep*width+odstep2, Y+(K_cat-1)*box_size-(i+1)*width+odstep*width, name, width, space_size, fname=fname)
            elif miejsce!=2:
                draw_into_rectangle(c, X+odstep*width+odstep2, Y+(miejsce-2)*box_size-(i+1)*width+odstep*width, name, width, space_size, fname=fname)
            # rysowanie pionowe:
            if miejsce==2:
                draw_into_rectangle(c, Y+(K_cat-1)*box_size+odstep*width, -X-text_box_size-(i+1)*width+odstep*width, name, width, space_size, angle=270, fname=fname)
            elif miejsce!=1:
                draw_into_rectangle(c, Y+(K_cat-1)*box_size+odstep*width, -X-text_box_size-(miejsce-2)*box_size-(i+1)*width+odstep*width, name, width, space_size, angle=270, fname=fname)

            
def draw_on_canvas(puzzle1, c, fname="undefgewgwegined.svg", X = 30, Y = 30, puzzle_h = 400):
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
    draw_grid(puzzle1=puzzle1, c=c, X=X, Y=Y, puzzle_h=puzzle_h, fname=fname)
    
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
    
    # ------------- drawing info
    width_foot = 8
    
    c.append(draw.Text( "diff: "+str(puzzle1.diff), width_foot, X+text_box_size+box_size+10, Y+3*width_foot ))
    
    if puzzle1.is_grid_contradictory():
        c.append(draw.Text( "Contradictory: "+str(puzzle1.is_grid_contradictory()), width_foot, X+text_box_size+box_size+10, Y+2*width_foot,  fill='red' ))
    else:
        c.append(draw.Text(  "Contradictory: "+str(puzzle1.is_grid_contradictory()), width_foot, X+text_box_size+box_size+10, Y+2*width_foot, fill='black' ))

    
    if not puzzle1.is_grid_completed():
        c.append(draw.Text( "Solvable: "+str(puzzle1.is_grid_completed()), width_foot, X+text_box_size+box_size+10, Y+width_foot, fill='red' ))
    else:
        c.append(draw.Text( "Solvable: "+str(puzzle1.is_grid_completed()), width_foot, X+text_box_size+box_size+10, Y+width_foot, fill='black' ))
    
    c.append(draw.Text( "seed: "+str(seed), width_foot, X+text_box_size+box_size+10, Y ))

    c.append(draw.Text( "Krzysztof Banecki, all rights reserved ©", width_foot, 450, 10 ))
    
    # ------------- drawing solution
    X_sol = 450
    Y_sol = 350
    width_sol = 8
    
    if funs.do_categories_repeat(puzzle1.categories, with_bar=False):
        add_info = True    # additional (K0) with names in case of repeating names
    else:
        add_info = False
    
    sol_text = "Solution:\n"
    for i in range(k_cat):
        linijka = funs.get_string_name(categories, 0, i, replace_polish=False, add_info=add_info)
        for k2 in range(1, K_cat):
            for j in range(k_cat):
                if puzzle1.get_grid_value(0, i, k2, j)==1:
                    break
            linijka += " ~ "+funs.get_string_name(categories, k2, j, replace_polish=False)
        sol_text += linijka+"\n"
    c.append(draw.Text( sol_text, width_sol, X_sol, Y_sol-(i+1)*width_sol ))
    
    
    
    