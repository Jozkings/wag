import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from informations import *
from graph import Graph
import threading
import time
from plot import Plot
import sys
import os
import networkx as nx


class GraphicalUserInterface(object):
    """object for creating gui for easy manipulation with application"""
    VERSION_NUMBER = 1.0

    def __init__(self):
        """Init function"""
        self.main_window = self.create_window("Analýza textov pomocou grafov a grafletov", "800x700")
        self.menu_bar = tk.Menu(self.main_window)
        self.main_window.config(menu=self.menu_bar)
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.style = ttk.Style()
        self.style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        self.style.map('TCombobox', selectforeground=[('readonly', 'white')])
        self.graphlets_max_size = 4
        self.initialize_menu()
        self.initialize_main_widgets()
        self.initialize_graphs_info()
        self.main_window.mainloop()

    def initialize_menu(self):
        """Initialize top navigation bar"""
        program_menu = tk.Menu(self.menu_bar, tearoff=0)
        program_menu.add_command(label="Uložiť výsledky", command=lambda: self.save(False))
        program_menu.add_command(label="Uložiť výsledky ako ...", command=lambda: self.save(True))
        self.menu_bar.add_cascade(label="Program", menu=program_menu)
        stats_menu = tk.Menu(self.menu_bar, tearoff=0)
        stats_menu.add_command(label="Grafové štatistiky", command=lambda: self.graph_stats_info())
        stats_menu.add_command(label="Grafletové štatistiky", command=lambda: self.graphlets_stats_info())
        stats_menu.add_command(label="RGFD, GDDA", command=lambda: self.graphlets_comparision_info())
        stats_menu.add_command(label="Distribúcie", command=lambda: self.distributions_info())
        self.menu_bar.add_cascade(label="Štatistiky", menu=stats_menu)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="O programe...", command=lambda: self.about())
        help_menu.add_command(label="O grafoch a slovných sieťach", command=lambda: self.about_graphs())
        help_menu.add_command(label="O grafletoch", command=lambda: self.about_graphlets())
        self.menu_bar.add_cascade(label="Pomoc", menu=help_menu)

    def save(self, save_as):
        """Saves computed results to text file"""
        """:param save_as: boolean paramater for option save as (not just save)"""
        if save_as or self.file_name is None:
            file = filedialog.asksaveasfile(
                mode='w', defaultextension=".txt", filetypes=(("Textové súbory", "*.txt"), ("Všetky súbory", "*.*")))
            if file is None:
                return
            self.file_name = file.name
        with open(self.file_name, 'w') as file:
            for i, graph in enumerate([self.first_graph, self.second_graph]):
                file.write(f'Výsledky siete {(i+1)}:\n\nZákladné štatistiky:\n')
                for index, result in enumerate(graph.basic_results):
                    to_write = f'{LABELS[index]} '
                    to_write += "-" if result == -3 else str(result)
                    file.write(f'{to_write}\n')
                used = len(self.first_graph.basic_results)
                file.write('Grafletové štatistiky:\n')
                for index, result in enumerate(graph.graphlets_sum_counts):
                    to_write = f'{LABELS[index + used]} '
                    to_write += "-" if result == -3 else str(result)
                    file.write(f'{to_write}\n')
                    if to_write[-1] != "-" and index != len(graph.graphlets_sum_counts)-1:
                        to_write = f'{LABELS[index+used][:6] + "ne" + LABELS[index+used][6:]} '
                        if index == 0:
                            to_write += str(graph.motifs_counts[0])
                        elif index == 1:
                            to_write += str(sum(graph.motifs_counts[4:6]))
                        else:
                            to_write += str(sum(graph.motifs_counts[12:]))
                        file.write(f'{to_write}\n')
                file.write("-------------------\n\n")
            if graph.comparision_results[0] != -3:
                file.write('Porovnanie sietí:\n\n')
                file.write(f'{LABELS[13]} {graph.comparision_results[0]}\n')
                file.write(f'{LABELS[14]} {graph.comparision_results[1]}\n')

    def about(self):
        """Initialize 'about' part available from top navigation bar"""
        new_window = self.create_window("O programe...", "200x130", 'white')
        #last_modified = datetime.datetime.fromtimestamp(pathlib.Path("gui.py").stat().st_mtime) #doesnt work in .exe
        label = self.create_label(new_window,
                                  #f"Diplomová práca\n"
                                  f"Autor: Jozef Kubík\nVerzia: "
                                  f"{self.VERSION_NUMBER}\nNaposledy upravené: 27.04.2021",
                                  pady=(30, 5), col='white')

    def about_graphlets(self):
        """Initialize 'about graphlets' part available from top navigation bar"""
        new_window, new_frame, new_canvas = self.create_scrollable_window("O grafletoch", "700x400", top_level=True, color='white')
        text = GRAPHLETS_INFO
        label = self.create_label(new_frame, text, pady=(30, 5), an='w', col='white')
        self.graphlets_img = tk.PhotoImage(file="images/help_graphlets.png") #must be self
        image_label = self.create_label(new_frame, "", img=self.graphlets_img, col='white')

        text2 = GRAPHLETS_INFO2
        label2 = self.create_label(new_frame, text2, pady=(30, 5), an='w', col='white')
        self.graphlets_img2 = tk.PhotoImage(file="images/orbits.png") #must be self
        self.graphlets_img2 = self.graphlets_img2.zoom(5, 1)
        self.graphlets_img2 = self.graphlets_img2.subsample(6, 1)
        image_label2 = self.create_label(new_frame, "", padx= (30, 0), img=self.graphlets_img2, col='white')

        new_window.bind_all("<MouseWheel>", lambda event, arg=new_canvas: self.on_mousewheel(event, arg))

    def about_graphs(self):
        """Initialize 'about graphs' part available from top navigation bar"""
        new_window = self.create_top_level("O grafoch a slovných sieťach", "600x400")
        text = GRAPHS_INFO
        label = self.create_label(new_window, text, pady=(30, 5), an='w', col='white')

    def graphlets_stats_info(self):
        """Initialize 'graphlets stats info' part available from top navigation bar"""
        new_window = self.create_window("Grafletové štatistiky", "500x150", 'white')
        text = GRAPHLETS_STATS_INFO
        label = self.create_label(new_window, text, pady=(30, 5), an='w', col='white')

    def graph_stats_info(self):
        """Initialize 'graphs stats info' part available from top navigation bar"""
        new_window, new_frame, new_canvas = self.create_scrollable_window(
            "Grafové štatistiky", "670x400", top_level=True, color='white')
        text = GRAPHS_STATS_INFO
        label = self.create_label(new_frame, text, pady=(30, 5), an='w', col='white')

        self.graphs_img = tk.PhotoImage(file="images/other_graphs_stats.PNG") #must be self
        image_label = self.create_label(new_frame, "", img=self.graphs_img, col='white')

        self.graphs_img2 = tk.PhotoImage(file="images/density.PNG") #must be self
        image_label2 = self.create_label(new_frame, "", img=self.graphs_img2, col='white')

        self.graphs_img3 = tk.PhotoImage(file="images/clustering_coefficient.PNG") #must be self
        image_label3 = self.create_label(new_frame, "", img=self.graphs_img3, col='white')

        self.graphs_img4 = tk.PhotoImage(file="images/shortest_path_length.PNG") #must be self
        image_label4 = self.create_label(new_frame, "", img=self.graphs_img4, col='white')

        new_window.bind_all("<MouseWheel>", lambda event, arg=new_canvas: self.on_mousewheel(event, arg))

    def graphlets_comparision_info(self):
        """Initialize 'graphlets comparision info' part available from top navigation bar"""
        new_window, new_frame, new_canvas = self.create_scrollable_window(
            "Pokročilé grafletové štatistiky", "660x400", top_level=True, color='white')
        text1 = GRAPHLETS_COMPARISION_INFO

        label = self.create_label(new_frame, text1, pady=(30, 5), an='w', col='white')
        self.graphlets_img3 = tk.PhotoImage(file="images/rgfd_equations.png") #must be self
        self.graphlets_img3 = self.graphlets_img3.subsample(2, 2)
        image_label = self.create_label(new_frame, "", img=self.graphlets_img3, col='white')

        text2 = GRAPHLETS_COMPARISION_INFO2
        label2 = self.create_label(new_frame, text2, pady=(30, 5), an='w', col='white')
        self.graphlets_img4 = tk.PhotoImage(file="images/gdda_equations.png") #must be self
        image_label = self.create_label(new_frame, "", img=self.graphlets_img4, col='white')

        new_window.bind_all("<MouseWheel>", lambda event, arg=new_canvas: self.on_mousewheel(event, arg))

    def distributions_info(self):
        """Initialize 'distribution info' part available from top navigation bar"""
        new_window = self.create_window("Distribúcie", "600x200", 'white')
        text = DISTRIBUTIONS_INFO
        label = self.create_label(new_window, text, pady=(30, 5), an='w', col='white')

    def on_close(self):
        """Removes all created help files and closes application"""
        for graph in [self.first_graph, self.second_graph]:
            if graph is not None:
                if graph.file_name is not None:
                    if os.path.isfile(graph.file_name):
                        os.remove(graph.file_name)
                    if os.path.isfile(graph.file_name[:-4] + "_orca.txt"):
                        os.remove(graph.file_name[:-4] + "_orca.txt")
        sys.exit()

    def initialize_graphs_info(self):
        """Initialize graphs and variable for name of the file for results saving"""
        self.first_graph = Graph(None)
        self.second_graph = Graph(None)
        self.file_name = None

    def initialize_notebook(self):
        """Initializes main application window as notebook widget"""
        self.notebook = ttk.Notebook(self.main_window, name="notebook")

    def add_notebook_card(self, name, text, state="normal"):
        """Adds card to notebook, sets its background color, text and shows it"""
        frame = tk.Frame(self.notebook, name=name)
        #frame.configure(bg='white')
        self.notebook.add(frame, text=text, state=state)
        self.notebook.pack(expand=1, fill='both')
        return frame

    def initialize_first_tab(self):
        """Initializes all widgets for first card"""
        first_frame = self.add_notebook_card("inputTab", "Načítanie dát")
        title_label = self.create_label(first_frame, "Načítanie textov", pady=(20,20), size=15)
        file_label = self.create_label(first_frame, "Načitať súbor obsahujúci text", pady=(30, 5))
        add_file_button = self.create_button(first_frame, "Vyber súbor...",
                                                  lambda: self.add_file_click(True),
                                                  name="addButton")
        edge_label = self.create_label(first_frame, "Načítať súbor obsahujúci zoznám hrán", pady=(30, 5))
        add_edge_list_button = self.create_button(first_frame, "Vyber súbor...",
                                              lambda: self.add_file_click(False),
                                              name="edgeButton")
        entry_label = self.create_label(first_frame, "Vložiť priamo text", pady=(30, 5))
        entry_widget = self.create_entry(first_frame, "entryWidget", 5, 50)
        add_entry_button = self.create_button(first_frame, "Načítať vložený text",
                                                   lambda: self.add_entry_click(),
                                                   name="entryButton")
        status_label = self.create_label(first_frame, "", pady=(30, 5), name="loadStatusLabel")
        random_button = self.create_button(first_frame, "Načítať ako druhú sieť náhodný graf",
                                             lambda: self.load_second_random(),
                                             name="randomButton")
        self.disable_name_widget(".notebook.inputTab.randomButton")

    def initialize_second_tab(self):
        """Initializes all widgets for second card"""
        second_frame = self.add_notebook_card("graph1Tab", 'Graf 1 - analýza', "disabled")
        title_label = self.create_label(second_frame, "Analýza prvého textu", pady=(20, 20), size=15)
        basic_analysis_button = self.create_button(second_frame, "Spustiť základnú analýzu",
                            lambda: self.basic_analyze_bar(
                                True, first_bar, ".notebook.graph1Tab.firstBasicButton", first_label),
                            name="firstBasicButton")
        first_bar = self.create_progressbar(second_frame)
        first_label = self.create_label(second_frame, "")
        file_label = self.create_label(second_frame, "Zvoľ maximálnu veľkosť grafletov:")

        self.option1 = tk.StringVar(value="4")
        self.option1.trace('w', self.set_graphlets_size)
        graphlet_analysis_radio1 = self.create_radio(second_frame, "4", "4", self.option1, "radioButton1", 'center')
        graphlet_analysis_radio2 = self.create_radio(second_frame, "5", "5", self.option1, "radioButton2", 'center')
        graphlet_analysis_button = self.create_button(second_frame, "Spustiť grafletovú analýzu",
                            lambda: self.graphlet_analyze_bar(
                                True, second_bar, ".notebook.graph1Tab.firstGraphletButton", second_label),
                            name="firstGraphletButton")
        second_bar = self.create_progressbar(second_frame)
        second_label = self.create_label(second_frame, "")

    def initialize_third_tab(self):
        """Initializes all widgets for third card"""
        third_frame = self.add_notebook_card("graph2Tab", 'Graf 2 - analýza', "disabled")
        title_label = self.create_label(third_frame, "Analýza druhého textu", pady=(20, 20), size=15)
        basic_analysis_button = self.create_button(third_frame, "Spustiť základnú analýzu",
                                    lambda: self.basic_analyze_bar(
                                        False, first_bar, ".notebook.graph2Tab.secondBasicButton", first_label),
                                    name="secondBasicButton")
        first_bar = self.create_progressbar(third_frame)
        first_label = self.create_label(third_frame, "")
        file_label = self.create_label(
            third_frame, f"Maximálna veľkosť grafletov bude rovnaká ako v prvom grafe ({self.graphlets_max_size})",
            name="sizeLabel")
        graphlet_analysis_button = self.create_button(third_frame, "Spustiť grafletovú analýzu",
                                    lambda: self.graphlet_analyze_bar(
                                        False, second_bar, ".notebook.graph2Tab.secondGraphletButton", second_label),
                                    name="secondGraphletButton")
        second_bar = self.create_progressbar(third_frame)
        second_label = self.create_label(third_frame, "")

    def initialize_fourth_tab(self):
        """Initializes all widgets for fourth card"""
        fourth_frame = self.add_notebook_card("compareTab", 'Porovnanie grafov', "disabled")
        title_label = self.create_label(fourth_frame, "Grafletové porovnávacie štatistiky", pady=(20, 20), size=15)
        rg_label = self.create_label(
            fourth_frame, "Relative graphlet frequency distance\nGraphlet degree distribution agreement",pady=(50, 10))
        bar = self.create_progressbar(fourth_frame)
        add_file_button = self.create_button(fourth_frame, "Spustiť RGFD a GDDA analýzu",
                                    lambda: self.graphlets_comparision_bar(bar, ".notebook.compareTab.rgButton", label),
                                    name="rgButton")
        add_file_button['state'] = 'disabled'
        label = self.create_label(fourth_frame, "")

    def initialize_fifth_tab(self):
        """Initializes all widgets for fifth card"""
        fifth_frame = self.add_notebook_card("resultsTab", 'Výsledky', "disabled")
        for r in range((len(LABELS)*2)+1):
            for c in range(3):
                if r == 0:
                    if c == 1:
                        first_label = tk.Label(fifth_frame, text="Graf 1", width=50)
                        first_label.grid(row=r, column=c, sticky=tk.NSEW)
                    elif c == 2:
                        second_label = tk.Label(fifth_frame, text="Graf 2")
                        second_label.grid(row=r, column=c, sticky=tk.NSEW)
                    else:
                        zero_label = tk.Label(fifth_frame, text="Štatistika")
                        zero_label.grid(row=r, column=c, sticky=tk.NSEW)
                else:
                    if c == 0 and r > 0 and r % 2 == 0:
                        label = tk.Label(fifth_frame, text=LABELS[(r//2)-1], anchor='w', name=f"resultsLabel{r}")
                        label.grid(row=r, column=c, sticky=tk.NSEW)
                    else:
                        label = tk.Label(fifth_frame, text="", name=f"resultsLabel{r} {c}")
                        label.grid(row=r, column=c, sticky=tk.NSEW)

    def initialize_sixth_tab(self):
        """Initializes all widgets for sixth card"""
        sixth_frame = self.add_notebook_card("otherTab", 'Iné', "disabled")
        title_label = self.create_label(
            sixth_frame, "Jednotlivé štatistiky a štatistiky konkrétnych uzlov", pady=(20, 20), size=15)
        length = max(LABELS.values(), key=len)
        length = len(max(length, max(SINGLE_STATS.values(), key=len))) - 10
        rg_label1 = self.create_label(sixth_frame, "Vypočítať jednotlivé štatistiky grafu 1", pady=(5, 5))
        self.stats_combo_res1 = tk.StringVar()
        stats_combo1 = self.create_combo(sixth_frame, self.stats_combo_res1, length,
                                          tuple([LABELS[index][:-1] for index in range(9)])
                                          + tuple(GRAPHLETS_STATS.values()), pady=(5, 5))
        start1_button = self.create_button(sixth_frame, "Spustiť analýzu",
                                    lambda: self.count_stat_init(
                                        True, stats_combo1.current(), label1, ".notebook.otherTab.other1Button"),
                                    name="other1Button")
        label1 = self.create_label(sixth_frame, "", pady=(5, 0))


        vg_label1 = self.create_label(sixth_frame, "Vypočítať štatistiky pre konkrétny vrchol grafu 1", pady=(5, 5))
        self.vstats_combo_res1 = tk.StringVar()
        vstats_combo1 = self.create_combo(sixth_frame, self.vstats_combo_res1, length,
                                          tuple(SINGLE_STATS.values()), pady=(5, 5))
        vstart1_button = self.create_button(sixth_frame, "Spustiť analýzu",
                                    lambda: self.single_stat_init(
                                        True, vstats_combo1.current(), vlabel1, ".notebook.otherTab.vertex1Button"),
                                    name="vertex1Button")
        vlabel1 = self.create_label(sixth_frame, "", pady=(5, 0))

        rg_label2 = self.create_label(sixth_frame, "Vypočítať jednotlivé štatistiky grafu 2", pady=(5, 5))
        self.stats_combo_res2 = tk.StringVar()
        stats_combo2 = self.create_combo(sixth_frame, self.stats_combo_res2, length,
                                          tuple([LABELS[index][:-1] for index in range(9)])
                                          + tuple(GRAPHLETS_STATS.values()), (5, 5))
        start2_button = self.create_button(sixth_frame, "Spustiť analýzu",
                                    lambda: self.count_stat_init(
                                        False, stats_combo2.current(), label2, ".notebook.otherTab.other2Button"),
                                    name="other2Button")
        start2_button['state'] = 'disabled'
        label2 = self.create_label(sixth_frame, "",  pady=(5, 0))
        vg_label2 = self.create_label(sixth_frame, "Vypočítať štatistiky pre konkrétny vrchol grafu 2", pady=(5, 5))

        vlabel2 = self.create_label(sixth_frame, "", pady=(5, 0), side=tk.LEFT, an='s')
        self.vstats_combo_res2 = tk.StringVar()
        vstats_combo2 = self.create_combo(sixth_frame, self.vstats_combo_res2, length,
                                          tuple(SINGLE_STATS.values()), (5, 5))
        vstart2_button = self.create_button(sixth_frame, "Spustiť analýzu",
                                    lambda: self.single_stat_init(
                                        False, vstats_combo2.current(), vlabel2, ".notebook.otherTab.vertex2Button"),
                                    name="vertex2Button")
        vstart2_button['state'] = 'disabled'
        vlabel2 = self.create_label(sixth_frame, "", pady=(5, 0))

    def initialize_seventh_tab(self):
        """Initializes all widgets for seventh card"""
        seventh_frame = self.add_notebook_card("visualizationTab", 'Vizualizácia', "disabled")
        title_label = self.create_label(seventh_frame, "Vizualizovanie výsledkov sietí", pady=(20, 20), size=15)
        self.figure = Plot(seventh_frame)
        canvas = self.figure.get_canvas()
        widget = canvas.get_tk_widget()
        widget.pack(pady=(20, 0))
        length = len(max(DISTRIBUTIONS.values(), key=len)) - 10

        var1, var2, var3 = tk.IntVar(), tk.IntVar(), tk.IntVar()
        self.draw_combo_res1, self.draw_combo_res2 = tk.StringVar(), tk.StringVar() #must be self
        draw_button = self.create_button(seventh_frame, "Vykresliť dáta",
                                    lambda: self.redraw(
                                        stats_combo1.current(), stats_combo2.current(), var1.get(), var2.get()),
                                    name="draw1Button", pady=10)
        log_checkbox = tk.Checkbutton(
            master=seventh_frame, text="Logaritmická škála", variable=var3, command=lambda: self.log_status(var3))
        log_checkbox.pack()

        label1 = self.create_label(seventh_frame, "Graf 1:", side=tk.LEFT, an='s')
        stats_combo1 = self.create_combo(seventh_frame, self.draw_combo_res1, length,
                                          ("", "Sieť",) + tuple([val[:-1] for val in LABELS.values()]) +
                                         tuple(DISTRIBUTIONS.values()), pady=(5, 5), side=tk.LEFT, anchor='s')
        scatter_checkbox1 = tk.Checkbutton(master=seventh_frame, text="scatter", variable=var1)
        scatter_checkbox1.pack(side=tk.LEFT, padx=(0, 20), anchor='s')
        label2 = self.create_label(seventh_frame, "Graf 2:", side=tk.LEFT, an='s')
        stats_combo2 = self.create_combo(seventh_frame, self.draw_combo_res2, length,
                                          ("", "Sieť",) + tuple([val[:-1] for val in LABELS.values()]) +
                                         tuple(DISTRIBUTIONS.values()), pady=(10, 10), side=tk.LEFT, anchor='s')
        scatter_checkbox2 = tk.Checkbutton(master=seventh_frame, text="scatter", variable=var2)
        scatter_checkbox2.pack(side=tk.LEFT, anchor='s')

    def initialize_main_widgets(self):
        """Calls notebook and cards initialization"""
        self.initialize_notebook()
        self.initialize_first_tab()
        self.initialize_second_tab()
        self.initialize_third_tab()
        self.initialize_fourth_tab()
        self.initialize_fifth_tab()
        self.initialize_sixth_tab()
        self.initialize_seventh_tab()

    def count_stat_init(self, is_first, statistic, label, button_name):
        """Initializes statistic counting thread"""
        """:param is_first: whether it's statistic from first graph (or second), :param statistic: statistic index,
           :param label: label for showing current proces :param button_name: name of button which state will be
            normalized (this function disables it when counting is in progress)"""
        self.disable_name_widget(button_name)
        self.handle_thread(self.count_stat, (is_first, statistic, label, button_name))

    def count_stat(self, is_first, statistic, label, button_name):
        """Calls graph functions for counting statistics and functions for label updating"""
        """:param is_first: whether it's statistic from first graph (or second), :param statistic: statistic index,
           :param label: label for showing current proces :param button_name: name of button which state will be
            normalized (it's blocked when counting is in progress)"""
        graph = self.first_graph if is_first else self.second_graph
        label['text'] = 'Počítam...'
        if statistic < 9 and graph.basic_results[statistic] != -3:
            label['text'] = 'Hotovo!'
            self.normalize_name_widget(button_name)
            self.update_single_label(graph, graph.basic_results[statistic], statistic)
            return
        if statistic < 9:
            stato = [graph.get_order, graph.get_size, graph.get_density, graph.get_maximal_degree,
                     graph.get_minimal_degree, graph.get_degree_average, graph.get_whole_clustering_coefficient,
                     graph.get_diameter, graph.get_average_path_length]
            result = stato[statistic]()[1] if 3 <= statistic <= 4 else stato[statistic]()
            self.update_single_label(graph, result, statistic)
        else:
            results = graph.motifs_counts
            if not results:
                messagebox.showerror('Error', 'Pred spustením tejto analýzy treba mať dokončenú grafletovú analýzu!')
                self.normalize_name_widget(button_name)
                label['text'] = ''
                return
            statistic -= 9
            if statistic == 0:
                result = results[:graph.AllGraphletsTypesSumCount.TWO]
            elif statistic == 1:
                result = results[graph.AllGraphletsTypesSumCount.TWO:graph.AllGraphletsTypesSumCount.THREE]
            else:
                result = results[graph.AllGraphletsTypesSumCount.THREE:]
            self.graphlets_counts_window(result, statistic, graph)
        label['text'] = 'Hotovo!'
        self.normalize_name_widget(button_name)

    def single_stat_init(self, is_first, statistic, label, button_name):
        """Creates window for taking input from user (for node, on which should some statistic be applied)"""
        """:param is_first: whether it's statistic from first graph (or second), :param statistic: statistic index,
           :param label: label for showing current proces :param button_name: name of button which state will be
            normalized (this function disables it when counting is in progress)"""
        self.disable_name_widget(button_name)
        new_window = self.create_window("Zadaj vrchol", "300x250")
        self.create_label(new_window, "Zadaj vrchol, pre ktorý chceš spustiť danú analýzu")
        entry_widget = self.create_entry(new_window, "nodeEntryWidget", 5, 50)
        button = self.create_button(
            new_window, "Potvrdiť vrchol",
            lambda: self.single_stat_init_node(is_first, statistic, label, button_name, entry_widget, new_window),
            name="nodeEntryButton", pady=10)

    def single_stat_init_node(self, is_first, statistic, label, button_name, entry_widget, window):
        """Initializes node statistic counting thread"""
        """:param is_first: whether it's statistic from first graph (or second), :param statistic: statistic index,
           :param label: label for showing current proces :param button_name: name of button which state will be
            normalized (it's blocked when counting is in progress), :param entry_widget: entry widget, from which
            will be node taken, :param window: window where entry is placed (should be destroyed)"""
        node = entry_widget.get("1.0", tk.END)
        window.destroy()
        self.handle_thread(self.single_stat, (is_first, statistic, label, button_name, node))

    def single_stat(self, is_first, statistic, label, button_name, node):
        """Calls graph functions for counting node statistics and functions for label updating"""
        """:param is_first: whether it's statistic from first graph (or second), :param statistic: statistic index,
           :param label: label for showing current proces :param button_name: name of button which state will be
            normalized (it's blocked when counting is in progress, :param node: node on which statistic is applied"""
        graph = self.first_graph if is_first else self.second_graph
        node = node.strip()
        if node not in graph.get_g().keys():
            if node.isdigit():
                node = int(node)
            if node not in graph.get_g().keys():
                messagebox.showerror('Error', 'Daný vrchol sa nenachádza v grafe!')
                self.normalize_name_widget(button_name)
                return
        label['text'] = 'Počítam...'
        stato = [graph.get_degree, graph.get_clustering_coefficient, graph.get_nodes()[node].get_count]
        result = stato[statistic](node) if statistic < 2 else stato[statistic]()
        label['text'] = 'Hotovo!'
        self.normalize_name_widget(button_name)
        label['text'] = f'Výsledok analýzy pre vrchol {node} je: {result}'

    def get_redraw_results(self, stat, graph, is_other):
        """Calls functions for getting statistics result for plotting (or network plotting)"""
        """:param stat: statistic index, :param graph: graph on which is statistic applied, 
           :param is_other: if statistic chosen for other graph is not network showing (just helpful paramater)"""
        result_x, result_y = None, None
        log = False
        if stat == 0:
            return result_x, result_y, log
        distributions = [graph.get_nodes_degree_distribution, graph.get_nodes_degree_distribution_normalized,
                         graph.get_shortest_path_length_distribution, graph.get_clustering_coefficient_distribution,
                         graph.get_clustering_to_degree_distribution]
        if stat == 1:
            if is_other:
                messagebox.showerror('Error',
                                     'Pre zobrazenie siete musí zostať výber štatistiky pre druhú sieť prázdny!')
                return result_x, result_y, log
            try:
                self.figure.show_graph(graph)
            except:
                messagebox.showerror('Error', 'Zobrazenie siete funguje len pre malý počet vrcholov (<=100)!')
            return result_x, result_y, log
        elif 2 <= stat <= 10:
            result_y = graph.basic_results[stat-2]
        elif 11 <= stat <= 14:
            result_y = graph.graphlets_sum_counts[stat-2-9]
        elif 15 <= stat <= 16:
            result_y = graph.comparision_results[stat-2-13]
        elif stat != 0:
            if stat == 17 or stat == 20:
                result = distributions[stat-17]()
                result_y, result_x = list(result.keys()), list(result.values())
            else:
                result_y = distributions[stat-17]()
                result_x = [i+1 for i in range(len(result_y))]
            log = (stat == 18 or stat == 21)
        if result_y == tuple or result_y == -3:
            result_y = -3
            messagebox.showerror('Error', 'Daná štatistika musí byť najskôr vypočítaná!')
            return result_x, result_y, log
        if result_y is None and stat > 1:
            messagebox.showerror('Error',
                                 'Daná štatistika alebo časť distribúcie ešte nebola analyzovaná pre daný graf!')
        return result_x, result_y, log

    def redraw(self, stat1, stat2, scatter1, scatter2):
        """Calls function for getting results for drawing and function for drawing them"""
        """:param stat1: first graph statistic index, :param stat2: second graph statistic index,
           :param scatter1: if first plot should be scattered,
           :param scatter2: if second plot should be scattered"""
        result_x1, result_y1, log1 = self.get_redraw_results(stat1, self.first_graph, stat2 > 0)
        result_x2, result_y2, log2 = self.get_redraw_results(stat2, self.second_graph, stat1 > 0)
        if 2 <= stat1 <= 16:  #one point graphs must be scatter-like
            scatter1 = True
        if 2 <= stat2 <= 16:
            scatter2 = True
        if (stat1 != 0 or stat2 != 0) and (stat1 != 1 and stat2 != 1):
            self.figure.update(result_x1, result_y1, result_x2, result_y2, scatter1, scatter2, log1 and log2)

    def graphlets_counts_window(self, result, statistic, graph):
        """Creates window for showing specific graphlets types counts, and shows them"""
        """:param: result: resulting values, :param statistic: chosen statistic,
           :param graph: form which graph are graphlets counted"""
        window = self.create_window(f"Všetky graflety veľkosti {(statistic+2)}", "200x300")
        text = f"Graflety veľkosti {(statistic+2)}:"
        name_label = self.create_label(window, text)
        result_label = self.create_label(window, "", an='w')
        if statistic == 0:
            types = GRAPHLETS_TYPES[:graph.AllGraphletsTypesSumCount.TWO]
        elif statistic == 1:
            types = GRAPHLETS_TYPES[graph.AllGraphletsTypesSumCount.TWO:graph.AllGraphletsTypesSumCount.THREE]
        else:
            types = GRAPHLETS_TYPES[graph.AllGraphletsTypesSumCount.THREE:]
        for index, res in enumerate(result):
            result_label['text'] += f"\n{types[index]}: {result[index]}"
        window.mainloop()

    def set_graphlets_size(self, *args):
        """Sets maximum graphlet size (4 or 5)"""
        """:param *args: arguments"""
        self.graphlets_max_size = self.option1.get()
        label = self.main_window.nametowidget(".notebook.graph2Tab.sizeLabel")
        new_value = label['text'][:-2] + f"{self.graphlets_max_size})"
        label['text'] = new_value

    def log_status(self, status):
        """Sets status of function for scaling axis in plot"""
        """:param status: checkbutton widget"""
        if status.get() == 1:
            self.figure.set_scale_variables("log", "log")
        else:
            self.figure.set_scale_variables("linear", "linear")

    def load_second_random(self):
        """Loads random graph instead of second text. Graph has same number of vertices and nodes as first one.
            It's usually created from bigger graph and deleting it's isolated vertices"""
        N = self.first_graph.get_order()
        m = self.first_graph.get_size()
        random_graph = nx.gnm_random_graph(N, m, directed=False)
        new_n = N
        tries = 0
        statement = True
        while statement:  #we need connected graph (statistics won't be exact due to this)
            random_graph = nx.gnm_random_graph(new_n, m, directed=False)
            tries += 1
            if new_n - len(list(nx.isolates(random_graph))) == N:
                random_graph.remove_nodes_from(list(nx.isolates(random_graph)))
                statement = False
            elif tries == 5:
                tries = 0
                new_n += 1
        file_name = 'interfiles\\quick_random_help.txt'
        vertices_dict = {val:index for index, val in enumerate(list(random_graph.nodes))}
        with open(file_name, 'w') as file:
            file.write(f"{N} {m}\n")
            for value in list(random_graph.edges()):
                v1, v2 = vertices_dict[value[0]], vertices_dict[value[1]]
                file.write(f"{v1} {v2}\n")
        self.initialize_graph(("edges", file_name))

    def initialize_graph(self, entry):
        """Calls function to initialize word network as graph and changes status of widgets depending on loaded graph"""
        """:param entry: pair (type, data), where type denotes method of loading text/graph and data actual data"""
        type, data = entry
        adding = 'pri takomto veľkom texte' if type != 'edges' else 'pre takúto veľkú sieť'
        infotext = f'Prvý výpočet niektorých štatistík či distribúcií môže {adding} trvať dlhšie.'
        if not self.first_graph.initialized:
            if type == "text":
                self.first_graph.add_connections(data)
            else:
                try:
                    self.first_graph.load_text(data) \
                        if type == "is_text" else self.first_graph.load_graph_edge_list(data)
                except:
                    messagebox.showerror('Error', 'Súbor nebol vložený v správnom formáte!')
                    return
            self.normalize_multiple_notebook_tabs([".notebook.graph1Tab", ".notebook.resultsTab", ".notebook.otherTab",
                                                  ".notebook.visualizationTab"])
            self.main_window.nametowidget(".notebook.inputTab.loadStatusLabel")['text'] = "Graf 1 úspešne načítaný!"
            self.normalize_name_widget(".notebook.inputTab.randomButton")
            if self.first_graph.get_size() >= 4000: #pretty much dummy constant:
                messagebox.showinfo('Upozornenie', infotext)
        elif not self.second_graph.initialized:
            if type == "text":
                self.second_graph.add_connections(data)
            else:
                try:
                    self.second_graph.load_text(data) \
                        if type == "is_text" else self.second_graph.load_graph_edge_list(data)
                except:
                    messagebox.showerror('Error', 'Súbor nebol vložený v správnom formáte!')
                    return
            self.normalize_multiple_notebook_tabs(
                [".notebook.graph2Tab", ".notebook.compareTab", ".notebook.resultsTab"])
            self.change_multiple_name_widgets_states({".notebook.inputTab.addButton" : "disabled",
                                                      ".notebook.inputTab.edgeButton": "disabled",
                                                    ".notebook.inputTab.entryButton": "disabled",
                                                    ".notebook.otherTab.other2Button": "normal",
                                                      ".notebook.otherTab.vertex2Button": "normal",
                                                      ".notebook.inputTab.randomButton" : "disabled"})
            self.main_window.nametowidget(".notebook.inputTab.loadStatusLabel")['text'] = "Graf 2 úspešne načítaný!"
            if self.second_graph.get_size() >= 4000:
                messagebox.showinfo('Upozornenie', infotext)

    def add_file_click(self, is_text):
        """Allows user to load file into application"""
        """:param is_text: if loaded file contains text or edge list (depending which button user clicked)"""
        file = filedialog.askopenfilename(filetypes=(("Textové súbory", "*.txt"), ("Všetky súbory", "*.*")))
        if not file:
            return
        type = "is_text" if is_text else "edges"
        self.initialize_graph((type, file))

    def add_entry_click(self):
        """Loads text from entry after button click"""
        entry = self.main_window.nametowidget(".notebook.inputTab.entryWidget")
        text = entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror('Error', 'Nebol vložený žiaden text!')
            return
        self.initialize_graph(("text", text))

    def basic_analyze_bar(self, is_first_graph, bar, after, label):
        """Initialize thread for showing and updating bar representing progress in calculating graphs stats"""
        """:param is_first_graph: if statistic is calculated from first graph, :param bar: bar object, 
           :param after: button to be disabled after starting, :param label: label for text showing current operation"""
        bar.pack(after=after, pady=10)
        self.disable_name_widget(after)
        self.handle_thread(self.basic_analyze, (is_first_graph, bar, label,))

    def graphlet_analyze_bar(self, is_first_graph, bar, after, label):
        """Initialize thread for showing and updating bar representing progress in calculating graphlets stats"""
        """:param is_first_graph: if statistic is calculated from first graph, :param bar: bar object, 
           :param after: button to be disabled after starting, :param label: label for text showing current operation"""
        bar.pack(after=after)
        self.disable_name_widget(after)
        self.disable_name_widget(".notebook.graph1Tab.radioButton1")
        self.disable_name_widget(".notebook.graph1Tab.radioButton2")
        self.handle_thread(self.graphlet_analyze, (is_first_graph, bar, label,))

    def graphlets_comparision_bar(self, bar, after, label):
        """Initialize thread for showing and updating bar representing progress in calculating comparision stats"""
        """:param bar: bar object, :param after: button to be disabled after starting, 
           :param label: label for text showing current operation"""
        bar.pack(after=after, pady=10)
        self.disable_name_widget(after)
        self.handle_thread(self.graphlets_comparision, (bar, label,))

    def graphlets_comparision(self, bar, label):
        """Initialize thread which gets comparision results and update labels with calculated results"""
        """:param bar: bar widget, :param label: label widget for showing current operation"""
        self.handle_thread(self.first_graph.get_gdda_rgfd, (self.second_graph, bar, label, self.move_bar,), bar)
        r_label1 = self.main_window.nametowidget(f".notebook.resultsTab.resultsLabel28 1")
        g_label1 = self.main_window.nametowidget(f".notebook.resultsTab.resultsLabel30 1")
        r_label1['text'] += f"{self.first_graph.comparision_results[0]}"
        g_label1['text'] += f"{self.first_graph.comparision_results[1]}"
        r_label2 = self.main_window.nametowidget(f".notebook.resultsTab.resultsLabel28 2")
        g_label2 = self.main_window.nametowidget(f".notebook.resultsTab.resultsLabel30 2")
        r_label2['text'] += f"{self.first_graph.comparision_results[0]}"
        g_label2['text'] += f"{self.first_graph.comparision_results[1]}"

    def basic_analyze(self, is_first_graph, bar, label):
        """Initialize thread which gets graphs results and update labels with calculated results"""
        """:param is_first_graph: if statistic is calculated from first graph,:param bar: bar widget, 
           :param label: label widget for showing current operation"""
        if is_first_graph:
            func_graph = self.first_graph
        else:
            func_graph = self.second_graph
        self.handle_thread(func_graph.basic_analysis, (bar, label, self.move_bar,), bar)
        self.update_labels(func_graph, True)

    def graphlet_analyze(self, is_first_graph, bar, label):
        """Initialize thread which gets graphlets results and update labels with calculated results"""
        """:param is_first_graph: if statistic is calculated from first graph,:param bar: bar widget, 
           :param label: label widget for showing current operation"""
        if is_first_graph:
            func_graph = self.first_graph
        else:
            func_graph = self.second_graph
        self.handle_thread(func_graph.graphlet_analysis, (bar, label, self.graphlets_max_size, self.move_bar,), bar)
        self.update_labels(func_graph, False)

    def move_bar(self, bar, maxo, label, textholder):
        """Move progress in progress bar and set new text to label showing current operation"""
        """:param bar: bar widget, :param maxo: value to be added, 
           :param label: label widget for showing current operation, :param textholder: current operation key as text"""
        for i in range(maxo):
            bar['value'] += 1
        time.sleep(0.2)
        label['text'] = OPERATIONS[textholder]

    def handle_thread(self, target, args, bar=None):
        """Creates and handles thread for some task, also sets bar correctly after thread finishing"""
        """:param target: target function for thread, :param args: arguments for function for thread,
           :param bar: bar widget"""
        thread = threading.Thread(target=target, args=args)
        thread.start()
        if bar is not None:
            thread.join()
            bar.stop()
            bar['value'] = 100

    def update_single_label(self, graph, result, index):
        """Updates text in single label"""
        """:param graph: graph object, :param result: result to be showed, :param index: index of label"""
        label = self.main_window.nametowidget(
            f".notebook.resultsTab.resultsLabel{(index+1)*2} {(2 - (graph == self.first_graph))}")
        label['text'] = f"{result}"

    def update_labels(self, graph, is_basic):
        """Updates text in multiple labels"""
        """:param graph: graph object, :param is_basic: if results are from graph analysis"""
        if is_basic:
            for i in range(9):
                label = self.main_window.nametowidget(
                    f".notebook.resultsTab.resultsLabel{(i+1)*2} {(2 - (graph == self.first_graph))}")
                result = "-" if graph.basic_results[i] == -3 else graph.basic_results[i]
                label['text'] = f"{result}"
        else:
            if self.first_graph.graphlets_counts and self.second_graph.graphlets_counts:
                self.normalize_name_widget(".notebook.compareTab.rgButton")
            for i in range(9, 13):
                label = self.main_window.nametowidget(
                    f".notebook.resultsTab.resultsLabel{(i+1)*2} {(2 - (graph == self.first_graph))}")
                index = i - 9
                if i < 12:
                    label['text'] = f"{graph.graphlets_sum_counts[index]}"
                elif i == 12 and int(self.graphlets_max_size) == 5:
                    label['text'] = f"{graph.graphlets_sum_counts[3]}"

    def on_mousewheel(self, event, window):
        window.yview_scroll(int(-1*(event.delta/120)), "units")


    """TKINTER PARAMETERS CHANGING--------------------------------------------------"""

    def disable_name_widget(self, widget_name):
        """Disables widget according to its name"""
        """:param name: name of the widget"""
        self.main_window.nametowidget(widget_name)['state'] = "disabled"

    def normalize_name_widget(self, widget_name):
        """Normalizes widget according to its name"""
        """:param name: name of the widget"""
        self.main_window.nametowidget(widget_name)['state'] = "normal"

    def normalize_notebook_tab(self, tab_name):
        """Normalizes notebook tab according to its name"""
        """:param name: name of the tab"""
        self.notebook.tab(tab_name, state="normal")

    def normalize_multiple_notebook_tabs(self, tabs_name):
        """Normalizes multiple notebook tabs according to their names"""
        """:param tabs_name: list of names of the tabs"""
        for name in tabs_name:
            self.notebook.tab(name, state="normal")

    def change_multiple_name_widgets_states(self, name_state_dict):
        """Changes states of multiple widgets"""
        """:param name_state_dict: dictionary, where key = widget name, value = new widget state"""
        for widget_name, new_state in name_state_dict.items():
            self.main_window.nametowidget(widget_name)['state'] = new_state

    """TKINTER WIDGETS and ASSETS CREATING--------------------------------------------------"""
    def create_progressbar(self, master):
        """Creates progressbar widget"""
        """:param master: master window/tab"""
        bar = ttk.Progressbar(master=master, length=200, mode='determinate', value=0, maximum=100)
        bar.pack()
        bar.pack_forget()
        return bar

    def create_label(self, master, txt, padx=None, pady=None, side=None, an=None, name="", size=10, img=None, col=None):
        """Creates label widget"""
        """:param master: master window/tab, :param text: text of the label :param padx: x-axis padding,
           :param pady: y-axis padding, :param side: side on which should label be placed, :param anchor: side where
            label should be anchored, :param name: name of the label, :param size: size of the label, 
            :param image: image if label should be used to display some image"""
        if name:
            label = tk.Label(master=master, text=txt, name=name, font=(None,size))
        elif img is not None:
            label = tk.Label(master=master, text=txt, image=img)
        elif side is None and an is not None:
            label = tk.Label(master=master, text=txt, anchor=an, justify='left')
        else:
            label = tk.Label(master=master, text=txt, font=(None,size))
        if col is not None:
            label.configure(bg=col)
        if side is not None:          #statements not bullet-proof but smartly represented for just needed
            label.pack(side=side, anchor=an)
        elif padx is not None:
            label.pack(padx=padx, pady=pady)
        elif pady is not None:
            label.pack(pady=pady)
        else:
            label.pack()
        return label

    def create_button(self, master, text, command, name="", pady=None):
        """Creates button widget"""
        """:param master: master window/tab, :param text: text of the label, :param command: button press command,
           :param name: name of the button, :param pady: y-axis padding"""
        button = tk.Button(master=master, text=text, name=name, command=command, pady=pady)
        button.pack()
        return button

    def create_entry(self, master, name="", height=None, width=None):
        """Creates entry widget"""
        """:param master: master window/tab, :param name: name of the entry, :param height: entry height,
           :param width: entry width"""
        entry = tk.Text(master=master, name=name, height=height, width=width)
        entry.pack()
        return entry

    def create_combo(self, master, textvariable, width, options, pady, side=None, anchor=None):
        """Creates combobox widget"""
        """:param master: master window/tab, :param textvariable : string variable associated with widget,
           :param width: widget width, :param options: options to choose from, :param pady: y-axis padding, 
           :param side: side on which should label be placed, :param anchor: side where widget should be anchored"""
        combo = ttk.Combobox(master=master, textvariable=textvariable, state="readonly", width=width)
        combo['values'] = options
        combo.current(0)
        if side is not None:
            combo.pack(pady=pady, side=side, anchor=anchor)
        else:
            combo.pack(pady=pady)
        return combo

    def create_radio(self, master, text, value, var, name, anchor):
        """Creates radiobutton widget"""
        """:param master: master window/tab, :param text: text of the widget, :param value: value of the widget,
           :param var: variable associated with widget, :param name: name of the widget, 
           :param anchor: side where widget should be anchored"""
        radio = tk.Radiobutton(master=master, text=text, value=value, var=var, name=name)
        radio.pack(anchor=anchor)
        return radio

    def create_window(self, title, geometry, color=None):
        """Creates new window"""
        """:param title: window title, :param geometry: window dimensions, :param color: background color"""
        window = tk.Tk()
        return self.create_window_properties(window, title, geometry, color)

    def create_top_level(self, title, geometry):
        """Creates new toplevel window"""
        """:param title: window title, :param geometry: window dimensions"""
        window = tk.Toplevel()
        return self.create_window_properties(window, title, geometry, 'white')

    def create_window_properties(self, window, title, geometry, color):
        """Sets properties to window"""
        """:param window: window object, :param title: window title, :param geometry: window dimensions,
           :param color: background color"""
        window.title(title)
        window.geometry(geometry)
        window.wm_iconbitmap("images/logo.ico")
        window.resizable(False, False)
        if color is not None:
            window.configure(bg=color)
        return window

    def create_scrollable_window(self, title, geometry, top_level=False, color=None):
        """Creates new scrollable window"""
        """:param title: window title, :param geometry: window dimensions, 
        :param top_level: if window should be toplevel-like type, :param color: background color"""
        if top_level:
            window = self.create_top_level(title, geometry)
        else:
            window = self.create_window(title, geometry)
        first_frame = tk.Frame(window)
        if color is not None:
            first_frame.configure(bg='white')
        first_frame.pack(fill=tk.BOTH, expand=1)
        canvas = tk.Canvas(master=first_frame)
        if color is not None:
            canvas.configure(bg='white')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar = ttk.Scrollbar(first_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
        second_frame = tk.Frame(canvas)
        if color is not None:
            second_frame.configure(bg='white')
        canvas.create_window((0,0), window=second_frame, anchor="nw")
        return window, second_frame, canvas

