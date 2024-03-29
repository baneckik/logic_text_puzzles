from numpy import random, unique, sort, ndarray
from pandas import read_csv
from pathlib import Path


# ----------------------------------------- Drawing categorical categories ---------------------------------------------


def draw_cat_scheme(ile=1, puzzle_k=5):
    if ile < 1:
        return []

    # drawing folders
    folders_weights = [("activities", 3), ("geography", 3), ("items", 5), ("names", 12), ("nature", 4),
                       ("other_concepts", 5), ("special_names", 6)]
    folder_names = [fw[0] for fw in folders_weights]
    weights_folder = [fw[1] for fw in folders_weights]
    weights_folder = [w / sum(weights_folder) for w in weights_folder]

    if ile < 6:
        if random.uniform(0, 1) < 0.75:
            folders = random.choice(folder_names, ile, p=weights_folder, replace=False)
        else:
            folders = random.choice(folder_names, ile, p=weights_folder, replace=True)
    else:
        folders = random.choice(folder_names, ile, p=weights_folder, replace=True)

    # drawing categories from folders
    chosen = []
    for folder in unique(folders):
        available_cats = []
        available_weights = []
        for path in Path('categories/categorical/' + folder).rglob('*.txt'):
            kat = read_csv(path, header=None)
            if kat.shape[0] - 1 >= puzzle_k:
                available_cats.append(path)
                available_weights.append(int(kat.iloc[0, 0].split(" ")[-1]))
        available_weights = [w / sum(available_weights) for w in available_weights]

        # number of categories to draw from this folder
        ile_kat = sum([f == folder for f in folders])
        if len(available_cats) < ile_kat:
            raise Exception("Cannot find " + str(ile) + " categorical categories for " \
                            + str(puzzle_k) + " objects in each category!")

        chosen += list(random.choice(available_cats, ile_kat, p=available_weights, replace=False))

    chosen_out = []
    for c in chosen:
        if c == Path("categories/categorical/special_names/zmysleni_superbohaterowie_ang.txt"):
            kat = read_csv(c, header=None, skiprows=[0], sep=" ")
            prenames = random.choice(kat.iloc[:, 0], puzzle_k, replace=False)
            if puzzle_k < 5:
                n = 1
            else:
                n = 2
            counts = [0] * n + [1] * n
            counts += list(random.choice([0, 1], puzzle_k - len(counts), replace=True))
            names_male = random.choice(kat.iloc[:, 1], len([i for i in counts if i == 0]), replace=False)
            names_female = random.choice(kat.iloc[:, 2], len([i for i in counts if i == 1]), replace=False)
            names = list(names_male) + list(names_female)
            names = [prenames[i] + " " + names[i] for i in range(len(prenames))]
        elif c == Path("categories/categorical/special_names/zmysleni_superbohaterowie_pol.txt"):
            kat = read_csv(c, header=None, skiprows=[0], sep=" ")
            rows = random.choice(range(kat.shape[0]), puzzle_k, replace=False)
            if puzzle_k < 5:
                n = 1
            else:
                n = 2
            counts = [0] * n + [1] * n
            counts += list(random.choice([0, 1], puzzle_k - len(counts), replace=True))
            names = []
            for j, i in enumerate(rows):
                if counts[j] == 0:
                    names.append(kat.iloc[i, 0] + " " + kat.iloc[i, 2])
                else:
                    names.append(kat.iloc[i, 1] + " " + kat.iloc[i, 3])
        else:
            kat = read_csv(c, header=None)
            kat.drop(kat.head(1).index, inplace=True)
            names = list(random.choice(kat.iloc[:, 0], puzzle_k, replace=False))
        chosen_out.append(names)

    chosen_out2 = [{'typ': "categorical", 'names': chosen_out[i], 'cross_bar': "", 'groups': [0] * puzzle_k} for i in
                   range(len(chosen_out))]

    # replacement some categories for grouped categories

    # possible grouped data:
    grouped_data = [
        (10, ["Anna", "Aleksandra", "Amelia", "Agata", "Anastazja", "Alicja", "Aniela", "Apolonia", "Adrianna", "Aneta",
              "Anita", "Antonina"],
         ["Adam", "Artur", "Albert", "Alfons", "Adolf", "Ambroży", "Adrian", "Aleksander", "Andrzej", "Arnold",
          "Alojzy", "Antoni"]),
        (15,
         ["Zuzanna", "Julia", "Zofia", "Hanna", "Maja", "Lena", "Alicja", "Oliwia", "Laura", "Maria", "Pola", "Amelia",
          "Emilia", "Antonina", "Wiktoria", "Aleksandra", "Marcelina", "Liliana", "Iga", "Helena", "Katarzyna",
          "Teresa", "Danuta"],
         ["Jan", "Antoni", "Jakub", "Aleksander", "Franciszek", "Szymon", "Filip", "Mikołaj", "Stanisław", "Wojciech",
          "Leon", "Adam", "Kacper", "Nikodem", "Marcel", "Tymon", "Ignacy", "Michał", "Wiktor", "Piotr", "Krzysztof",
          "Ryszard", "Grzegorz"]),
        (4, ["kot", "pies", "koza", "krowa", "koń", "byk", "owca", "jeleń", "sarna", "małpa", "słoń", "żyrafa", "lew",
             "tygrys", "zebra", "antylopa", "łoś", "dzik", "mysz", "szczur", "wiewiórka", "kret", "królik", "zając",
             "wilk"],
         ["krokodyl", "gawial", "aligator", "jaszczurka", "kameleon", "zwinka", "bazyliszek", "gekon", "iguana",
          "legwan", "żółw", "zaskroniec", "boa", "wąż Eskulapa", "żmija", "kobra"]),
        (5, ["Portugalia", "Hiszpania", "Francja", "Anglia", "Irlandia", "Islandia", "Włochy", "Luksemburg", "Belgia",
             "Holandia", "Niemcy", "Dania", "Szwecja", "Norwegia", "Finlandia", "Estonia", "Łotwa", "Litwa", "Białoruś",
             "Polska", "Ukraina", "Mołdawia", "Rumunia", "Bułgaria", "Grecja", "Malta", "Albania", "Macedonia Płn.",
             "Serbia", "Kosowo", "Czarnogóra", "Bośnia", "Chorwacja", "Słowenia", "Austria", "Liechtenstein",
             "Szwajcaria", "Czechy", "Słowacja", "Węgry"],
         ["ALgieria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Czad", "Dżibuti", "Egipt", "Erytrea",
          "Etiopia", "Gabon", "Gambia", "Ghana", "Gwinea", "Kamerun", "Kenia", "Komory", "Kongo", "Lesotho", "Liberia",
          "Libia", "Madagaskar", "Malawi", "Mali", "Maroko", "Mauretania", "Mauritius", "Mozambik", "Namibia", "Niger",
          "Nigeria", "RPA", "Rwanda", "Senegal", "Seszele", "Sierra Leone", "Somalia", "Sudan", "Tanzania", "Togo",
          "Tunezja", "Uganda", "Zambia", "Zimbabwe"])
    ]
    poss_grouped_data = [gp for gp in grouped_data if len(gp[1]) >= puzzle_k and len(gp[2]) >= puzzle_k]

    # how many categorical categories are to be replaced by grouped categories (to_replace):
    if puzzle_k == 3:
        to_replace = 0  # no grouped categories allowed when k=3
    elif ile == 1:
        to_replace = random.choice([1, 0, 0, 0, 0])
    elif ile == 2:
        to_replace = random.choice([2, 1, 1, 0, 0, 0, 0])
    else:
        to_replace = random.choice([3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0])

    if to_replace > 0:
        weights = [p[0] for p in poss_grouped_data]
        chosen_i = random.choice(range(len(poss_grouped_data)), to_replace, p=[w / sum(weights) for w in weights],
                                 replace=False)
        chosen = [poss_grouped_data[chosen_i[i]] for i in range(to_replace)]

        replacements = []
        for ch in chosen:
            if puzzle_k == 3:
                ile0 = random.randint(1, 3)
                ile1 = puzzle_k - ile0
            else:
                ile0 = random.randint(2, puzzle_k - 1)
                ile1 = puzzle_k - ile0
            group0_names = random.choice(ch[1], ile0, replace=False)
            group1_names = random.choice(ch[2], ile1, replace=False)
            rand_order = random.permutation([(0, g0) for g0 in group0_names] + [(1, g1) for g1 in group1_names])
            g_names = [g[1] for g in rand_order]
            g_groups = [g[0] for g in rand_order]
            replacements.append({'typ': "categorical", 'names': g_names, 'cross_bar': "", 'groups': g_groups})

        cat_to_replace = random.choice(range(ile), to_replace)
        for i, j in enumerate(cat_to_replace):
            chosen_out2[j] = replacements[i]

    return chosen_out2


