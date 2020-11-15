from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from os import path
import copy
from reportlab.pdfgen import canvas

import numpy as np
from puzzle_class import puzzle
import generating_cathegories_functions as funs
from pdf_printing_functions import rysuj_zagadke

window = Tk()
window.geometry('700x740')
window.title("Text puzzle generator v1")

def clicked_gen():
	choice_int = choice.get()
	if choice_int==1:
		seed = np.random.choice(range(100), 1)[0]
	elif choice_int==2:
		try:
			seed = int(txt.get())
		except:
			messagebox.showwarning('Warning', 'Seed must be a number!')
			return
		if seed<0 or seed>=100:
			messagebox.showwarning('Warning', 'Seed must be an integer from 0 to 99!')
			return
	else:
		messagebox.showwarning('Warning', 'Decide what you want to do first!')
		return
		
	try:
		K = int(txt4.get())
	except:
		messagebox.showwarning('Warning', 'Number of cathegories must be an integer!')
		txt4.focus()
		return
	try:
		k = int(txt5.get())
	except:
		messagebox.showwarning('Warning', 'Number of objects in each cathegory must be an integer!')
		txt5.focus()
		return
	
	if K<3 or K>7:
		messagebox.showwarning('Warning', 'Number of cathegories must be an integer from 3 to 7!')
		txt4.focus()
		return
	if k<3 or k>8:
		messagebox.showwarning('Warning', 'Number of objects in each cathegory must be an integer from 3 to 8!')
		txt5.focus()
		return
	
	btn.configure(state='disabled')
	lbl6.grid(row=6, column=0)
	bar.grid(row=7, column=0)
	
	percent = 0
	lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
	bar['value'] = percent
	window.update()
	
	# ----------------- Generating --------------
	
	puzzle1 = puzzle(K, k)
	#puzzle1.generate(seed, trace=True)
	
	puzzle1.set_seed(seed)
	puzzle1.draw_cathegories()
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
	
	# ---------------- clues restriction -----------------
	
	clues_copy = copy.deepcopy(puzzle1.clues)
	to_restrict = []
        
	clues1 = [ i for i, clue in enumerate(clues_copy) if clue["typ"]==1 ]
	clue_order = np.random.choice(clues1, len(clues1), replace=False)
	for i in clue_order:
		clues1_restricted = [ j for j in clues1 if j!=i ]
		puzzle1.clear_grid()
		puzzle1.clues = [ clue for j, clue in enumerate(clues_copy) if j in clues1_restricted or not j in clue_order ]
		puzzle1.try_to_solve()
		if puzzle1.is_grid_completed() and not puzzle1.is_grid_contradictory():
			to_restrict.append(i)
			clues1 = clues1_restricted
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
		percent += int(np.floor(95/bar_N))
		lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
		bar['value'] = percent
		window.update()

	puzzle1.clues = [ clue for j, clue in enumerate(clues_copy) if not j in to_restrict ]
	
	#percent = int(np.floor(5+95/bar_N*(bar_N-5)))
	#lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
	#bar['value'] = percent
	#window.update()
	
	# ---------------- difficulty assessment -------------------
	
	N = 5
	diffs = []
	for n in range(N):
		puzzle1.clear_grid()
		puzzle1.diff = 0
		puzzle1.try_to_solve()
		diffs.append(puzzle1.diff)
		
		percent = int(np.floor(5+95/bar_N*(bar_N-4+n)))
		lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
		bar['value'] = percent
		window.update()
	puzzle1.diff = round(np.mean(diffs),2)
	
	puzzle1.print_info()
	
	percent = 100
	lbl6.configure(text="Generating puzzle...("+str(percent)+"%)")
	bar['value'] = percent
	
	lbl7.grid(row=8, column=0)
	lbl7.configure(text="You drew a puzzle from seed="+str(seed)+", estimated difficulty is: "+str(puzzle1.diff)+".\nYou may now alter cathegory names if you wish. \nWhen you are done you can print your puzzle to pdf.\n@ is a special symbol for the place where numerical data is inserted.")
	
	cat_cats.clear()
	num_cats.clear()
	for j, cat in enumerate(puzzle1.cathegories):
		entries = []
		if cat[0]=='cathegorical' or cat[0]=='ordinal':
			l = Label(cat_frame, text="Cathegory "+str(j)+":", font=(std_font, std_font_size//2, 'bold'))
			l.grid(row=0, column=len(cat_cats))
			entries.append(l)
			for i in range(k):
				v = StringVar(cat_frame, value=cat[1][i])
				e = Entry(cat_frame, textvariable=v)
				e.grid(row=i+1, column=len(cat_cats))
				entries.append(e)
			cat_cats.append(entries)
		elif cat[0]=='numerical':
			l = Label(num_frame, text="Cathegory "+str(j)+":", font=(std_font, std_font_size//2, 'bold'))
			l.grid(row=0, column=len(num_cats))
			v = StringVar(num_frame, value=cat[3])
			e = Entry(num_frame, textvariable=v)
			e.grid(row=1, column=len(num_cats))
			
			vals = [ str(val)[:-2] if str(val).endswith(".0") else str(val) for val in cat[1] ]
			l2 = Label(num_frame, text="("+", ".join(vals)+")", font=(std_font, 10))
			l2.grid(row=2, column=len(num_cats))
			
			entries.append(l)
			entries.append(e)
			entries.append(l2)
			num_cats.append(entries)
			
	cat_frame.grid()
	num_frame.grid()
	
	final_frame.grid()
	print_btn['state'] = 'normal'
	new_btn['state'] = 'normal'
	final_lbl.grid()
	
	final_puzzle.K = K
	final_puzzle.k = k
	final_puzzle.grid = puzzle1.grid
	final_puzzle.diff = puzzle1.diff
	final_puzzle.clues = puzzle1.clues
	final_puzzle.cathegories = puzzle1.cathegories
	final_puzzle.seed = puzzle1.seed
	final_puzzle.solved = puzzle1.solved
	final_puzzle.contradictory = puzzle1.contradictory
	
	final_name.configure(text="p"+str(puzzle1.seed)+"K"+str(puzzle1.K)+"k"+str(puzzle1.k)+"c"+str(len(puzzle1.clues))+".pdf")


def chosen_random():
	txt.configure(state='disabled')
	txt4['state'] = 'normal'
	txt5['state'] = 'normal'
	txt4.focus()
	
def chosen_seed():
	txt['state'] = 'normal'
	txt4['state'] = 'normal'
	txt5['state'] = 'normal'
	txt.focus()

def clicked_print():
	input_cathegories = []
	n = 0
	for j, cat in enumerate(final_puzzle.cathegories):
		if cat[0]=='cathegorical' or cat[0]=='ordinal':
			names = []
			for i in range(final_puzzle.k):
				names.append(cat_cats[n][i+1].get())
			input_cathegories.append( (cat[0], names) )
			n += 1
	n = 0
	for j, cat in enumerate(final_puzzle.cathegories):
		if cat[0]=='numerical':
			input_cathegories.append( (cat[0], cat[1], cat[2], num_cats[n][1].get()) )
			n += 1
	
	print(input_cathegories)
	
	if funs.do_cathegories_repeat(input_cathegories):
		messagebox.showwarning('Warning', 'Repeating names detected!')
		return
		
	final_puzzle.cathegories = input_cathegories
	
	direc = filedialog.askdirectory(initialdir= path.dirname(__file__))
	
	if not direc:
		return
	
	c = canvas.Canvas(direc+"/"+final_name.cget("text"))
	rysuj_zagadke(final_puzzle, c)
	c.showPage()
	c.save()
	
	final_lbl.configure(text="The puzzle has been printed to:\n"+direc+"/"+final_name.cget("text"))
	
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

# ------------------------- Intro -----------------------------

std_font = 'sans-serif'
std_font_size = 12
font = (std_font, std_font_size)

lbl0 = Label(window, text="Welcome to my text puzzle generator!", font=(std_font, 30), pady=10)
lbl0.grid(row=0, column=0, columnspan=2)

lbl1 = Label(window, text="This is only a test version. \nThe range for random seed is restricted to numbers from 0 to 99!", font=font, bd=1, relief="solid")
lbl1.grid(row=1, column=0, columnspan=2)

lbl2 = Label(window, text="Choose what you want to do:", font=font, pady=10)
lbl2.grid(row=2, column=0, columnspan=2)

# ------------ choosing frame ------------------

choose_frame = Frame(window)
choose_frame.grid(row=3, column=0)

choice = IntVar()
rad1 = Radiobutton(choose_frame, text='Generate random puzzle', value=1, variable=choice, command=chosen_random, font=font)
rad2 = Radiobutton(choose_frame, text='Generate from seed(0 to 99)', value=2, variable=choice, command=chosen_seed, font=font)
rad1.grid(row=0, column=0)
rad2.grid(row=0, column=1)

txt = Entry(choose_frame, width=10)
txt.grid(row=0, column=3)
txt.configure(state='disabled')

# -------------- specifying sizes frame ---------------

size_frame = Frame(window)
size_frame.grid(row=4)

lbl3 = Label(size_frame, text="Specify dimensions for your puzzle:", font=font, pady=10)
lbl3.grid(row=0, column=0, columnspan=2)

lbl4 = Label(size_frame, text="Number of cathegories(3-7): ", font=font, pady=0)
lbl4.grid(row=1, column=0)
txt4 = Entry(size_frame, width=5)
txt4.grid(row=1, column=1)
txt4.configure(state='disabled')

lbl5 = Label(size_frame, text="Number of objects in each cathegory(3-8):", font=font, pady=0)
lbl5.grid(row=2, column=0)
txt5 = Entry(size_frame, width=5)
txt5.grid(row=2, column=1)
txt5.configure(state='disabled')

# ------------ Generate -------------------

btn = Button(window, text="Generate!", font=("Arial", std_font_size), command=clicked_gen)
btn.grid(row=5, column=0, pady=(10,0))

lbl6 = Label(window, text="Generating puzzle...(0%)", font=font)

bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 0

# ----------------- Info about generated puzzle ------------------

cat_cats = []
num_cats = []

lbl7 = Label(window, text="", font=font)

cat_frame = Frame(window)
cat_frame.grid(row=9, column=0, pady=(10,0))
num_frame = Frame(window)
num_frame.grid(row=10, column=0, pady=(0,10))

# --------------------- Final buttons ------------------------

final_frame = Frame(window)
final_frame.grid(row=11)

print_btn = Button(final_frame, text="Print to PDF!", font=("Arial", std_font_size), command=clicked_print)
print_btn.grid(row=0, column=0)
print_btn.configure(state='disabled')

new_btn = Button(final_frame, text="I want another puzzle!", font=("Arial", std_font_size), command=clicked_new)
new_btn.grid(row=0, column=1)
new_btn.configure(state='disabled')

# -------------------- Final info ----------------------------

final_puzzle = puzzle(3,3)
final_name = Label(window, text="unknown_puzzle.pdf", font=font)

final_lbl = Label(window, text="", font=(std_font, 10))
final_lbl.grid(row=12)



window.mainloop()
