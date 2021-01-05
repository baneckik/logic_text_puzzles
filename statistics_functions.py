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
            
    folders = np.unique(df.folder)
    fig, ax = plt.subplots(len(folders),1, figsize=(15,50))
    for i in range(len(folders)):
        df_plot = df[df.folder==folders[i]]
        ax[i].pie(df_plot.weight, labels=df_plot.name)
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
    
    print("Liczba wszystkich kategorii: "+str(df.shape[0])+".")
    print("Liczba wszystkich słów we wszystkich kategoriach: "+str(sum(df.N))+".")
    print("Każda kategoria posiada średnio "+str(np.round(sum(df.N)/df.shape[0],2))+" słów.")
    print("Minimalna/maksymalna liczność kategorii: "+str(min(df.N))+"/"+str(max(df.N))+"." )
    
def find_word(word):
    found = []
    for path in Path('categories/categorical').rglob('*.txt'):
            kat = pd.read_csv(path, header=None)
            if word in list(kat.iloc[1:,0]):
                found.append("/".join(str(path).split(".")[0].split("/")[-2:]))
    if len(found)>0:
        print("Słowo występuje już w: ", found)
    else:
        print("Słowo nie występuje jeszcze w zbiorze.")
        
def check_for_duplicates():
    found = []
    for path in Path('categories/categorical').rglob('*.txt'):
            kat = pd.read_csv(path, header=None).iloc[1:,0]
            if len(list(kat)) != len(set(kat)):
                found.append(path.name.split(".")[0])
                print([item for item, count in collections.Counter(list(kat)).items() if count > 1])
    if len(found)>0:
        print("Znaleziono powtarzające się słowa w: ", found)
    else:
        print("Nie znaleziono nigdzie powtarzających się słów.")

        
        
        
        