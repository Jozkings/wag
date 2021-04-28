"""gui and graph variables"""
OPERATIONS = {"order": "Zisťujem počet vrcholov", "size": "Zisťujem počet hrán", "density": "Počítam hustotu grafu",
              "max_degree": "Zisťujem vrchol s najväčším stupňom", "min_degree": "Zisťujem vrchol s najmenším stupňom",
              "avg_degree": "Počítam priemerný stupeň uzla", "clust_coeff": "Počítam klasterizačný koeficient grafu",
              "s_p_d": "Počítam všetky najkratšie cesty", "finish1": "Hotovo", "edge_list": "Vytváram množinu hrán",
              "o_computing": "Počítam orbity", "g_analysis": "Aplikujem grafletovú analýzu",
              "g_reading": "Načítavam výsledky", "g_saving": "Ukladám výsledky", "finish2": "Hotovo",
              "files": "Získavám potrebné súbory", "rg": "Vykonávam analýzu", "res": "Získavam výsledky",
              "a_saving": "Ukladám výsledky", "finish3": "Hotovo"}
LABELS = {0: "Počet vrcholov:", 1: "Počet hrán:", 2: "Hustota grafu:", 3: "Maximálny stupeň uzla:",
          4: "Minimálny stupeň uzla:", 5: "Priemerný stupeň uzla:", 6: "Klasterizačný koeficient grafu:",
          7: "Priemer siete:",8: "Priemerná najkratšia cesta:", 9: "Počet súvislých grafletov veľkosti 2:",
          10: "Počet súvislých grafletov veľkosti 3:", 11: "Počet súvislých grafletov veľkosti 4:",
          12: "Počet súvislých grafletov veľkosti 5:", 13: "RGFD:", 14: "GDDA:"}
DISTRIBUTIONS = {0: "Distribúcia - počet uzlov / stupeň uzla",
                 1: "Normalizovaná distribúcia - počet uzlov / stupeň uzla",
                 2: "Distribúcia - najkratšie cesty", 3: "Distribúcia - klasterizačný koeficient",
                 4: "Distribúcia - klasterizačný koeficient / stupeň uzla"}
SINGLE_STATS = {0: "Stupeň uzla", 1: "Klasterizačný koeficient uzla", 2: "Počet výskytov uzla"}
GRAPHLETS_STATS = {0: "Všetky graflety veľkosti 2", 1: "Všetky graflety veľkosti 3", 2: "Všetky graflety veľkosti 4"}
GRAPHLETS_TYPES = ["edge", "2-node-independent", "triangle", "2-star", "3-node-1-edge", "3-node-independent",
                   "4-clique", "4-chordalcycle", "4-tailedtriangle", "4-cycle", "3-star", "4-path", "4-node-1-triangle",
                   "4-node-2-star", "4-node-2-edge", "4-node-1-edge", "4-node-independent"]

"""gui informations texts"""
GRAPHLETS_INFO = "Graflety sú malé neizomorfné indukované podgrafy veľkej siete.\nHoci sa väčšinou o grafletoch hovorí ako " \
               "súvislých (existuje cesta medzi všetkými vrcholmi),\nvieme rozoznať aj nesúvislé graflety.\n\n" \
               "Graflety sú schopné zistiť špecifiká vnútornej štruktúry siete lepšie\nako všeobecné vlastnosti grafu " \
               "(ako napr. stupeň uzla). Pri ich skúmaní porovnávame ich frekvencie,\nči už ako celkového počtu grafletov danej" \
               " veľkosti (zvyčajne 2-5 uzlov, \nväčšie graflety sú časovo náročné na hľadanie), alebo slúžia pre ďalšie štatistiky" \
               " (RGFD, GDDA)\n\nNázvy grafletov veľkosti 2-4, ktoré sa hľadajú v aplikácii predstavujú nasledujúce graflety:\n" \
               "(prevzaté z: Ahmed et al.: Graphlet Decomposition: Framework, Algorithms, and Applications)\n\n"

GRAPHLETS_INFO2 = "Ak nás zaujíma aj topologické rozdelenie grafletov (ako napr. pri GDDA), \nskúmame tzv. " \
                "automorfizované orbity. Zobrazené orbity nižšie sú v graflete rozdelené rozdielnou farbou. \n" \
                "(prevzaté z: Pržulj Nataša: Biological network comparison using graphlet degree distribution)"

GRAPHS_INFO = "Pojem graf v matematike predstavuje objekt daný množinou vrcholov (uzlov)\na množinou hrán," \
               "ktoré tieto vrcholy spájajú. V tejto aplikácii reprezentujú grafy slovné siete,\n" \
               "ktoré boli vytvorené zo zadaných dát.\nSlovné siete, ktoré vytvára " \
               "táto aplikácia vyznačujú syntaktickú stránku textu.\nVytvárajú sa z textu nasledovným spôsobom:\n\n" \
               "   1. Aplikácia načíta slovo z textu.\n   2. Slovo sa pridá do siete ako vrchol\n   3. Bezprostredný ľavý " \
               "a pravý sused slova vo vete sa zaznačí ako sused slova - pomocou hrany v sieti\n\nTakto vytvorený graf " \
               "následne možno štatisticky skúmať.\n\n" \
               "Aplikácia primárne slúži pre skúmanie anglických textov. Je tomu prispôsobená tak, že sama dokáže\n" \
               "identifikovať množstvo skrátenýchanglických tvarov, ako napr. I'm alebo He'll, a správne ich rozdeliť\n" \
               "na viacero slov pre čo najväčšiu prenosť štatistík.\n\nVytvorené grafy sú neorientované (nezáleží na" \
               "tom, ktoré slovo z dvojice sa vyskytlo v texte ako prvé)\na bez slučiek (slovo nie je susedom samého seba) \n\n" \
               "Namiesto druhej slovnej siete vytvorenej z textu možno vytvoriť sieť ako náhodný graf, ktorý má rovnaký počet\n" \
               "uzlov a hrán ako prvá slovná sieť. Náhodný graf je špeciálneho modelu G(N+x,m), kde x navyše vrcholov\n" \
               "sa v procese zmaže a zaisťuje správne finálne rozmery siete."