# ----------------------------------------- Drawing ordinal categories ---------------------------------------------

def draw_ord_scheme(ile=1, puzzle_k=5):
    if ile < 1:
        return []

    available_cats = []
    available_weights = []
    for path in Path('categories/ordinal').rglob('*.txt'):
        kat = read_csv(path, header=None)
        if kat.shape[0] - 1 >= puzzle_k:
            available_cats.append(path)
            available_weights.append(int(kat.iloc[0, 0].split(" ")[-1]))
    available_weights = [w / sum(available_weights) for w in available_weights]

    if len(available_cats) < ile:
        raise Exception("Cannot find " + str(ile) + " ordinal categories for "
                        + str(puzzle_k) + " objects in each category!")

    chosen = random.choice(available_cats, ile, p=available_weights, replace=False)
    chosen_out = []
    for c in chosen:
        kat = read_csv(c, header=None)
        start = int(random.choice(range(1, kat.shape[0] - puzzle_k + 1), 1))
        names = list(kat.iloc[start:(start + puzzle_k), 0])
        chosen_out.append(names)

    final_categories = [{'typ': "ordinal", 'names': chosen_out[i], 'cross_bar': ""} for i in range(len(chosen_out))]

    # numerical interpretation for ordinal categories like 'days of the week' or 'months':
    for path_i, path in enumerate(chosen):
        if path == Path("categories/ordinal/miesiace.txt") or path == Path("categories/ordinal/dni_tygodnia.txt"):
            min_free = (puzzle_k - 1) // 2 + 1
            clues_candidates = []
            values = range(1, puzzle_k + 1)
            for i in range(1, 4):
                suma = 0
                for val in values:
                    if val + i in values:
                        suma += 1
                if suma >= min_free:
                    clues_candidates.append("x=y+" + str(i))
            final_categories[path_i]["pre_clues"] = clues_candidates

    return final_categories


