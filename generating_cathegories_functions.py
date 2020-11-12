import numpy as np
import pandas as pd
from pathlib import Path

# ----------------------------------------- LOSOWANIE ZMIENNYCH KATEGORYCZNYCH ---------------------------------------------

def losuj_schemat_cat(ile=1, przedmiotow_w_kategorii=5):
    
    if ile<1:
        return []
    
    # losowanie folderów
    foldery_wagi = [("activities",3),("geography",3),("items",5),("names",12),("nature",4),("other_concepts",5),("special_names",6)]
    podstawy = [ fw[0] for fw in foldery_wagi ]
    wagi_folder = [ fw[1] for fw in foldery_wagi ]
    wagi_folder = [ w/sum(wagi_folder) for w in wagi_folder ]
    
    if przedmiotow_w_kategorii<6:
        if np.random.uniform(0,1)<0.75:
            foldery = np.random.choice(podstawy, ile, p=wagi_folder, replace=False)
        else:
            foldery = np.random.choice(podstawy, ile, p=wagi_folder, replace=True)
    else:
        foldery = np.random.choice(podstawy, ile, p=wagi_folder, replace=True)
      
    # drawing cathegories from folders
    chosen = []
    for folder in np.unique(foldery):
        available_cats = []
        available_weights = []
        for path in Path('cathegories/cathegorical/'+folder).rglob('*.txt'):
            kat = pd.read_csv(path, header=None)
            if kat.shape[0]-1 >= przedmiotow_w_kategorii:
                available_cats.append(path)
                available_weights.append(int(kat.iloc[0,0].split(" ")[-1]))
        available_weights = [ w/sum(available_weights) for w in available_weights ]
        
        # number of cathegories to draw from this folder
        ile_kat = sum([f==folder for f in foldery])
        if len(available_cats)<ile_kat:
            raise Exception("Nie można znaleźć "+str(ile)+" kategorii porządkowych dla " \
                            +str(przedmiotow_w_kategorii)+" przedmiotów w kategorii!")

        chosen += list( np.random.choice(available_cats, ile_kat, p=available_weights, replace=False) )
        
    chosen_out = []
    for c in chosen:
        if str(c)=="cathegories/cathegorical/special_names/zmysleni_superbohaterowie_ang.txt":
            kat = pd.read_csv(c, header=None, skiprows=[0], sep=" ")
            kat.drop(kat.head(1).index, inplace=True)
            prenames = np.random.choice(kat.iloc[:,0], przedmiotow_w_kategorii, replace=False)
            if przedmiotow_w_kategorii<5:
                n = 1
            else: 
                n = 2
            counts = [0]*n+[1]*n
            counts += list(np.random.choice([0,1], przedmiotow_w_kategorii-len(counts), replace=True))
            names_male = np.random.choice(kat.iloc[:,1], len([i for i in counts if i==0]), replace=False)
            names_female = np.random.choice(kat.iloc[:,2], len([i for i in counts if i==1]), replace=False)
            names = list(names_male)+list(names_female)
            names = [prenames[i]+" "+names[i] for i in range(len(prenames))]
        elif str(c)=="cathegories/cathegorical/special_names/zmysleni_superbohaterowie_pol.txt":
            kat = pd.read_csv(c, header=None, skiprows=[0], sep=" ")
            kat.drop(kat.head(1).index, inplace=True)
            rows = np.random.choice(range(kat.shape[0]), 5, replace=False)
            if przedmiotow_w_kategorii<5:
                n = 1
            else: 
                n = 2
            counts = [0]*n+[1]*n
            counts += list(np.random.choice([0,1], przedmiotow_w_kategorii-len(counts), replace=True))
            names = []
            for j, i in enumerate(rows):
                if counts[j]==0:
                    names.append(kat.iloc[i,0]+" "+kat.iloc[i,2])
                else:
                    names.append(kat.iloc[i,1]+" "+kat.iloc[i,3])
        else:
            kat = pd.read_csv(c, header=None)
            kat.drop(kat.head(1).index, inplace=True)
            names = list(np.random.choice(kat.iloc[:,0], przedmiotow_w_kategorii, replace=False))
        chosen_out.append(names)
    
    return [ ("cathegorical", chosen_out[i]) for i in range(len(chosen_out)) ]

# ----------------------------------------- LOSOWANIE ZMIENNYCH PORZĄDKOWYCH ---------------------------------------------

