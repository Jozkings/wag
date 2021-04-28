# WAG
Word network Analysis using Graph statitics

The application is used to analyze word networks created from text. After loading the text (or directly network), application can analyze this network using various graph and graphlet methods. Results can be saved or compared directly in the application thanks to a simple graphical user interface not only numerically but also graphically.

The application is primarily intended for the Windows operating system. The libraries that the application runs with are:
- matplotlib 3.1.0
- networkx 2.4
- tkinter 8.6

In addition, it uses its own implementation of the pseudocode of the PGD algorithm and the implementation of the ORCA algorithm. Both algorithms are freely available and described here:
- PGD: http://nesreenahmed.com/publications/ahmed-et-al-icdm2015.pdf
- ORCA: tinyurl.com/3hcnj27n

Graph statistics that the application can calculate:
- number of nodes
- number of edges
- maximum node degree 
- minimum node degree
- average node degree
- average clustering coefficient
- graph density
- average shortest distance of the graph
- graph diameter

Graphlet statistics that the application can calculate:
- number of connected graphlets of size 2-5
- number of disconnected graphlets of size 2-4
- RGFD analysis
- GDDA analysis

In addition, different distributions and node statitics can be calculated. Usage: finding the scalelessness of a network, comparing syntactic word networks of two texts, comparing the properties of a syntactic word network and a random graph.

The application was created as part of the diploma thesis: Analysis and creation of language graph of the people before and after aphasia, Comenius University, 2021. All source code files are well commented in English, but application is in Slovak language.

--------------------------------------------------------------------------------------------------------------

Analýza slovných sietí pomocou grafových štatistík

Aplikácia slúži na analýzu slovných sietí vytvorených z textu. Po načítaní textu (alebo priamo siete) dokáže aplikácia analyzovať túto sieť rôznymi grafovými a grafletovými metódami. Výsledky možno uložiť alebo porovnať priamo v aplikácii vďaka jednoduchému grafickému rozhraniu, a to nielen číselne, ale aj graficky.

Aplikácia je prioritne určená pre operačný systém Windows. Knižnice, pomocou ktorých aplikácia beží sú:
- matplotlib 3.1.0
- networkx 2.4
- tkinter 8.6

Okrem toho využíva vlastnú implementáciu pseudokódu PGD algoritmu a implementáciu ORCA algoritmu. Oba algoritmy sú voľne dostupné a popísané tu:
- PGD : http://nesreenahmed.com/publications/ahmed-et-al-icdm2015.pdf
- ORCA : tinyurl.com/3hcnj27n

Grafové štatistiky, ktoré aplikácia dokáže vypočítať:
- počet uzlov
- počet hrán
- maximálny stupeň uzla
- minimálny stupeň uzla
- priemerný stupeň uzla
- priemerný klasterizačný koeficient
- hustota grafu
- priemerná najkratšia vzdialenosť grafu
- priemer grafu

Grafletové štatistiky, ktorá aplikácia dokáža vypočítať:
- počet súvislých grafletov veľkosti 2-5
- počet nesúvislých grafletov veľkosti 2-4
- RGFD analýza
- GDDA analýza

Okrem toho možno vypočítať rôzne distribúcie a štatistiky vrcholov. Využitie: zisťovanie bezškálovosti siete, porovnávanie syntaktických slovných sietí dvoch textov, porovnávanie vlastností syntaktickej slovnej siete a náhodného grafu.

Aplikácia bola vytvorená ako súčasť diplomovej práce: Analýza a tvorba jazykových grafov ľudí pred a po afázii na báze angličtiny, Univerzita Komenského, 2021. Všetky zdrojové súbory sú dobre okomentované v angličtine, ale aplikácia je v slovenskom jazyku.