# ----------------------------------------- Drawing numerical categories ---------------------------------------------

def draw_num_scheme(puzzle_k=5):
    # ---------------------- choice of the scheme and first element in a sequence=n*p ---------------------------------

    # (scheme, its_weight)
    schemes_weights = [("arithmetic_sequence", 10), ("geometric_sequence", 2), ("ascending_sequence", 3)]
    schemes = [t[0] for t in schemes_weights]
    weights = [t[1] for t in schemes_weights]
    weights = [w / sum(weights) for w in weights]
    scheme = random.choice(schemes, 1, p=weights)

    # (base_value(p), its_weight)
    base_weights = [(-40, 1), (-10, 1), (-5, 1), (0, 1), (1, 20), (1.50, 5), (2, 10), (2.50, 5), (3, 4), (4, 4), (5, 3),
                    (6, 3),
                    (7, 2), (8, 2), (9, 2), (10, 5), (20, 5), (50, 5), (100, 6), (1000, 6), (1500, 4), (1920, 1),
                    (1950, 1), (1980, 1), (1990, 1), (2000, 4)]
    # limitations of the base value p
    if scheme == "geometric_sequence":
        base_weights = [bw for bw in base_weights if 10 >= bw[0] > 0]
    if scheme == "ascending_sequence":
        base_weights = [bw for bw in base_weights if bw[0] != 0]

    base_values = [bw[0] for bw in base_weights]
    weights = [bw[1] for bw in base_weights]
    weights = [w / sum(weights) for w in weights]
    p = random.choice(base_values, 1, p=weights)[0]

    # (times factor(n), its_weight)
    times_weights = [(1, 10), (2, 4), (3, 1)]
    times_factors = [k[0] for k in times_weights]
    weights = [k[1] for k in times_weights]
    weights = [w / sum(weights) for w in weights]
    n = random.choice(times_factors, 1, p=weights)[0]

    # ------------ choice of the multiplier/increment and counting the final numerical values --------------------

    r = 0
    if scheme == "arithmetic_sequence":
        increment_weights = [(0.5, 10), (1, 40), (1.5, 5), (2, 15), (2.5, 5), (3, 5), (4, 5), (5, 10), (10, 10),
                             (15, 4), (25, 10), (50, 10), (100, 8), (200, 6), (250, 3), (500, 5), (1000, 5)]
        # limitation on the increment value (r)
        if -5 <= n * p <= 10:
            increment_weights = [iw for iw in increment_weights if iw[0] <= 10]
        if 100 <= n * p <= 1500 or n * p >= 2300:
            increment_weights = [iw for iw in increment_weights if iw[0] >= 25]
        if n * p >= 20:
            increment_weights = [iw for iw in increment_weights if iw[0] == int(iw[0])]

        increments = [i[0] for i in increment_weights]
        weights = [i[1] for i in increment_weights]
        weights = [w / sum(weights) for w in weights]
        r = random.choice(increments, 1, p=weights)[0]
        values = [n * p + k * r for k in range(puzzle_k)]

    elif scheme == "geometric_sequence":
        multiplier_weights = [(2, 15), (3, 5), (4, 4), (5, 3), (10, 2)]
        # limitation on the multiplier value (r)
        if (n * p) >= 50 and (n * p) % 100 != 0:
            multiplier_weights = [mw for mw in multiplier_weights if mw[0] == 2 or mw[0] == 10]

        multipliers = [i[0] for i in multiplier_weights]
        weights = [i[1] for i in multiplier_weights]
        weights = [w / sum(weights) for w in weights]
        r = random.choice(multipliers, 1, p=weights)[0]
        values = list(sort([n * p * (r ** k) for k in range(puzzle_k)]))

    elif scheme == "ascending_sequence":
        r = [n * p, 2 * n * p]
        r += list(random.choice([n * p, 2 * n * p], puzzle_k - 3, p=[0.8, 0.2]))
        r = list(random.permutation(r))
        values = list(sort([n * p + sum(r[:k]) for k in range(puzzle_k)]))

    if not isinstance(r, ndarray) and r == 0:
        raise Exception("Cannot generate multiplier/increment r!\nParameters are: p=" + str(p) + ", n=" + str(n)
                        + ", scheme=" + str(scheme))

    # -------------------- determining possible clues of type 3 ----------------------------

    clues_candidates = []
    min_free = (puzzle_k - 1) // 2 + 1
    if scheme == "ascending_sequence":
        for r1 in [n * p, 2 * n * p]:
            # additive clues
            for i in range(1, 4):
                suma = 0
                for val in values:
                    if val + i * r1 in values:
                        suma += 1
                if suma >= min_free:
                    clues_candidates.append("x=y+" + str(i * r1))
            # multiplicative clues
            if r1 != 1:
                for i in range(1, 4):
                    suma = 0
                    for val in values:
                        if val * (r1 ** i) in values:
                            suma += 1
                    if suma >= min_free:
                        clues_candidates.append("x=y*" + str(r1 ** i))
            if r1 != 2:
                for i in range(1, 4):
                    suma = 0
                    for val in values:
                        if val * (2 ** i) in values:
                            suma += 1
                    if suma >= min_free:
                        clues_candidates.append("x=y*" + str(2 ** i))
    else:
        # additive clues
        for i in range(1, 4):
            suma = 0
            for val in values:
                if val + i * r in values:
                    suma += 1
            if suma >= min_free:
                clues_candidates.append("x=y+" + str(i * r))
        # multiplicative clues
        if r != 1:
            for i in range(1, 4):
                suma = 0
                for val in values:
                    if val * (r ** i) in values:
                        suma += 1
                if suma >= min_free:
                    clues_candidates.append("x=y*" + str(r ** i))
        if r != 2 and scheme == "arithmetic_sequence":
            for i in range(1, 4):
                suma = 0
                for val in values:
                    if val * (2 ** i) in values:
                        suma += 1
                if suma >= min_free:
                    clues_candidates.append("x=y*" + str(2 ** i))

    # return schemat[0], values, clues_candidates
    return {'typ': "numerical", 'names': values, 'pre_clues': clues_candidates, 'seq_scheme': scheme[0].split("_")[0],
            "r": r}