def losuj_schemat_porz(ile=1, przedmiotow_w_kategorii=5):
    
    if ile<1:
        return []
    
    available_cats = []
    for path in Path('cathegories/ordinal').rglob('*.txt'):
        kat = pd.read_csv(path, header=None)
        #kat.columns = [path.name.split(".")[0]]
        if kat.shape[0]>=przedmiotow_w_kategorii:
            available_cats.append(path)
        
    if len(available_cats)<ile:
        raise Exception("Nie można znaleźć "+str(ile)+" kategorii porządkowych dla " \
                        +str(przedmiotow_w_kategorii)+" przedmiotów w kategorii!")
    
    chosen = np.random.choice(available_cats, ile, replace=False)
    chosen_out = []
    for c in chosen:
        kat = pd.read_csv(c, header=None)
        start = int(np.random.choice(range(0,kat.shape[0]-przedmiotow_w_kategorii+1), 1))
        names = list(kat.iloc[start:(start+przedmiotow_w_kategorii),0])
        chosen_out.append(names)
    
    return [ ("ordinal", chosen_out[i]) for i in range(len(chosen_out)) ]

# ----------------------------------------- LOSOWANIE ZMIENNYCH NUMERYCZNYCH ---------------------------------------------

def losuj_schemat_num(przedmiotow_w_kategorii=5):
    
    # ---------------------- wybór schematu i pierwszego wyrazu=n*p ---------------------------------
    
    # (schemat, jego_waga)
    typy_schematu_wagi = [ ("ciag_arytmetyczny", 10), ("ciag_geometryczny", 2), ("ciag_rosnacy", 4)]
    typy = [ t[0] for t in typy_schematu_wagi ]
    wagi_typow = [ t[1] for t in typy_schematu_wagi ]
    wagi_typow = [ w/sum(wagi_typow) for w in wagi_typow ]
    schemat = np.random.choice(typy, 1, p=wagi_typow)
    
    # (podstawa, jej_waga)
    podstawy_wagi = [(-40,1),(-10,1),(-5,1),(0,1),(1,20),(1.50,5),(2,10),(2.50,5),(3,4),(4,4),(5,3),(6,3), \
                (7,2),(8,2),(9,2),(10,5),(20,5),(50,5),(100,6),(1000,6),(1500,4),(1920,1),(1950,1),(1980,1),(1990,1),(2000,4)]
    # ograniczenia na wartości podstawy
    if schemat=="ciag_geometryczny": 
        podstawy_wagi = [ pw for pw in podstawy_wagi if abs(pw[0])<=10 and pw[0]!=0 ]
    if schemat=="ciag_rosnacy": 
        podstawy_wagi = [ pw for pw in podstawy_wagi if pw[0]!=0 ]
        
    podstawy = [ pod[0] for pod in podstawy_wagi ]
    wagi_podstaw = [ pod[1] for pod in podstawy_wagi ]
    wagi_podstaw = [ w/sum(wagi_podstaw) for w in wagi_podstaw ]
    p = np.random.choice(podstawy, 1, p=wagi_podstaw)[0]
    
    # (krotnosc, jej_waga)
    krotnosci_wagi = [(1,10),(2,5),(3,2)]
    krotnosci = [ k[0] for k in krotnosci_wagi ]
    wagi_krotnosci = [ k[1] for k in krotnosci_wagi ]
    wagi_krotnosci = [ w/sum(wagi_krotnosci) for w in wagi_krotnosci ]
    n = np.random.choice(krotnosci, 1, p=wagi_krotnosci)[0]
    
    # ------------ wybór mnożnika/incrementu i obliczanie wyjściowych wartości --------------------
    
    r = 0
    if schemat=="ciag_arytmetyczny":
        incrementy_wagi = [ (0.5,10), (1,40), (1.5,5), (2,15), (2.5,5), (3,5), (4,5), (5,10), (10,10), \
                           (15,4), (25,10), (50,10), (100,8), (200,6), (250,3), (500,5), (1000,5)]
        # ograniczenia na wartości incrementu
        if n*p>=-5 and n*p<=10: 
            incrementy_wagi = [ iw for iw in incrementy_wagi if iw[0]<=10 ]
        if n*p>=100 and n*p<=1500 or n*p>=2300: 
            incrementy_wagi = [ iw for iw in incrementy_wagi if iw[0]>=25 ]
        if n*p>=20: 
            incrementy_wagi = [ iw for iw in incrementy_wagi if iw[0]==int(iw[0]) ]
        
        incrementy = [ i[0] for i in incrementy_wagi ]
        wagi_incrementow = [ i[1] for i in incrementy_wagi ]
        wagi_incrementow = [ w/sum(wagi_incrementow) for w in wagi_incrementow ]
        r = np.random.choice(incrementy, 1, p=wagi_incrementow)[0]
        values = [ n*p+k*r for k in range(przedmiotow_w_kategorii) ]
        
    elif schemat=="ciag_geometryczny":
        mnozniki_wagi = [ (0.5,10), (2,10), (3,5), (4,4), (5,3), (10,2)]
        # ograniczenia na wartości mnożnika
        if (n*p)%8!=0: 
            mnozniki_wagi = [ mw for mw in mnozniki_wagi if mw[0]>=2 ]
        if (n*p)>=50 and (n*p)%100!=0: 
            mnozniki_wagi = [ mw for mw in mnozniki_wagi if mw[0]==2 or mw[0]==10 ]
        
        mnozniki = [ i[0] for i in mnozniki_wagi ]
        wagi_mnoznikow = [ i[1] for i in mnozniki_wagi ]
        wagi_mnoznikow = [ w/sum(wagi_mnoznikow) for w in wagi_mnoznikow ]
        r = np.random.choice(mnozniki, 1, p=wagi_mnoznikow)[0]
        values = list(np.sort([ n*p*(r**k) for k in range(przedmiotow_w_kategorii) ]))
        
    elif schemat=="ciag_rosnacy":
        r = np.random.choice([n*p, 2*n*p], przedmiotow_w_kategorii, p=[0.8, 0.2])
        values = list(np.sort([ n*p+sum(r[:k]) for k in range(przedmiotow_w_kategorii) ]))
        
    if not isinstance(r, np.ndarray) and r==0:
        raise Exception("Nie udało się wygenerować mnożnika/incrementu r!\nParametry to: p="+str(p)+", n="+str(n)+", schemat="+str(schemat[0]))
        
    # -------------------- określanie możliwych wskazówek ----------------------------
    
    wskazowki = []
    min_free = (przedmiotow_w_kategorii-1)//2+1
    if schemat=="ciag_rosnacy":
        for r1 in [n*p, 2*n*p]:
            # wskazowki addytywne
            for i in range(1,4):
                suma = 0
                for val in values:
                    if val+i*r1 in values:
                        suma += 1
                if suma>=min_free:
                    wskazowki.append("x=y+"+str(i*r1))
            # wskazowki multiplikatywne
            if r1!=1:
                for i in range(1,4):
                    suma = 0
                    for val in values:
                        if val*(r1**i) in values:
                            suma += 1
                    if suma>=min_free:
                        wskazowki.append("x=y*"+str(r1**i))
            if r1!=2:
                for i in range(1,4):
                    suma = 0
                    for val in values:
                        if val*(2**i) in values:
                            suma += 1
                    if suma>=min_free:
                        wskazowki.append("x=y*"+str(2**i))
    else:
        # wskazowki addytywne
        for i in range(1,4):
            suma = 0
            for val in values:
                if val+i*r in values:
                    suma += 1
            if suma>=min_free:
                wskazowki.append("x=y+"+str(i*r))
        # wskazowki multiplikatywne
        if r!=1:
            for i in range(1,4):
                suma = 0
                for val in values:
                    if val*(r**i) in values:
                        suma += 1
                if suma>=min_free:
                    wskazowki.append("x=y*"+str(r**i))
        if r!=2:
            for i in range(1,4):
                suma = 0
                for val in values:
                    if val*(2**i) in values:
                        suma += 1
                if suma>=min_free:
                    wskazowki.append("x=y*"+str(2**i))

    #return schemat[0], values, set(wskazowki)
    return "numerical", values, set(wskazowki)

