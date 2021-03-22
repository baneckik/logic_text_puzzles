from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from os import path
import copy
from functools import partial
from reportlab.pdfgen import canvas
import drawSvg

import numpy as np
from puzzle_class import puzzle
import generating_categories_functions as funs
import pdf_printing_functions as pdf_funs
import svg_printing_functions as svg_funs

window = Tk()
window.geometry('700x800')
window.title("Text puzzle generator v1.2")

def clicked_ok():
	choice_int = choice.get()
	if choice_int==1:
		seed = np.random.randint(0,100000000)
	elif choice_int==2:
		try:
			seed = int(txt.get())
		except:
			messagebox.showwarning('Warning', 'Seed must be a number!')
			return
		if seed<0:
			messagebox.showwarning('Warning', 'Seed must be an integer greater or equal to 3!')
			return
	elif choice_int==3:
		seed = np.random.randint(0,100000000)
        
	else:
		messagebox.showwarning('Warning', 'Decide what you want to do first!')
		return
		
	try:
		K = int(txt4.get())
	except:
		messagebox.showwarning('Warning', 'Number of categories must be an integer!')
		txt4.focus()
		return
	try:
		k = int(txt5.get())
	except:
		messagebox.showwarning('Warning', 'Number of objects in each category must be an integer!')
		txt5.focus()
		return
	
	if K<3:
		messagebox.showwarning('Warning', 'Number of categories must be an integer greater or equal to 3!')
		txt4.focus()
		return
	if k<3:
		messagebox.showwarning('Warning', 'Number of objects in each category must be an integer greater or equal to 3!')
		txt5.focus()
		return
	btn_OK.configure(state='disabled')
    
	btn['state'] = 'normal'
	btn.grid()

