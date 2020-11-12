from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from os import path

window = Tk()
window.geometry('650x600')
window.title("Text puzzle generator v1")

lbl = Label(window, text="Hello WorlŁąŹŻd", font=("sans-serif", 50))
lbl.grid(column=0, row=0)

txt = Entry(window, width=10)
txt.grid(column=1, row=1)
txt.focus()
x = txt.get()

def clicked():
    lbl.configure(text="was clicked !!")
    txt.configure(state='disabled')
    #x = int(txt.get())
    #messagebox.showinfo('Message title','Message content')
    messagebox.showwarning('Message title','Message content')
    
def clicked2():
    messagebox.showinfo('Message title','Coś się zmieniło!')

btn = Button(window, text="Generate!", bg="red", fg="red", font=("Arial", 20), command=clicked)
btn.grid(column=0, row=1)

selected = IntVar()

rad1 = Radiobutton(window,text='First', value=1, variable=selected, command=clicked2)
rad2 = Radiobutton(window,text='Second', value=2, variable=selected, command=clicked2)

rad1.grid(column=2, row=0)
rad2.grid(column=2, row=1)

bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 70
bar.grid(column=0, row=3)

direc = filedialog.askdirectory(initialdir= path.dirname(__file__))

lbl2 = Label(window, text=direc, font=("sans-serif", 10))
lbl2.grid(column=0, row=4)

window.mainloop()
