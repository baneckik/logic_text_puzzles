from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from os import path

import numpy as np

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
	
	print(seed)
	btn.configure(state='disabled')
	lbl5.grid(row=6, column=0)
	bar.grid(row=7, column=0)

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

std_font = 'sans-serif'
std_font_size = 12
font = (std_font, std_font_size)

lbl0 = Label(window, text="Welcome to my text puzzle generator!", font=(std_font, 30), pady=10)
lbl0.grid(row=0, column=0, columnspan=2)

lbl1 = Label(window, text="This is only a test version. \nThe range for random seed is restricted to numbers from 0 to 99!", font=font, bd=1, relief="solid")
lbl1.grid(row=1, column=0, columnspan=2)

lbl2 = Label(window, text="Choose what you want to do:", font=font, pady=10)
lbl2.grid(row=2, column=0, columnspan=2)

# --------- choosing frame ---------------
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
size_frame.grid(row=4, columnspan=2)

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

percent = 0
lbl5 = Label(window, text="Generating puzzle...("+str(percent)+"%)", font=font)

bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = percent




# direc = filedialog.askdirectory(initialdir= path.dirname(__file__))

window.mainloop()