# ----------------------------- LOSOWANIE INTERPRETACJI ZMIENNYCH NUMERYCZNYCH ---------------------------------------------

def czy_calk(values):
    return all([int(v)==v for v in values])

def czy_dodatnie(values):
    return all([v>0 for v in values])

def czy_ujemne(values):
    return all([v<0 for v in values])

def czy_mniejsze_od(values, C):
    return all([v<C for v in values])

def czy_wieksze_od(values, C):
    return all([v>C for v in values])

def czy_zawieraja(values, C):
    return any([v==C for v in values])

def losuj_interpretacje_num(values):
    
    interpretacje = []
    
    if czy_calk(values) and czy_dodatnie(values):
        interpretacje.append( ("@ rok/lata", 35) )
        interpretacje.append( ("@ klocków",5) )
        interpretacje.append( ("@ punktów",10) )
        
        interpretacje.append( ("@ okruszków",5) )
        interpretacje.append( ("@ ziaren",5) )
        interpretacje.append( ("@ kropelek",5) )
        interpretacje.append( ("@ groszków",5) )
        interpretacje.append( ("@ plamek",5) )
        interpretacje.append( ("@ drobinek",5) )
        interpretacje.append( ("@ liści",5) )
        interpretacje.append( ("@ kapsli",5) )
        interpretacje.append( ("@ pocztówek",3) )
        interpretacje.append( ("@ kulek",5) )
        interpretacje.append( ("@ muszelek",5) )
        interpretacje.append( ("@ drzew",5) )
        interpretacje.append( ("@ kwiatów",5) )
        interpretacje.append( ("@ owadów",5) )
        interpretacje.append( ("@ ton",3) )
        interpretacje.append( ("@ schodów",5) )
        interpretacje.append( ("@ domów",5) )
        interpretacje.append( ("@ ludzi",5) )
        
        interpretacje.append( ("@ gwiazd",4) )
        interpretacje.append( ("@ puzzli",2) )
        interpretacje.append( ("@ zł",35) )
        interpretacje.append( ("@ EUR",15) )
        interpretacje.append( ("@ USD",15) )
        interpretacje.append( ("@ CHF",5) )
        interpretacje.append( ("@ denarów",2) )
        interpretacje.append( ("@ koron",5) )
        
    if czy_calk(values) and czy_mniejsze_od(values, 2040) and czy_wieksze_od(values, 1300):
        interpretacje.append( ("@ rok",100) )
        
    if czy_mniejsze_od(values, 120):
        interpretacje.append( ("@ stopni F",5) )
    
    if czy_mniejsze_od(values, 50):
        interpretacje.append( ("@ stopni C",5) )
    
    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 50):
        interpretacje.append( ("@ pasków",5) )
        interpretacje.append( ("@ misiów",5) )
        interpretacje.append( ("@ lalek",5) )
        interpretacje.append( ("@ miejsce",15) )
        interpretacje.append( ("Nr @",15) )
        interpretacje.append( ("@ dni",10) )
        interpretacje.append( ("@ miesięcy",5) )
        
    if czy_dodatnie(values):
        interpretacje.append( ("@ kg",15) )
        interpretacje.append( ("@ W",5) )
        interpretacje.append( ("@ J",5) )
    
    if czy_dodatnie(values) and czy_mniejsze_od(values, 1000):
        interpretacje.append( ("@ l",15) )
        interpretacje.append( ("@ m",15) )
        interpretacje.append( ("@ s",15) )
        
        
    if czy_dodatnie(values) and czy_mniejsze_od(values, 11):
        interpretacje.append( ("@ szklanki",15) )
        interpretacje.append( ("@ łyżeczki",10) )
        interpretacje.append( ("@ wiaderka",5) )
        interpretacje.append( ("@ koszy",5) )
        interpretacje.append( ("@ filiżanek",5) )
    
    if czy_wieksze_od(values, -0.01) and czy_mniejsze_od(values, 100.001):
        interpretacje.append( ("@ %",5) )
        
    
    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 600):
        interpretacje.append( ("@ stron",5) )
        
    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 10):
        interpretacje.append( ("@ warianty",5) )
        interpretacje.append( ("@-osobowy",15) )
        interpretacje.append( ("@ pasażerów",10) )
        
    
    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 24):
        interpretacje.append( ("Rozpoczęcie",5) )
        interpretacje.append( ("Zakończenie",5) )
        interpretacje.append( ("Kolejność",25) )
        interpretacje.append( ("Sprawdzian",5) )
        interpretacje.append( ("@ interwencji",5) )
        interpretacje.append( ("@:00",25) )
        interpretacje.append( ("@ sztuk",5) )
        interpretacje.append( ("@ groszy",5) )
        
        
    if czy_mniejsze_od(values, 50):
        interpretacje.append( ("zysk/strata",25) )
        
    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 11) and czy_zawieraja(values,1):
        interpretacje.append( ("Kolejność",55) )
     
    if True:
        interpretacje.append( ("Wynik",5) )
        interpretacje.append( ("Liczba",5) )
        interpretacje.append( ("Pomiar",5) )
        interpretacje.append( ("Wartość stałej",5) )
        
    teksty = [ t[0] for t in interpretacje ]
    wagi_tekstów = [ t[1] for t in interpretacje ]
    wagi_tekstów = [ w/sum(wagi_tekstów) for w in wagi_tekstów ]
    tekst = np.random.choice(teksty, 1, p=wagi_tekstów)
    
    return tekst[0], values

