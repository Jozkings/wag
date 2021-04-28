import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FormatStrFormatter

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import random

"""Some of the functions below are not used in final implementation (pre-final functions), but can be
   in the future"""


class Plot(object):
    """object for manipulating with plotting using library matplotlib.pyplot and networkX in some cases"""
    COLOR_SPECTRUMS = ['purplish', 'rainbow']   #rainbow  #rainbow has more different color shades, purplish less cold colors
    NUMBER_TYPES = [int, float]

    def __init__(self, master):
        """Init function"""
        """:param master: card of application window"""
        self.figure = plt.figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.axis = self.figure.add_subplot(111)
        y_formatter = FormatStrFormatter('%.3f')
        self.axis.yaxis.set_major_formatter(y_formatter)
        self.x_scale = "linear"
        self.y_scale = "linear"

    def new_figure(self, figure_size=None):
        """Creates new figure for plotting"""
        """:param figure_size: size of the figure"""
        if figure_size is None:
            self.figure = plt.figure()
        else:
            self.figure = plt.figure(figsize=figure_size)

    def new_canvas(self, master):
        """Creates new canvas for plotting"""
        """:param master: master figure"""
        if self.canvas is None or master is None:
            raise Exception("Bad format of canvas or tkinter master!")
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)

    def get_canvas(self):
        """Returns current canvas"""
        return self.canvas

    def show_graph(self, graph):
        """Plots a network using networkx library; graph should not be big (max 100 nodes)"""
        self.axis.clear()
        g = graph.get_g()
        nx_g = graph.get_nx_g()
        if len(g) > 100:
            n = len(g)
            raise Exception(f"Network is too big to visualize (maximum number of nodes - 100, current number of nodes - {n}")
        colors = []
        nodes = nx_g.nodes()
        palette = self.set_colors(len(g))
        for node in nodes:
            position = int(nx_g.degree[node] / (len(g) / len(palette)))
            colors.append(palette[position])
        self.set_legend('upper left', colors, palette, len(g), label="")
        self.set_title('Slovná sieť')
        nx.draw(nx_g, with_labels=True, node_size=1000, node_color=colors, ax=self.axis)
        self.axis.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        self.figure.canvas.draw()

    def get_linear_binning(self, x_values1, y_values1, x_values2, y_values2):
        """Gets x-axis values for linear plotting (if not already present)"""
        """:param x_values1: x-axis values of first graph or None, :param y_values1: y-axis values of first graph,
           :param x_values2: x-axis values of second graph or None, :param y_values2: y-axis values of second graph"""
        if x_values1 is None and y_values1 is not None:
            length = 1 if type(y_values1) in self.NUMBER_TYPES else len(y_values1)
            x_values1 = [1 for _ in range(length)]
        if x_values2 is None and y_values2 is not None:
            length = 1 if type(y_values2) in self.NUMBER_TYPES else len(y_values2)
            x_values2 = [1 for _ in range(length)]
        return x_values1, x_values2

    def get_bins(self, y_values):
        """Gets bins of values for logarithmic binning"""
        """:param y_values: y-axis values of graph"""
        first_bins = [[] for _ in range(len(y_values))]
        size = 1
        bin_index = 0
        current_size = size
        values_index = 0
        while values_index < len(y_values):
            first_bins[bin_index].append(y_values[values_index])
            values_index += 1
            current_size -= 1
            if current_size == 0:
                size *= 2
                current_size = size
                bin_index += 1
        first_bins = first_bins[:bin_index]
        if not first_bins[-1]:
            first_bins = first_bins[:-1]
        return first_bins

    def get_log_binning_values(self, y_values):
        """Creates x-axis values for plotting and calls functions to create logarithmic bins"""
        """:param y_values: y-axis values of graph"""
        index = 0
        while y_values[index] == 0 and index < len(y_values) - 1:
            index += 1
        y_values = y_values[index:]  # don't need k=0 or first misleading values
        first_bins = self.get_bins(y_values)
        real_y_values = self.get_bin_distribution(first_bins)
        length = len(real_y_values)
        x_values = [2 ** i for i in range(length)]
        return x_values, real_y_values

    def get_log_binning(self, x_values1, y_values1, x_values2, y_values2):
        """Gets both y and x-axis values for logarithmic binning plotting"""
        """:param x_values1: x-axis values of first graph or None, :param y_values1: y-axis values of first graph,
           :param x_values2: x-axis values of second graph or None, :param y_values2: y-axis values of second graph"""
        real_y_values1, real_y_values2 = y_values1, y_values2
        if x_values1 is None:
            length = 1 if type(y_values1) in self.NUMBER_TYPES else len(y_values1)
            x_values1 = [1 for _ in range(length)]
        else:
            x_values1, real_y_values1 = self.get_log_binning_values(y_values1)
        if x_values2 is None:
            length = 1 if type(y_values2) in self.NUMBER_TYPES else len(y_values2)
            x_values2 = [1 for _ in range(length)]
        else:
            x_values2, real_y_values2 = self.get_log_binning_values(y_values2)
        return x_values1, x_values2, real_y_values1, real_y_values2

    def get_bin_distribution(self, bins):
        """Computes final bins values"""
        """:param bins: bins of y-axis values of graph"""
        distribution = []
        for index, bin in enumerate(bins):
            nodes_count = sum(bin)
            degrees_count = 2 ** index
            distribution.append(nodes_count / degrees_count)
        return distribution

    def update(self, x_values1, y_values1, x_values2, y_values2, scatter1=False, scatter2=False, can_log_bin=False):
        """Updates current figure with new plot with custom settings. Some parameters can be None-type"""
        """:param x_values1: x-axis values of first graph, :param y_values1: y-axis values of first graph,
           :param x_values2: x-axis values of second graph, :param y_values2: y-axis values of second graph
           :param scatter1 : option for plotting first graph scatteredly, :param scatter2 : option for plotting 
           second graph scatteredly, :param can_log_bin: boolean telling if logarithmic binning should be applied"""

        log_binning = True if self.x_scale == "log" and self.y_scale == "log" and can_log_bin else False
        if scatter1 or scatter2:
            self.update(x_values1, y_values1, x_values2, y_values2, False, False, can_log_bin) #preventing axis scaling bug
        self.axis.clear()
        self.set_x_scale()
        self.set_y_scale()

        if not log_binning:
            x_values1, x_values2 = self.get_linear_binning(x_values1, y_values1, x_values2, y_values2)
        else:
            x_values1, x_values2, y_values1, y_values2 = self.get_log_binning(x_values1, y_values1, x_values2, y_values2)
        if y_values1 is not None and y_values1 != -3:
            if not scatter1:
                plt.plot(x_values1, y_values1, color='blue')
            else:
                plt.plot(x_values1, y_values1, 'o', color='blue')
        if y_values2 is not None and y_values2 != -3:
            if not scatter2:
                plt.plot(x_values2, y_values2, color='red')
            else:
                plt.plot(x_values2, y_values2, 'o', color='red')
        #self.set_legend('upper left')
        self.set_title('Porovnanie sietí')
        self.figure.canvas.draw()

    def new_axis(self):
        """Creates new axis for plotting (hack for having two plots in scatter graph)"""
        self.axis = self.figure.add_subplot(111)

    def set_scale_variables(self, x_function, y_function):
        """Scales axis according to parameters (only saves option!)"""
        """:param x_function: x-axis scaling function, can be either 'linear' or 'log',
           :param y_function: y-axis scaling function, can be either 'linear' or 'log'"""
        if x_function == "linear":
            self.x_scale = "linear"
        elif x_function == "log":
            self.x_scale = "log"
        else:
            raise Exception("Only allowed scales are: 'linear', 'log'")
        if y_function == "linear":
            self.y_scale = "linear"
        elif y_function == "log":
            self.y_scale = "log"
        else:
            raise Exception("Only allowed scales are: 'linear', 'log'")

    def set_x_scale(self):
        """Sets scale of x axis"""
        plt.xscale(self.x_scale)

    def set_y_scale(self):
        """Sets scale of y axis"""
        plt.yscale(self.y_scale)

    def set_colors(self, length):
        """Returns list of colors to be used in plotting of whole graph"""
        """:param length: number of nodes in graph"""
        #spektrum = random.choice(self.COLOR_SPECTRUMS) #bugged
        spektrum = 'rainbow'
        if spektrum== 'rainbow':
            cm = plt.get_cmap('gist_rainbow')
            colors = [cm(1. * i / 20) for i in range(length)]
        elif spektrum == 'purplish':
            colors = ['violet', 'blueviolet', 'lightsteelblue', 'dodgerblue', 'darkturquoise',
                      'darkgreen', 'lime', 'yellow']
        else:
            raise Exception("No other color palette defined!")
        return colors

    def get_patches(self, colors, palette, length):
        """Returns patches used in legend of whole graph"""
        """:param colors: colors of nodes, :param palette: list of all colors,
           :param length: number of nodes in graph"""
        patches = [None] * len(palette)
        for color in set(colors):
            val = palette.index(color)
            low = val * (length / len(palette))
            up = low + (length / len(palette)) - 1
            patch = mpatches.Patch(color=color, label=f'Degrees <{low}, {up}>')
            patches[val] = patch
        return list(filter(None.__ne__, patches))

    def compact_data_list(self, data):
        """Cuts all zero values from end of list data for better plotting proposition"""
        """:param data: data to be cut"""
        if type(data) is not list:
            raise Exception("Only lists can be compacted!")
        index = -999
        for i in range(len(data) - 1, -1, -1):
            if data[i] != 0:
                index = i
                break
        new_data = data[:index + 1] if index != -999 else []
        return new_data

    def scatter_plot(self, data, x_data=None, sign="o", label=""):
        """Creates scatter plot"""
        """:param data: data to be plotted, :param x_data: present if plotting from map,
         :param sign: shape of plotted points, :param label: label of plotted graph """
        if self.axis is None:
            self.new_axis()
        if x_data is None:
            x_data = [i for i in range(len(data))]
        self.axis.plot(x_data, data, sign, label=label)

    def line_plot(self, data, x_data=None, label=""):
        """Creates line plot"""
        """:param data: data to be plotted, :param x_data: present if plotting from map,
           :param label: label of plotted graph """
        if x_data is None:
            plt.plot(data, label=label)
        else:
            plt.plot(x_data, data, label=label)

    def set_legend(self, location, colors=None, palette=None, length=None, label=""):
        """Sets legend of figure, could also set colors and size of circles as nodes in whole graph visualization"""
        """:param location: location of legend, :param colors: colors to be used for nodes,
        :param palette: palette of possible colors to be chosen from, :param length: number of nodes in graph"""
        if colors:
            plt.legend(loc=location, handles=self.get_patches(colors, palette, length), prop={'size': 6})
            return
        if label:
            plt.legend(loc=location, label=label)
        else:
            plt.legend(loc=location)

    def set_title(self, title):
        """Sets title of plot"""
        """:param title: name of the figure"""
        plt.title(title)

    def save_figure(self, file_name):
        """Saves figure to a file"""
        """:param file_name: name of the file"""
        plt.savefig(file_name, bbox_inches="tight")

    def show_figure(self):
        """Plots figure"""
        plt.show()