# ----------------------------- drawing numerical interpretations ---------------------------------------------

def czy_calk(values):
    return all([int(v) == v for v in values])


def czy_dodatnie(values):
    return all([v > 0 for v in values])


def czy_ujemne(values):
    return all([v < 0 for v in values])


def czy_mniejsze_od(values, C):
    return all([v < C for v in values])


def czy_wieksze_od(values, C):
    return all([v > C for v in values])


def czy_zawieraja(values, C):
    return any([v == C for v in values])


def draw_num_interpretation(values):
    interpretacje = []

    if czy_calk(values) and czy_dodatnie(values):
        interpretacje.append(("@ rok/lata", 35))
        interpretacje.append(("@ klocków", 5))
        interpretacje.append(("@ punktów", 10))

        interpretacje.append(("@ okruszków", 5))
        interpretacje.append(("@ ziaren", 5))
        interpretacje.append(("@ kropelek", 5))
        interpretacje.append(("@ groszków", 5))
        interpretacje.append(("@ plamek", 5))
        interpretacje.append(("@ drobinek", 5))
        interpretacje.append(("@ liści", 5))
        interpretacje.append(("@ kapsli", 5))
        interpretacje.append(("@ pocztówek", 3))
        interpretacje.append(("@ kulek", 5))
        interpretacje.append(("@ muszelek", 5))
        interpretacje.append(("@ drzew", 5))
        interpretacje.append(("@ kwiatów", 5))
        interpretacje.append(("@ owadów", 5))
        interpretacje.append(("@ ton", 3))
        interpretacje.append(("@ schodów", 5))
        interpretacje.append(("@ domów", 5))
        interpretacje.append(("@ ludzi", 5))

        interpretacje.append(("@ gwiazd", 4))
        interpretacje.append(("@ puzzli", 2))
        interpretacje.append(("@ zł", 35))
        interpretacje.append(("@ EUR", 15))
        interpretacje.append(("@ USD", 15))
        interpretacje.append(("@ CHF", 5))
        interpretacje.append(("@ denarów", 2))
        interpretacje.append(("@ koron", 5))

    if czy_calk(values) and czy_mniejsze_od(values, 2040) and czy_wieksze_od(values, 1300):
        interpretacje.append(("@ rok", 100))

    if czy_mniejsze_od(values, 120) and czy_wieksze_od(values, -460):
        interpretacje.append(("@ stopni F", 5))

    if czy_mniejsze_od(values, 100) and czy_wieksze_od(values, -273):
        interpretacje.append(("@ stopni C", 5))

    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 50):
        interpretacje.append(("@ pasków", 5))
        interpretacje.append(("@ misiów", 5))
        interpretacje.append(("@ lalek", 5))
        interpretacje.append(("@ miejsce", 15))
        interpretacje.append(("Nr @", 15))
        interpretacje.append(("@ dni", 15))
        interpretacje.append(("@ miesięcy", 5))
        interpretacje.append(("kanał @", 5))

    if czy_dodatnie(values):
        interpretacje.append(("@ kg", 15))
        interpretacje.append(("@ W", 5))
        interpretacje.append(("@ J", 5))

    if czy_dodatnie(values) and czy_mniejsze_od(values, 1000):
        interpretacje.append(("@ l", 15))
        interpretacje.append(("@ m", 15))
        interpretacje.append(("@ s", 15))

    if czy_dodatnie(values) and czy_mniejsze_od(values, 11):
        interpretacje.append(("@ szklanki", 15))
        interpretacje.append(("@ łyżeczki", 10))
        interpretacje.append(("@ wiaderka", 5))
        interpretacje.append(("@ koszy", 5))
        interpretacje.append(("@ filiżanek", 5))

    if czy_wieksze_od(values, -0.01) and czy_mniejsze_od(values, 100.001):
        interpretacje.append(("@ %", 10))

    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 600):
        interpretacje.append(("@ stron", 10))
        interpretacje.append(("@ MHz", 5))

    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 10):
        interpretacje.append(("@ warianty", 5))
        interpretacje.append(("@-osobowy", 15))
        interpretacje.append(("@ pasażerów", 10))

    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 24):
        interpretacje.append(("Rozpoczęcie", 5))
        interpretacje.append(("Zakończenie", 5))
        interpretacje.append(("Sprawdzian", 5))
        interpretacje.append(("@ interwencji", 5))
        interpretacje.append(("@:00", 25))
        interpretacje.append(("@ sztuk", 5))
        interpretacje.append(("@ groszy", 5))

    if czy_mniejsze_od(values, 50):
        interpretacje.append(("zysk/strata", 25))

    if czy_calk(values) and czy_dodatnie(values) and czy_mniejsze_od(values, 11) and czy_zawieraja(values, 1):
        interpretacje.append(("Kolejność", 55))

    if True:
        interpretacje.append(("Wynik", 5))
        interpretacje.append(("Liczba", 5))
        interpretacje.append(("Pomiar", 5))
        interpretacje.append(("Wartość stałej", 5))

    teksty = [t[0] for t in interpretacje]
    weights_text = [t[1] for t in interpretacje]
    weights_text = [w / sum(weights_text) for w in weights_text]
    tekst = random.choice(teksty, 1, p=weights_text)

    return tekst[0], values