# ----------------------------------------- LOSOWANIE WSZYTKIEGO (FKCJA ZBIORCZA) ---------------------------------------------

def losuj_kategorie(K, k, gwiazdki, seed=0):
    np.random.seed(seed)
    
    if K<2:
        raise Exception("Liczba kategorii musi być równa co najmniej 2!")
    if k<3:
        raise Exception("Liczba przedmiotów w kategorii musi być równa co najmniej 3!")
    
    # wyznaczamy rozkład poszczególnych typów kategorii z zależności od liczby gwiazdek
    if gwiazdki==2:
        rozklad = [2, 0.5, 2]
    elif gwiazdki==3:
        rozklad = [2, 0.2, 2]
    elif gwiazdki==4:
        rozklad = [2.5, 0.4, 1.5]
    else:
        raise Exception("Można losować zagadki tylko o liczbie gwiazdek równej 2, 3 albo 4!")
    rozklad = [ r/sum(rozklad) for r in rozklad ]
    
    # wyznaczamy licznosci poszczególnych typów kategorii
    licznosci = ["cat", "num"] # zawsze musi być przynajmniej jedna zmienna kategoryczna i jadna numeryczna
    licznosci += list(np.random.choice(["cat", "ord", "num"], K-2, p=rozklad))
    licznosci = [ sum([l==kat for l in licznosci]) for kat in ["cat", "ord", "num"] ]
    
    # losujemy konkretne kategorie
    wylosowane = []
    # zmienne kategoryczne:
    wylosowane += losuj_schemat_cat(ile=licznosci[0], przedmiotow_w_kategorii=k) 
    # zmienne porządkowe
    wylosowane += losuj_schemat_porz( ile=licznosci[1], przedmiotow_w_kategorii=k) 
    #zmienne numeryczne i ich interpretacje:
    interpretacje = []
    for i in range(licznosci[2]):
        los = losuj_schemat_num(przedmiotow_w_kategorii=k)
        # próbujemy wylosować interpretację, tak żeby się nie powtarzać
        for j in range(20):
            los_interpret = losuj_interpretacje_num(los[1])
            if not los_interpret[0] in interpretacje:
                interpretacje.append(los_interpret[0])
                break
        wylosowane.append( (los[0], los[1], los[2], los_interpret[0]) )
    
    return wylosowane   