GRAPHLETS_STATS_INFO = "Počet súvislých grafletov: Celkový počet súvislých podgrafov siete danej veľkosti\n" \
               "Počet nesúvislých grafletov: Celkový počet nesúvislých podgrafov siete danej veľkosti\n" \
               "Počet konkrétneho typu grafletu do veľkosti 4: viď 'O grafletoch'"

GRAPHS_STATS_INFO = "Počet vrcholov/uzlov |V| = N: počet unikátnych slov rozpoznaných aplikáciou\n" \
               "Počet hrán |E|: Počet vzájomných interakcií slov v texte (počet susedstiev vo vetách)\n" \
               "Hustota grafu D: Vyjadrenie pomeru počtu vrcholov a hrán\n" \
               "Maximálny stupeň uzla : Vrchol s najväčším počtom napojených hrán\n" \
               "Minimálny stupeň uzla : Vrchol s nejmenším počtom napojených hrán\n" \
               "Priemerný stupeň uzla : Priemer stupňov uzlov v grafe\n" \
               "Klasterizačný koeficient grafu C: Priemerný klasterizačný koeficient uzlov \n(pomer počtu " \
               "existujúcich hrán uzla ku teoreticky všetkým možným)\n" \
               "Priemerná najkratšia cesta L: Priemer najkratších možných ciest z každého vrchola grafu ku " \
               "každému inému vrcholu grafu\n"

GRAPHLETS_COMPARISION_INFO = "Relative graphlet frequency distance porovnáva frekvencie počtov grafletov\ndo veľkosti 5 uzlov " \
               "dvoch rôznych grafov. Výsledná hodnota vyjadruje podobnosť grafov v tomto\nohľade početnosti, " \
               "pričom sa snaží eliminovať vplyv veľkosti grafov (teda počtu uzlov a hrán).\nTáto štatistika sa teda " \
               "viac zameriava na menšie vnútorne štruktúry veľkých sietí.\n\n" \
                "Výsledná hodnota je číslo, ktoré predstavuje vzdialenosť sietí. Výsledok pod hodnotu\n" \
                "50 predstavuje výsledok relatívne blízkych sietí v tomto ohľade."

padd = " "*18

GRAPHLETS_COMPARISION_INFO2 = f"{padd}Graphlet degree distribution agreement predstavuje zovšeobecnenie distribúcie uzlov\n{padd}na spektrum " \
                f"grafletových distribúcií. Tak, ako pri stupni uzla\n{padd}skúmame počet dotykov uzla, tak v tejto " \
                f"štatistike podobne skúmame dotyky, \n{padd}avšak tentokrát grafletov. Taktiež vhľadom na to, že graflety " \
                f"sú zložené z viacerých uzlov,\n{padd}je často dôležité zisťovať, ktorý uzol v danom type grafletu je " \
                f"dotykový.\n{padd}Preto sa graflety rozdeľujú na tzv. automorfizované orbity, ktoré zohľadňujú " \
                f"topologické rozloženie grafletov.\n\n{padd}Výsledná hodnota sa získa aplikovaním aritmetického alebo " \
                f"geometrického priemeru, \n{padd}pričom čím bližšia je výsledná hodnota k 1, tým bližšie sú si siete."

DISTRIBUTIONS_INFO = "Distribúcie označené * využívajú pri vykresľovaní logaritmický binning\n\n"\
               "Počet uzlov / stupeň uzla : Počet uzlov so stupňom k pre všetky k nachádzajúce sa v grafe\n" \
               "*Normalizácia - počet uzlov / stupeň uzla : Počet uzlov " \
               "vydelený \n  celkovým počtom uzlov so stupňom k pre všetky k nachádzajúce sa v grafe\n" \
               "Najkratšie cesty: Počet najkratších ciest dvoch vrcholov s dĺžkou n pre všetky n\n" \
               "Klasterizačný koeficient: Počet uzlov s klasterizačným koeficientom c" \
               " pre všetky k nachádzajúce sa v grafe\n" \
               "*Klasterizačný koeficient / stupeň uzla : Priemerný klasterizačný koeficient c všetkých " \
               "uzlov\n  so stupňom k pre všetky k nachádzajúce sa v grafe"
"""graph variables"""
FORM_NEUTRAL_S = 'has/is/does'
FORM_NEUTRAL_D = 'had/would/did'
G_OPERATIONS = ["order", "size", "density", "max_degree", "min_degree", "avg_degree", "clust_coeff", "s_p_d",
                "finish1", "edge_list", "o_computing", "g_analysis", "g_reading", "g_saving", "finish2",
                "files", "rg", "res", "a_saving", "finish3"]