# ----------------------------------------- Collective function ---------------------------------------------

def draw_category(K, k, diff=3, seed=0):
    if K < 2:
        raise Exception("Number of categories (K) must be at least 2!")
    if k < 3:
        raise Exception("Number of objects in each category (k) must be at least 3!")

    random.seed(seed)

    # determining probability distribution of categories types (categorical, ordinal, numerical) depending on diff
    if diff == 2:
        distribution = [2, 0.5, 2]
    elif diff == 3:
        distribution = [2, 0.3, 2]
    elif diff == 4:
        distribution = [2.5, 0.4, 1.5]
    else:
        raise Exception("diff must be either 2, 3 or 4!")
    distribution = [d / sum(distribution) for d in distribution]

    # determining the count of the category types
    cat_counts = ["cat", "num"]  # always has to be at least one categorical and one numerical category
    cat_counts += list(random.choice(["cat", "ord", "num"], K - 2, p=distribution))
    cat_counts = [sum([l == kat for l in cat_counts]) for kat in ["cat", "ord", "num"]]

    # drawing specific categories
    drawn = []
    # categorical:
    drawn += draw_cat_scheme(ile=cat_counts[0], puzzle_k=k)
    # ordinal:
    drawn += draw_ord_scheme(ile=cat_counts[1], puzzle_k=k)
    # numerical and their interpretations:
    interpretations = []
    for i in range(cat_counts[2]):
        los = draw_num_scheme(puzzle_k=k)
        # trying to draw an interpretation, without repetitions
        for j in range(50):
            los_interpret = draw_num_interpretation(los["names"])
            if not los_interpret[0] in interpretations:
                interpretations.append(los_interpret[0])
                break
        if "@" in los_interpret[0]:
            los["interpretation"] = los_interpret[0]
            los["cross_bar"] = ""
        else:
            los["interpretation"] = ""
            los["cross_bar"] = los_interpret[0]
        drawn.append(los)

    return drawn


# ----------------------------------------- Other functions ---------------------------------------------

def get_string_name(categories, K1, i1, replace_polish=False, with_bar=False, add_info=False):
    if categories[K1]['typ'] == 'categorical' or categories[K1]['typ'] == 'ordinal':
        name = categories[K1]['names'][i1]
    else:
        number = str(categories[K1]['names'][i1])
        if number.endswith(".0"):
            number = number[:-2]
        if "@" in categories[K1]['interpretation']:
            a = categories[K1]['interpretation'].split("@")
            name = number.join(a)
        else:
            name = number

    if with_bar:
        name = categories[K1]['cross_bar'] + ":::" + name

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

    if add_info:
        name += "(K" + str(K1) + ")"

    return name


def do_categories_repeat(categories, with_bar=True):
    all_cats = []
    for i, cat in enumerate(categories):
        cats_i = [get_string_name(categories, i, j, with_bar=with_bar) for j in range(len(cat['names']))]
        all_cats += cats_i
    return len(all_cats) != len(set(all_cats))