# ----------------------------------------- INNE FUNKCJE ---------------------------------------------

def get_string_name(kategorie, K1, i1, replace_polish=False):
    if kategorie[K1][0]=='cathegorical' or kategorie[K1][0]=='ordinal':
        name = kategorie[K1][1][i1]
    else :
        number = str(kategorie[K1][1][i1])
        if number.endswith(".0"):
            number = number[:-2] 
        if "@" in kategorie[K1][3]:
            a = kategorie[K1][3].split("@")
            name = number.join(a)
        else:
            name = number
    
    if replace_polish:
        if "ł" in name:
            name = "l".join(name.split("ł"))
        if "Ł" in name:
            name = "L".join(name.split("Ł"))
        if "ś" in name:
            name = "s".join(name.split("ś"))
        if "Ś" in name:
            name = "S".join(name.split("Ś"))
        if "ć" in name:
            name = "c".join(name.split("ć"))
        if "Ć" in name:
            name = "C".join(name.split("Ć"))
        if "ą" in name:
            name = "a".join(name.split("ą"))
        if "ę" in name:
            name = "e".join(name.split("ę"))
        if "ż" in name:
            name = "z".join(name.split("ż"))
        if "ź" in name:
            name = "z".join(name.split("ź"))
        if "Ż" in name:
            name = "Z".join(name.split("Ż"))
        if "Ź" in name:
            name = "Z".join(name.split("Ź"))
        if "ń" in name:
            name = "n".join(name.split("ń"))
            
    return name

def do_cathegories_repeat(cathegories):
    all_cats = []
    for i, cat in enumerate(cathegories):
        cats_i = [ get_string_name(cathegories, i, j) for j in range(len(cat[1])) ]
        all_cats += cats_i
    return len(all_cats) != len(set(all_cats))