def clicked_gen():
	seed = np.random.randint(0,100000000)
	K = int(txt4.get())
	k = int(txt5.get())
    
	btn.configure(state='disabled')
	btn_OK.configure(state='disabled')
	lbl6.grid(row=6, column=0)
	bar.grid(row=7, column=0)
	
	percent = 0
	lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
	bar['value'] = percent
	window.update()
	
	print("------------------ generating started ------------------")
    
	# ----------------- Generating --------------
	
	puzzle1 = puzzle(K, k)
	#puzzle1.generate(seed, trace=True)
	
	puzzle1.set_seed(seed)
	puzzle1.draw_categories()
	puzzle1.print_info()
	i_max = 100
	for i in range(i_max):
		puzzle1.clear_grid()
		puzzle1.clues = []
		puzzle1.draw_clues()
		if puzzle1.is_grid_completed() and not puzzle1.is_grid_contradictory():
			break
	percent = 5
	lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
	bar['value'] = percent
	window.update()
	
	bar_N = len(puzzle1.clues)+5
	
	puzzle1.print_info()
	
	# ---------------- clues restriction -----------------
	
	clues_copy = copy.deepcopy(puzzle1.clues)
	to_restrict = []
        
	clues1 = [ i for i, clue in enumerate(clues_copy) if clue["typ"]==1 ]
	clue_order = np.random.choice(clues1, len(clues1), replace=False)
	trace_i = 1
	trace_clue_count = len(puzzle1.clues)
	for i in clue_order:
		clues1_restricted = [ j for j in clues1 if j!=i ]
		puzzle1.clear_grid()
		puzzle1.clues = [ clue for j, clue in enumerate(clues_copy) if j in clues1_restricted or not j in clue_order ]
		puzzle1.try_to_solve()
		if puzzle1.is_grid_completed() and not puzzle1.is_grid_contradictory():
			to_restrict.append(i)
			clues1 = clues1_restricted
			print("Restricting clue "+str(trace_i)+"/"+str(trace_clue_count)+" finished, type: 1 OUT")
			trace_i += 1
		else:
			print("Restricting clue "+str(trace_i)+"/"+str(trace_clue_count)+" finished, type: 1")
			trace_i += 1
		percent += int(np.floor(95/bar_N))
		lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
		bar['value'] = percent
		window.update()
	
	clues_other = [ i for i, clue in enumerate(clues_copy) if clue["typ"]!=1 ]
	clue_order = np.random.permutation(clues_other)
	for i in clue_order:
		clues_restricted = [ j for j in clues_other if j!=i ]
		puzzle1.clear_grid()
		puzzle1.clues = [ clue for j, clue in enumerate(clues_copy) if j in clues_restricted or j in clues1 ]
		puzzle1.try_to_solve()
		if puzzle1.is_grid_completed() and not puzzle1.is_grid_contradictory():
			to_restrict.append(i)
			clues_other = clues_restricted
			print("Restricting clue "+str(trace_i)+"/"+str(trace_clue_count)+" finished, type: "+str(clues_copy[i]["typ"])+" OUT")
			trace_i += 1
		else:
			print("Restricting clue "+str(trace_i)+"/"+str(trace_clue_count)+" finished, type: "+str(clues_copy[i]["typ"]))
			trace_i += 1
		percent += int(np.floor(95/bar_N))
		lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
		bar['value'] = percent
		window.update()

	puzzle1.clues = [ clue for j, clue in enumerate(clues_copy) if not j in to_restrict ]
	puzzle1.clues = list(np.random.permutation(puzzle1.clues))
	#percent = int(np.floor(5+95/bar_N*(bar_N-5)))
	#lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
	#bar['value'] = percent
	#window.update()
	
	# ---------------- difficulty assessment -------------------
    
	print("Final difficulty assessment...")
	N = 5
	diffs = []
	best_solution = ""
	lowest_diff = 1000000
	for n in range(N):
		puzzle1.clear_grid()
		puzzle1.diff = 0
		
		puzzle1.solution = ""
		puzzle1.try_to_solve(collect_solution=True)
        
		if puzzle1.diff<lowest_diff:
			best_solution = puzzle1.solution
			lowest_diff = puzzle1.diff
		diffs.append(puzzle1.diff)
		
		percent = int(np.floor(5+95/bar_N*(bar_N-4+n)))
		lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
		bar['value'] = percent
		window.update()
	puzzle1.solution = best_solution
	puzzle1.diff = round(np.mean(diffs),2)
	
	puzzle1.print_info()
	
	percent = 100
	lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
	bar['value'] = percent
	
	lbl7.grid(row=8, column=0)
	lbl7.configure(text="You drew a puzzle from seed="+str(seed)+" with estimated difficulty: "+str(puzzle1.diff)+".\nYou may now alter category names if you wish. \nWhen you are done you can print your puzzle to pdf.\n@ is a special symbol for the place where numerical data is inserted.")
	
	# -------------------- writing categories out -------------------
	
	cat_cats.clear()
	num_cats.clear()
    
	for j, cat in enumerate(puzzle1.categories):
		entries = []
		if cat[0]=='categorical':
			code = ' (CATEGORICAL)'
		elif cat[0]=='ordinal':
			code = ' (ORDINAL)'
		else:
			code = ' (NUMERICAL)'
            
		if cat[0]=='categorical' or cat[0]=='ordinal':
			l = Label(cat_frame, text="Category "+str(j)+code+":", font=(std_font, std_font_size//2, 'bold'))
			l.grid(row=0, column=len(cat_cats))
			entries.append(l)
			for i in range(k):
				v = StringVar(cat_frame, value=cat[1][i])
				e = Entry(cat_frame, textvariable=v)
				e.grid(row=i+1, column=len(cat_cats))
				entries.append(e)
			l = Label(cat_frame, text="cross bar text (optional):", font=(std_font, std_font_size//2))
			l.grid(row=puzzle1.k+1, column=len(cat_cats))
			entries.append(l)
			v = StringVar(cat_frame, value=cat[2])
			e = Entry(cat_frame, textvariable=v)
			e.grid(row=puzzle1.k+2, column=len(cat_cats))
			entries.append(e)
			cat_cats.append(entries)
            
		elif cat[0]=='numerical':
			l = Label(num_frame, text="Category "+str(j)+code+":", font=(std_font, std_font_size//2, 'bold'))
			l.grid(row=0, column=len(num_cats))
			
			if cat[5]!="ascending":
				seq_text = cat[5]+" sequence:"
			else:
				seq_text = "irregular sequence:"
			l2 = Label(num_frame, text=seq_text, font=(std_font, std_font_size//2))
			l2.grid(row=1, column=len(num_cats))
			
			vals = [ str(val)[:-2] if str(val).endswith(".0") else str(val) for val in cat[1] ]
			if len(vals)>5:
				vals = vals[:3]+["..."]+[vals[-1]]
			l3 = Label(num_frame, text=" ("+", ".join(vals)+")", font=(std_font, 10))  
			l3.grid(row=2, column=len(num_cats))
			l4 = Label(num_frame, text="numerical interpretation (optional):", font=(std_font, std_font_size//2))
			l4.grid(row=3, column=len(num_cats))
			v = StringVar(num_frame, value=cat[3])
			e = Entry(num_frame, textvariable=v)
			e.grid(row=4, column=len(num_cats))
            
			l5 = Label(num_frame, text="cross bar text (optional):", font=(std_font, std_font_size//2))
			l5.grid(row=5, column=len(num_cats))
			v = StringVar(num_frame, value=cat[4])
			e2 = Entry(num_frame, textvariable=v)
			e2.grid(row=6, column=len(num_cats))
            
			additives = [ clue["oper"]=="+" for clue in puzzle1.clues if clue["typ"]==3 and clue["K6"]==j ]
			multiplicatives = [ clue["oper"]=="*" for clue in puzzle1.clues if clue["typ"]==3 and clue["K6"]==j ]
			if cat[5]!="geometric" and all(additives):
				can_first_el_be_changed = True
				can_increment_be_changed = True
			elif cat[5]=="geometric" and all(multiplicatives):
				can_first_el_be_changed = True
				can_increment_be_changed = True
			elif cat[5]=="geometric" and all(additives):
				can_first_el_be_changed = True
				can_increment_be_changed = False
			else:
				can_first_el_be_changed = False
				can_increment_be_changed = False
            
			if can_first_el_be_changed or can_increment_be_changed:
				eval_frame = Frame(num_frame)
				eval_frame.grid(row=7, column=len(num_cats))
                
				if str(cat[1][0]).endswith(".0"):
					a = StringVar(eval_frame, value=str(cat[1][0])[:-2])
				else:
					a = StringVar(eval_frame, value=cat[1][0])
				if cat[5]=="geometric":
					r = cat[1][1]/cat[1][0]
				else:
					r = cat[1][1]-cat[1][0]
				if str(r).endswith(".0"):
					r = StringVar(eval_frame, value=str(r)[:-2])
				else:
					r = StringVar(eval_frame, value=r)
				l6 = Label(eval_frame, text="first:", font=(std_font, std_font_size//2))
				l6.grid(row=0, column=0)
				e3 = Entry(eval_frame, textvariable=a, width=5)
				e3.grid(row=0, column=1)
				if cat[5]=="geometric":
					l7 = Label(eval_frame, text="multiplier:", font=(std_font, std_font_size//2))
				else:
					l7 = Label(eval_frame, text="increment:", font=(std_font, std_font_size//2))
				l7.grid(row=0, column=2)
				e4 = Entry(eval_frame, textvariable=r, width=4)
				e4.grid(row=0, column=3)
				ev_btn = Button(eval_frame, text="eval", font=("Arial", std_font_size//2), command=partial(clicked_eval,j))
				ev_btn.grid(row=0, column=4)
				ev_btn.config( height = 1, width = 1 )
                
				if not can_first_el_be_changed:
					e3.configure(state='disabled')
				if not can_increment_be_changed:
					e4.configure(state='disabled')
            
			entries.append(l)
			entries.append(e) # interpretation
			entries.append(e2) # cross bar text
			entries.append(l2)
			entries.append(l3)
			entries.append(l4)
			entries.append(l5)
			if can_first_el_be_changed or can_increment_be_changed:  
				entries.append(l6)
				entries.append(e3) # first number element
				entries.append(l7)
				entries.append(e4) # multiplier/increment
				entries.append(eval_frame)
			num_cats.append(entries)
			
	cat_frame.grid()
	num_frame.grid()
	
	final_frame.grid()
	print_btn['state'] = 'normal'
	svg_btn['state'] = 'normal'
	solution_btn['state'] = 'normal'
	new_btn['state'] = 'normal'
	final_lbl.grid()
	
	final_puzzle.K = K
	final_puzzle.k = k
	final_puzzle.grid = puzzle1.grid
	final_puzzle.diff = puzzle1.diff
	final_puzzle.clues = puzzle1.clues
	final_puzzle.categories = puzzle1.categories
	final_puzzle.seed = puzzle1.seed
	final_puzzle.solved = puzzle1.solved
	final_puzzle.contradictory = puzzle1.contradictory
	final_puzzle.solution = puzzle1.solution    
	
	final_name.configure(text="p"+str(puzzle1.seed)+"K"+str(puzzle1.K)+"k"+str(puzzle1.k)+"c"+str(len(puzzle1.clues))+".pdf")
	final_name2.configure(text="p"+str(puzzle1.seed)+"K"+str(puzzle1.K)+"k"+str(puzzle1.k)+"c"+str(len(puzzle1.clues))+".svg")
	final_name3.configure(text="sol"+str(puzzle1.seed)+"K"+str(puzzle1.K)+"k"+str(puzzle1.k)+"c"+str(len(puzzle1.clues))+".pdf")
    
def chosen_random():
	txt.configure(state='disabled')
	txt4['state'] = 'normal'
	txt5['state'] = 'normal'
	txt4.focus()
	txt_categorical.delete(0, 'end')
	txt_ordinal.delete(0, 'end')
	txt_numerical.delete(0, 'end')
	txt_categorical.insert(END, 'random')
	txt_ordinal.insert(END, 'random')
	txt_numerical.insert(END, 'random')
	txt_categorical['state'] = 'disabled'
	txt_ordinal['state'] = 'disabled'
	txt_numerical['state'] = 'disabled'
    
def chosen_seed():
	txt['state'] = 'normal'
	txt4['state'] = 'normal'
	txt5['state'] = 'normal'
	txt.focus()
	txt_categorical.delete(0, 'end')
	txt_ordinal.delete(0, 'end')
	txt_numerical.delete(0, 'end')
	txt_categorical.insert(END, 'random')
	txt_ordinal.insert(END, 'random')
	txt_numerical.insert(END, 'random')
	txt_categorical['state'] = 'disabled'
	txt_ordinal['state'] = 'disabled'
	txt_numerical['state'] = 'disabled'
    
def chosen_custom():
	txt.configure(state='disabled')
	txt4['state'] = 'normal'
	txt5['state'] = 'normal'
	txt4.focus()
	txt_categorical['state'] = 'normal'
	txt_ordinal['state'] = 'normal'
	txt_numerical['state'] = 'normal'
	txt_categorical.delete(0, 'end')
	txt_ordinal.delete(0, 'end')
	txt_numerical.delete(0, 'end')
    
def check_and_save_categories():
	input_categories = []
	input_cross_bars = []
	n = 0
	for j, cat in enumerate(final_puzzle.categories):
		if cat[0]=='categorical' or cat[0]=='ordinal':
			names = []
			for i in range(final_puzzle.k):
				names.append(cat_cats[n][i+1].get())
			cross_text = cat_cats[n][final_puzzle.k+2].get()
			input_categories.append( (cat[0], names, cross_text) )
			n += 1
			if any([name=="" for name in names]):
				messagebox.showwarning('Warning', 'One or more object names are empty!')
				return False
	n = 0
	for j, cat in enumerate(final_puzzle.categories):
		if cat[0]=='numerical':
			cross_text = num_cats[n][2].get()
			input_categories.append( (cat[0], cat[1], cat[2], num_cats[n][1].get(),cross_text,cat[5]) )
			n += 1
	
	print(input_categories)
	
	if funs.do_categories_repeat(input_categories):
		messagebox.showwarning('Warning', 'Repeating names detected!')
		return False
		
	final_puzzle.categories = input_categories
	return True
    
def clicked_print():
	if not check_and_save_categories():
		return
	
	direc = filedialog.askdirectory(initialdir= path.dirname(__file__))
	
	if not direc:
		return
	
	c = canvas.Canvas(direc+"/"+final_name.cget("text"))
	pdf_funs.draw_on_canvas(final_puzzle, c)
	c.showPage()
	c.save()
	
	final_lbl.configure(text="The puzzle has been printed to:\n"+direc+"/"+final_name.cget("text"))
	
    
def clicked_svg():
	if not check_and_save_categories():
		return
	
	direc = filedialog.askdirectory(initialdir= path.dirname(__file__))
	
	if not direc:
		return
	
	d = drawSvg.Drawing(616, 870, displayInline=False)
	svg_funs.draw_on_canvas(final_puzzle, d)
	d.setPixelScale(2)
	d.saveSvg(direc+"/"+final_name.cget("text")[:-3]+"svg")
	final_lbl.configure(text="The puzzle has been printed to:\n"+direc+"/"+final_name.cget("text")[:-3]+"svg")

def clicked_sol():
	if not check_and_save_categories():
		return
	
	direc = filedialog.askdirectory(initialdir= path.dirname(__file__))
	
	if not direc:
		return
	c = canvas.Canvas(direc+"/"+final_name3.cget("text"))
	pdf_funs.draw_solution(final_puzzle, c)
	c.save()
	
	final_name3.configure(text="sol"+str(final_puzzle.seed)+"K"+str(final_puzzle.K)+"k"+str(final_puzzle.k)+"c"+str(len(final_puzzle.clues))+".pdf")
	final_lbl3.configure(text="The solution has been printed to:\n"+direc+"/"+final_name3.cget("text"))
    
def clicked_new():
	btn['state'] = 'normal'
	lbl6.grid_forget()
	bar.grid_forget()
	lbl7.grid_forget()
	
	final_frame.grid_forget()
	final_lbl.configure(text="")
	final_lbl.grid_forget()
	
	for cat in cat_cats:
		for entry in cat:
			entry.grid_forget()
	for cat in num_cats:
		for entry in cat:
			entry.grid_forget()
			

	cat_frame.grid_forget()
	num_frame.grid_forget()
	cat_frame.configure(pady=10)
	num_frame.configure(pady=10)

    
def clicked_eval(j):
	if len(num_cats)<1:
		return
	n = -1
	for i, cat in enumerate(final_puzzle.categories):
		if i<=j and cat[0]=="numerical":
			n += 1
		if i==j:
			break
    
	try: 
		float(num_cats[n][8].get())
	except:
		messagebox.showwarning('Warning', 'First element must be a number!')
		return
	try: 
		float(num_cats[n][10].get())
	except:
		messagebox.showwarning('Warning', 'Increment/multiplier must be a number!')
		return
    
	if final_puzzle.categories[j][0]=="numerical" and final_puzzle.categories[j][5]=="geometric" and float(num_cats[n][8].get())<=0:
		messagebox.showwarning('Warning', 'First element in geometric sequence has to be greater than zero!')
		return
	if final_puzzle.categories[j][0]=="numerical" and final_puzzle.categories[j][5]=="arithmetic" and float(num_cats[n][10].get())<=0:
		messagebox.showwarning('Warning', 'Sequence increment has to be greater than zero!')
		return
	if final_puzzle.categories[j][0]=="numerical" and final_puzzle.categories[j][5]=="geometric" and float(num_cats[n][10].get())<=0:
		messagebox.showwarning('Warning', 'Sequence multiplier has to be greater than zero!')
		return
    
	new_r = float(num_cats[n][10].get())
    
	old_vals = final_puzzle.categories[j][1]
	new_vals = [float(num_cats[n][8].get())]
	for i in range(final_puzzle.k-1):
		if final_puzzle.categories[j][5]=="geometric":
			new_vals.append(float(new_vals[-1])*new_r)
		elif final_puzzle.categories[j][5]=="arithmetic":
			new_vals.append(float(new_vals[-1])+new_r)
		else:
			new_vals.append( float(new_vals[-1])+new_r/(old_vals[1]-old_vals[0])*(old_vals[i+1]-old_vals[i]) )
    
	old_possible_clues_of_type_3 = final_puzzle.categories[j][2]
	new_possible_clues_of_type_3 = []
	for pc in old_possible_clues_of_type_3:
		old_a = float(pc[4:])
		if final_puzzle.categories[j][5]=="geometric":
			old_r = old_vals[1]/old_vals[0]
		else:
			old_r = old_vals[1]-old_vals[0]
		new_a = old_a/old_r*new_r
		new_possible_clues_of_type_3.append(pc[:4]+str(new_a))
    
	for clue in final_puzzle.clues:
		if clue["typ"]==3 and clue["K6"]==j:
			clue["diff"] = clue["diff"]/old_r*new_r
    
	final_puzzle.categories[j] = (final_puzzle.categories[j][0], new_vals, new_possible_clues_of_type_3, final_puzzle.categories[j][3], final_puzzle.categories[j][4], final_puzzle.categories[j][5] )
    
	vals = [ str(val)[:-2] if str(val).endswith(".0") else str(val) for val in new_vals ]
	if len(vals)>5:
		vals = vals[:3]+["..."]+[vals[-1]]
	num_cats[n][4].configure(text=" ("+", ".join(vals)+")", font=(std_font, 10))

# -------------------------- Scroll bar ---------------------------
    
# cTableContainer = Canvas(window)
# fTable = Frame(cTableContainer)
# sbHorizontalScrollBar = Scrollbar(window)
# sbVerticalScrollBar = Scrollbar(window)

# cTableContainer.config(xscrollcommand=sbHorizontalScrollBar.set,
#         yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
# sbHorizontalScrollBar.config(orient=HORIZONTAL, command=cTableContainer.xview)
# sbVerticalScrollBar.config(orient=VERTICAL, command=cTableContainer.yview)

# sbHorizontalScrollBar.grid(row=20, columnspan=5, sticky="we")
# sbVerticalScrollBar.grid(column=2, sticky="we")
# cTableContainer.grid(column=2, sticky="ns")
# cTableContainer.create_window(0, 0, window=fTable, anchor=NW)
    
# ------------------------- Intro -----------------------------

std_font = 'sans-serif'
std_font_size = 12
font = (std_font, std_font_size)

lbl0 = Label(window, text="Welcome to my text puzzle generator!", font=(std_font, 25), pady=10)
lbl0.grid(row=0, column=0, columnspan=2)

lbl1 = Label(window, text="This is version 1.2.", font=font, bd=1, relief="solid")
lbl1.grid(row=1, column=0, columnspan=2)

lbl2 = Label(window, text="Choose what you want to do:", font=font, pady=10)
lbl2.grid(row=2, column=0, columnspan=2)

# ------------ choosing frame ------------------

choose_frame = Frame(window, bd=1, relief="solid")
choose_frame.grid(row=3, column=0)

choose_seed_frame = Frame(choose_frame)
choose_seed_frame.grid(row=1, column=0, sticky="w")

choice = IntVar()
rad1 = Radiobutton(choose_frame, text='Generate random puzzle', value=1, variable=choice, command=chosen_random, font=font)
rad2 = Radiobutton(choose_seed_frame, text='Generate from seed:  ', value=2, variable=choice, command=chosen_seed, font=font)
rad3 = Radiobutton(choose_frame, text='Generate from custom categories', value=3, variable=choice, command=chosen_custom, font=font)

rad1.grid(row=0, column=0, sticky="w") # in choose_frame
rad2.grid(row=0, column=0) # in choose_seed_frame
rad3.grid(row=2, column=0, sticky="w") # in choose_frame

txt = Entry(choose_seed_frame, width=10)
txt.grid(row=0, column=1)
txt.configure(state='disabled')

# -------------- specifying sizes frame ---------------
text_box_width = 6

size_frame = Frame(window)
size_frame.grid(row=4)

lbl3 = Label(size_frame, text="Specify dimensions for your puzzle:", font=font, pady=10)
lbl3.grid(row=0, column=0, columnspan=2)

lbl4 = Label(size_frame, text="Number of categories(>2): ", font=font, pady=0)
lbl4.grid(row=1, column=0)
txt4 = Entry(size_frame, width=text_box_width)
txt4.grid(row=1, column=1)
txt4.configure(state='disabled')

lbl5 = Label(size_frame, text="Number of objects in each category(>2):", font=font, pady=0)
lbl5.grid(row=2, column=0)
txt5 = Entry(size_frame, width=text_box_width)
txt5.grid(row=2, column=1)
txt5.configure(state='disabled')

lbl_custom = Label(size_frame, text="Only for custom categories generation:", font=(std_font, std_font_size//2))
lbl_custom.grid(row=3, column=0)

lbl_categorical = Label(size_frame, text="Number of categorical categories:", font=font, pady=0)
lbl_categorical.grid(row=4, column=0)
txt_categorical = Entry(size_frame, width=text_box_width)
txt_categorical.insert(END, 'random')
txt_categorical.grid(row=4, column=1)
txt_categorical.configure(state='disabled')

lbl_ordinal = Label(size_frame, text="Number of ordinal categories:", font=font, pady=0)
lbl_ordinal.grid(row=5, column=0)
txt_ordinal = Entry(size_frame, width=text_box_width)
txt_ordinal.insert(END, 'random')
txt_ordinal.grid(row=5, column=1)
txt_ordinal.configure(state='disabled')

lbl_numerical = Label(size_frame, text="Number of numerical categories:", font=font, pady=0)
lbl_numerical.grid(row=6, column=0)
txt_numerical = Entry(size_frame, width=text_box_width)
txt_numerical.insert(END, 'random')
txt_numerical.grid(row=6, column=1)
txt_numerical.configure(state='disabled')



# ------------ Generate -------------------

gen_frame = Frame(window)
gen_frame.grid(row=5, column=0)

btn_OK = Button(gen_frame, text="OK", font=("Arial", std_font_size), command=clicked_ok)
btn_OK.grid(row=0, column=0, pady=(10,0), padx=(0,10))

btn = Button(gen_frame, text="Generate!", font=("Arial", std_font_size), command=clicked_gen)
btn.grid(row=0, column=1, pady=(10,0))
btn.configure(state='disabled')

lbl6 = Label(window, text="Generating puzzle...(0%)", font=font)

bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 0

# ----------------- Info about generated puzzle ------------------

cat_cats = []
num_cats = []

lbl7 = Label(window, text="", font=font)

cat_frame = Frame(window)
cat_frame.grid(row=9, column=0, pady=(10,10))
num_frame = Frame(window)
num_frame.grid(row=10, column=0, pady=(0,10))

# --------------------- Final buttons ------------------------

final_frame = Frame(window)
final_frame.grid(row=11)

print_btn = Button(final_frame, text="Print to PDF!", font=("Arial", std_font_size), command=clicked_print)
print_btn.grid(row=0, column=0)
print_btn.configure(state='disabled')

svg_btn = Button(final_frame, text="Print to SVG!", font=("Arial", std_font_size), command=clicked_svg)
svg_btn.grid(row=0, column=1)
svg_btn.configure(state='disabled')

solution_btn = Button(final_frame, text="Get step-by-step solution!", font=("Arial", std_font_size), command=clicked_sol)
solution_btn.grid(row=0, column=2)
solution_btn.configure(state='disabled')

new_btn = Button(final_frame, text="I want another puzzle!", font=("Arial", std_font_size), command=clicked_new)
new_btn.grid(row=0, column=3)
new_btn.configure(state='disabled')

# -------------------- Final info ----------------------------

final_puzzle = puzzle(3,3)
final_name = Label(window, text="unknown_puzzle.pdf", font=font)
final_name2 = Label(window, text="unknown_puzzle.svg", font=font)
final_name3 = Label(window, text="unknown_solution.pdf", font=font)

final_lbl = Label(window, text="", font=(std_font, 10))
final_lbl.grid(row=12)
final_lbl2 = Label(window, text="", font=(std_font, 10))
final_lbl2.grid(row=13)
final_lbl3 = Label(window, text="", font=(std_font, 10))
final_lbl3.grid(row=14)


window.mainloop()
