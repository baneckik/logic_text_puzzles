import numpy as np
import pandas as pd
from pathlib import Path
import collections
import matplotlib.pyplot as plt

def print_categories_stats():
    df = pd.DataFrame(columns=["name","weight","folder","N"])
    i = 0
    for path in Path('categories/categorical').rglob('*.txt'):
        kat = pd.read_csv(path, header=None)
        name = path.name.split(".")[0]
        weight = int(kat.iloc[0,0][2:])
        folder = path.parts[-2]
        count = kat.shape[0]-1
        df.loc[i] = [name, weight, folder, count]
        i += 1
    
    df2 = pd.DataFrame(columns=["name","weight","N"])
    i = 0
    for path in Path('categories/ordinal').rglob('*.txt'):
        kat = pd.read_csv(path, header=None)
        name = path.name.split(".")[0]
        weight = int(kat.iloc[0,0][2:])
        count = kat.shape[0]-1
        df2.loc[i] = [name, weight, count]
        i += 1
        
    folders = np.unique(df.folder)
    fig, ax = plt.subplots(len(folders)+1, 1, figsize=(17,50))
    for i in range(len(folders)):
        df_plot = df[df.folder==folders[i]]
        ax[i].pie(df_plot.weight, labels=df_plot.name)
    ax[-1].pie(df2.weight, labels=df2.name)    
    plt.tight_layout()
    plt.show()
    
def print_categories_stats2():
    df = pd.DataFrame(columns=["name","weight","folder","N"])
    i = 0
    for path in Path('categories/categorical').rglob('*.txt'):
        kat = pd.read_csv(path, header=None)
        name = path.name.split(".")[0]
        weight = int(kat.iloc[0,0][2:])
        folder = path.parts[-2]
        count = kat.shape[0]-1
        df.loc[i] = [name, weight, folder, count]
        i += 1
    
    df2 = pd.DataFrame(columns=["name","weight","N"])
    i = 0
    for path in Path('categories/ordinal').rglob('*.txt'):
        kat = pd.read_csv(path, header=None)
        name = path.name.split(".")[0]
        weight = int(kat.iloc[0,0][2:])
        count = kat.shape[0]-1
        df2.loc[i] = [name, weight, count]
        i += 1
        
    print("Liczba wszystkich kategorii kategorycznych: "+str(df.shape[0])+".")
    print("Liczba wszystkich słów we wszystkich kategoriach kategorycznych: "+str(sum(df.N))+".")
    print("Każda kategoria kategoryczna posiada średnio "+str(np.round(sum(df.N)/df.shape[0],2))+" słów.")
    print("Minimalna/maksymalna liczność kategorii kategorycznej: "+str(min(df.N))+"/"+str(max(df.N))+"." )
    print()
    print("Liczba wszystkich kategorii porządkowych: "+str(df2.shape[0])+".")
    print("Liczba wszystkich słów we wszystkich kategoriach porządkowych: "+str(sum(df2.N))+".")
    print("Każda kategoria porządkowa posiada średnio "+str(np.round(sum(df2.N)/df2.shape[0],2))+" słów.")
    print("Minimalna/maksymalna liczność kategorii porządkowych: "+str(min(df2.N))+"/"+str(max(df2.N))+"." )
    
def find_word(word):
    found = []
    for path in Path('categories').rglob('*.txt'):
            kat = pd.read_csv(path, header=None)
            if word.lower() in [ w.lower() for w in list(kat.iloc[1:,0]) ]:
                found.append("/".join(str(path).split(".")[0].split("/")[-2:]))
    if len(found)>0:
        print("Słowo występuje już w: ", found)
    else:
        print("Słowo nie występuje jeszcze w zbiorze.")
        
def check_for_duplicates():
    found = []
    for path in Path('categories').rglob('*.txt'):
            kat = pd.read_csv(path, header=None).iloc[1:,0]
            if len(list(kat)) != len(set(kat)):
                found.append(path.name.split(".")[0])
                print([item for item, count in collections.Counter(list(kat)).items() if count > 1])
    if len(found)>0:
        print("Znaleziono powtarzające się słowa w: ", found)
    else:
        print("Nie znaleziono kategorii, w której powtarzałyby się słowa.")

def print_table1():
    df = pd.DataFrame(columns=["name","weight","folder","N"])
    i = 0
    for path in Path('categories/categorical').rglob('*.txt'):
        kat = pd.read_csv(path, header=None)
        name = path.name.split(".")[0]
        weight = int(kat.iloc[0,0][2:])
        folder = path.parts[-2]
        count = kat.shape[0]-1
        df.loc[i] = [name, weight, folder, count]
        i += 1
    
    df = df.sort_values("name")
    pre = "\\begin{center}\n\\begin{tabular}{ | c | c | c | c |}\n\\hline\n Category & \\# of objects & Weight & Probability\\\\ \n\hline\n"
    post = "\\hline\n\\end{tabular}\n\\end{center}"
    for folder in np.unique(df.folder):
        print("------------------------- "+str(folder)+" ------------------------")
        table_latex = pre
        df1 = df[df.folder==folder]
        df1.insert(3, "prob", [round(df1.weight.iloc[i]/sum(df1.weight)*100, 1) for i in range(df1.shape[0]) ] )
        for i in range(df1.shape[0]):
            table_latex += "\_".join(df1.iloc[i,0].split("_"))+" & $"+str(df1.iloc[i,4])+"$ & $"+str(df1.iloc[i,1])+"$ & $"+str(df1.iloc[i,3])+"\\%$ \\\\ \n"
        table_latex += post
        print(table_latex)
        
       
    # ------------- ordinals -------------
    print("------------------------- ordinal ------------------------")
    df2 = pd.DataFrame(columns=["name","weight","N"])
    i = 0
    for path in Path('categories/ordinal').rglob('*.txt'):
        kat = pd.read_csv(path, header=None)
        name = path.name.split(".")[0]
        weight = int(kat.iloc[0,0][2:])
        count = kat.shape[0]-1
        df2.loc[i] = [name, weight, count]
        i += 1
    df2 = df2.sort_values("name")
    df2.insert(3, "prob", [round(df2.weight.iloc[i]/sum(df2.weight)*100, 1) for i in range(df2.shape[0]) ] )
    table_latex = pre
    for i in range(df2.shape[0]):
        table_latex += "\_".join(df2.iloc[i,0].split("_"))+" & $"+str(df2.iloc[i,2])+"$ & $"+str(df2.iloc[i,1])+"$ & $"+str(df2.iloc[i,3])+"\\%$ \\\\ \n"
    table_latex += post
    print(table_latex)