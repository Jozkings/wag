from node import Node
from degrees import Degrees
from informations import FORM_NEUTRAL_D, FORM_NEUTRAL_S, G_OPERATIONS
import time
from collections import defaultdict
import networkx as nx
import os
import subprocess
from enum import IntEnum
from datetime import datetime
import random


"""Good text - normal punctuation, grammatically correct, same words written in the same form, 
   after punctuation is space"""
"""Self loops are not allowed! (will be removed)"""
"""Graph is always undirected!"""
"""Many functions are for debugging or were used in previous (mostly non-gui) versions,
   they stay here for possible future usage"""


class Graph(object):
    """object for creating graph from text and its editing, analyzing and saving"""

    class OrbitsTypesSumCount(IntEnum):
        TWO = 1
        THREE = 4
        FOUR = 15
        FIVE = 73

    class ConnectedGraphletsTypesSumCount(IntEnum):
        TWO = 1
        THREE = 3
        FOUR = 9
        FIVE = 30

    class AllGraphletsTypesSumCount(IntEnum):
        TWO = 2
        THREE = 6
        FOUR = 17

    def __init__(self, text):
        """Init function"""
        """:param text: string of good text, :param directed: boolean determining if graph is directed or not"""
        self._g = defaultdict(set)
        self._nodes = defaultdict(Node)
        self.nx_graph = None
        self.no_edges = 0
        self.file_name = None
        self.orbit_counts = []
        self.motifs_counts = []
        self.graphlets_counts = []
        self.graphlets_sum_counts = [-3 for _ in range(4)] #all these default values are not necessary, just hint
        self.basic_results = [-3 for _ in range(9)]  #which types are going to be saved there
        self.distributions = [defaultdict(int), [], [], defaultdict(int), []]
        self.comparision_results = [-3.0, tuple()]
        self.numeric_index = 0
        self.initialized = False
        self.degrees = None
        self.from_edge_list = False
        if text is not None:
            self.add_connections(text)

    """TEXT LOADING AND EDITING PART---------------------------------------------------------------------------------"""

    def load_graph_edge_list(self, file_name):
        """Loads directly graph from file, graph must be in good format without mistakes!!"""
        """:param file_name: file with graph in edge list format; first line indicates number of vertices and edges"""
        if self._g:
            raise Exception("Other text already loaded!")
        first = True
        with open(file_name, 'r') as file:
            for line in file:
                values = list(map(int, line.split(" ")))
                if first:
                    #no_vertices, no_edges = values[0], values[1]
                    first = False
                else:
                    success = self.add(values[0], values[1])
                    if success:
                        self.add_to_nodes(values[0], 1, True)
                        self.add_to_nodes(values[1], 1, True)
                        self._nodes[values[0]].add_count()
                        self._nodes[values[1]].add_count()
        #assert(no_vertices == self.get_order())
        #assert(no_edges == self.get_size())
        self.file_name = file_name
        self.initialized = True
        self.from_edge_list = True
        self.degrees = Degrees(self._g)

    def load_text(self, file_name):
        """Loads text from file into a graph"""
        """:param file_name: file with good text"""
        text = ""
        with open(file_name, 'r', encoding="utf8") as file:
            for line in file:
                text += line
        self.add_connections(text)

    def check_apostrophes(self, text):
        """Returns text without shortened words like are/is"""
        """:param text: array of words represented as strings"""
        new_text = []
        for word in text:
            if word[-2:] == "'s" or word[-2:] == "’s":
                if word[0].lower() == word[0]:  #basic check for person name
                    new_text.append(word[:-2])
                    new_text.append(FORM_NEUTRAL_S)
                elif word[:3] == 'let':
                    new_text.append(word[:-2])
                    new_text.append("us")
                else:
                    new_text.append(word)
            elif word[-3:] == "'re" or word[-3:] == "’re":
                new_text.append(word[:-3])
                new_text.append('are')
            elif word[-2:] == "'m" or word[-2:] == "’m":
                new_text.append(word[:-2])
                new_text.append('am')
            elif word[-3:] == "'ll" or word[-3:] == "’ll":
                new_text.append(word[:-3])
                new_text.append('will')
            elif word[-3:] == "'ve" or word[-3:] == "’ve":
                new_text.append(word[:-3])
                new_text.append('have')
            elif word[-2:] == "'d" or word[-2:] == "’d":
                new_text.append(word[:-2])
                new_text.append(FORM_NEUTRAL_D)
            elif word[-3:] == "n't" or word[-3:] == "n’t":
                new_text.append(word[:-3])
                new_text.append("not")
            elif '-' in word:
                new_text.append(word[:word.index('-')] + word[word.index('-')+1:])
            elif '—' in word:
                if word[-1] == '—':
                    new_text.append(word[:-1])
                else:
                    new_text.append(word[:word.index('—')])
                    new_text.append(word[:word.index('—')])
            elif word[-3:] == "n't" or word[-3:] == "n’t":
                new_text.append(word[:-3])
                new_text.append('not')
            else:
                new_text.append(word)
        return new_text

    """BUILDING AND EDITING GRAPH PART-------------------------------------------------------------------------------"""

    def add_connections(self, text):
        """Adds all nodes pairs to graph (should be good-formatted text, see top of file for more info)"""
        """:param text: string of good text"""
        text = text.translate(
            text.maketrans('!"“”#$%&()*+, -./:;<=>?@[\]^_{|}~—', '                                  ')).split()
        text = self.check_apostrophes(text)
        if len(text) == 1:
            self._g[text[0].lower()] = set()
            self.add_to_nodes(text[0].lower(), 0, False)
            self.initialized = True
            self.degrees = Degrees(self._g)
            self._nodes[text[0].lower()].add_count()
            return
        success = self.add(text[0].lower(), text[1].lower())
        first_success = False
        if success:
            first_success = True
            self.add_to_nodes(text[0].lower(), 1, False)
            self.add_to_nodes(text[1].lower(), 1, False)
        self._nodes[text[0].lower()].add_count()
        self._nodes[text[1].lower()].add_count()
        for i in range(1, len(text)-1):
            success = self.add(text[i].lower(), text[i+1].lower())
            if success:
                self.add_to_nodes(text[i].lower(), not first_success, False)
                self.add_to_nodes(text[i+1].lower(), 1, False)
                first_success = True
            self._nodes[text[i+1].lower()].add_count()
        self.initialized = True
        self.degrees = Degrees(self._g)

    def add(self, first_node, second_node):
        """Adds two node pairs connections to graph"""
        """:param first_node: first word from substring of text, 
        :param second_node: second word from substring of text"""
        if first_node not in self._g:
            self._g[first_node] = set()
        if second_node not in self._g:
            self._g[second_node] = set()
        if first_node == second_node:
            return True
        if second_node in self._g[first_node]:
            return False
        if first_node in self._g[second_node]:
            return False
        self._g[first_node].add(second_node)
        self._g[second_node].add(first_node)
        self.no_edges += 1
        return True

    def add_to_nodes(self, node, add, from_edge_list):
        """Adds node representing word present in text"""
        """:param node: word from text, :param add: if should be node count increased (covers edge cases),
            :param from_edge_list: if node is from edge list (thus guaranteed to be number)"""
        if add and node not in self._nodes:
            if from_edge_list:
                if type(node) == int:
                    numeric = node
                else:
                    numeric = int(node)
            else:
                numeric = self.numeric_index
                self.numeric_index += 1
            new_node = Node(node, number_value=numeric)
            self._nodes[node] = new_node

    def remove(self, node):
        """Removes node and all its connections or raises Exception if no such node present"""
        """:param node: some string, makes sense to be word from text given"""
        if node not in self._g:
            raise Exception("No such node is in this graph!")
        for key, value_set in self._g.items():
            if node in value_set:
                value_set.remove(node)
        del self._g[node]

    """VISUALIZATION PART-------------------------------------------------------------------------------------"""

    def create_nx_graph(self):
        """Creates same graph in networkX library (for visualization or some statistics computing)"""
        self.nx_graph = nx.Graph()
        for node in self._g.keys():
            self.nx_graph.add_node(self._nodes[node].get_number_value())
            for neighbour in self._g[node]:
                if self._nodes[node].get_number_value() < self._nodes[neighbour].get_number_value():
                    self.nx_graph.add_edge(self._nodes[node].get_number_value(),
                                           self._nodes[neighbour].get_number_value())

    """RESULTS PRINTING PART-----------------------------------------------------------------------------------------"""

    def print_graph(self):
        """Prints information and vertices with their connections of this graph"""
        print(f'Number of nodes in this graph: {str(len(self._g))}')
        for key, value_set in self._g.items():
            print(f'{key}: {value_set}')

    def print_degree_stats(self, degrees, maximum, minimum, average):
        """Prints all statistics about degrees of vertices in this graph"""
        """:param degrees: degrees of nodes, :param maximum: maximum degree of node in graph,
        :param minimum: minimum degree of node in graph, :param average: average degree of node in graph"""
        print(f'Degrees of all vertices of this graph: {degrees}')
        print(f'Maximum degree: vertex "{maximum}" with degree {degrees[maximum]}')
        print(f'Minimum degree: vertex "{minimum}" with degree {degrees[minimum]}')
        print(f'Average degree of vertex in this graph: {average}')

    def print_all_degree_stats(self):
        """Calculates and prints many statistics about degrees of vertices in graph;
        does same as other specific functions"""
        degrees = self.get_all_degrees()
        maximum = max(degrees, key=degrees.get)
        minimum = min(degrees, key=degrees.get)
        average = sum(degrees.values()) / len(degrees)
        self.print_degree_stats(degrees, maximum, minimum, average)

    def print_whole_clustering_coefficient(self):
        """Prints clustering coefficient of whole graph"""
        print(f'Clustering coefficient of this graph is: {self.get_whole_clustering_coefficient()}')

    """INFORMATION ABOUT STRUCTURE GETTING PART----------------------------------------------------------------------"""

    def is_initialized(self):
        """Returns if graph was succesfully initialized"""
        return self.initialized

    def get_connected_nodes(self, node):
        """Gets all nodes connections from this node or raises Exception if no such node present"""
        """param node: some string, makes sense to be word from text given"""
        if node not in self._g:
            raise Exception("No such node is in this graph!")
        return self._g[node]

    def get_connecting_nodes(self, node):
        """Gets set of all nodes connecting to this node or raises Exception if no such node present"""
        """param node: some string, makes sense to be word from text given"""
        if node not in self._g:
            raise Exception("No such node is in this graph!")
        nodes = set()
        for key, value_set in self._g.items():
            if node in value_set:
                nodes.add(key)
        return nodes

    def get_neigbours(self, node):
        """Gets set of all nodes connected from/to this node or raises Exception if no such node present"""
        """param node: some string, makes sense to be word from text given"""
        nodes = set()
        nodes |= self.get_connected_nodes(node)
        nodes |= self.get_connecting_nodes(node)
        return nodes

    def is_connected(self, first_node, second_node):
        """Returns if second_node is connected from first_node or raises Exception if some of node is not present"""
        """:param first_node: some string, makes sense to be word from text given, :param second_node: some 
        other string, makes sense to be word from text given"""
        if first_node not in self._g:
            raise Exception("First node is not in this graph!")
        if second_node not in self._g:
            raise Exception("Second node is not in this graph!")
        return second_node in self._g[first_node]

    """STATISTICS GETTING PART---------------------------------------------------------------------------------------"""

    def get_g(self):
        """Return graph as dictionary"""
        return self._g

    def get_nodes(self):
        """Return dictionary of nodes objects"""
        return self._nodes

    def get_nx_g(self):
        """Returns networkX implementation of graph"""
        if self.nx_graph is None:
            self.create_nx_graph()
        return self.nx_graph

    def get_shortest_path_length_and_diameter(self):
        """Computes, saves and returns average shortest path length and graph diameter"""
        if self.basic_results[7] != -3 and self.basic_results[8] != -3:
            return self.basic_results[7], self.basic_results[8]
        lengths = dict(self.get_shortest_path_length_all())
        maxo = 0
        avg = 0
        for value in lengths.values():
            maxo = max(maxo, max(value.values()))
            avg += sum(value.values())
        average_result = round((avg/(self.get_order() * (self.get_order() - 1))), 5)
        self.basic_results[7] = maxo
        self.basic_results[8] = 0 if self.get_order() <= 1 else average_result
        return maxo, 0 if self.get_order() <= 1 else average_result

    def get_density(self):
        """Computes, saves and returns density of the graph"""
        common = (self.get_size() / (self.get_order() * (self.get_order() - 1))) if self.get_order() > 1 else 0
        self.basic_results[2] = round(2 * common, 5)
        return round(2 * common, 5)

    def get_different_nodes_percentage(self):
        """Computes and return percentage of different graph nodes to all words in text (mots of the time
            not useful in graph created from edge_list"""
        different = self.get_order()
        print(self._nodes)
        all = 0
        for node in self._nodes.values():
            all += node.get_count()
        return round(different / all, 5)

    def get_nodes_degree_distribution(self):
        """Computes, saves and returns degree distribution of nodes in graph and returns it as dictionary,
         where key = degree, value = number of nodes with that degree"""
        if self.distributions[0]:
            return self.distributions[0]
        distribution = defaultdict(int)
        for node in self._g.keys():
            distribution[len(self._g[node])] += 1
        self.distributions[0] = distribution
        return distribution

    def get_nodes_degree_distribution_normalized(self):
        """Computes, saves and returns degree distribution of nodes in graph, normalizes it by number
          of nodes an return array where index = degree, value = normalized value"""
        if self.distributions[1]:
            return self.distributions[1]
        distribution = self.get_nodes_degree_distribution()
        N = len(self._g)
        normalized = [0] * N
        for key, value in distribution.items():
            normalized[key] = value / N
        self.distributions[1] = normalized
        return normalized

    def get_order(self):
        """Saves and returns number of vertices in graph"""
        if self.basic_results[0] != -3:
            return self.basic_results[0]
        self.basic_results[0] = len(self._g)
        return len(self._g)

    def get_degree_average(self):
        """Saves and returns average degree in graph"""
        self.basic_results[5] = self.degrees.get_avg_degree_value()
        return self.degrees.get_avg_degree_value()

    def get_minimal_degree(self):
        """Saves and returns vertex with and minimal degree in graph"""
        self.basic_results[4] = self.degrees.get_min_degree()[1]
        return self.degrees.get_min_degree()

    def get_maximal_degree(self):
        """Saves and returns vertex with and maximal degree in graph"""
        self.basic_results[3] = self.degrees.get_max_degree()[1]
        return self.degrees.get_max_degree()

    def get_size(self):
        """Saves and returns number of edges in graph (with self-loops)"""
        if self.basic_results[1] != -3:
            return self.basic_results[1]
        self.basic_results[1] = self.no_edges
        return self.no_edges

    def get_all_degrees(self):
        """Returns degrees of nodes in graph"""
        return self.degrees.get_degrees()

    def get_degree(self, node):
        """Returns degree of node or raises Exception if no such node present"""
        """param node: some string, makes sense to be word from text given"""
        if node not in self._g:
            raise Exception("Node is not in this graph!")
        return self.degrees.get_degree(node)

    def get_clustering_coefficient(self, node):
        """Computes and returns clustering coefficient of node or raises Exception if no such node present"""
        """param node: some string, makes sense to be word from text given"""
        if node not in self._g:
            raise Exception("Node is not in this graph!")
        neighbours = self._g[node]
        added = set()
        for neigh1 in neighbours:
            for neigh2 in neighbours:
                if neigh1 != neigh2 and (self.is_connected(neigh1, neigh2) or self.is_connected(neigh2, neigh1)):
                    if (neigh1, neigh2) not in added and (neigh2, neigh1) not in added:
                        added.add((neigh1, neigh2))
        degree = self.get_degree(node)
        if degree == 1:
            lower = 0
        else:
            lower = ((degree-1)*degree)
        return 0 if lower == 0 else 2*len(added)/lower

    def get_whole_clustering_coefficient(self):
        """Computes, saves and returns average clustering coefficient of whole graph"""
        if self.basic_results[6] != -3:
            return self.basic_results[6]
        summing = 0
        for key in self._g.keys():
            summing += self.get_clustering_coefficient(key)
        self.basic_results[6] = round(summing/len(self._g), 5)
        return round(summing/len(self._g), 5)

    def get_average_path_length(self):
        """Saves and returns average shortest path length in graph using function from networkx library"""
        if self.basic_results[8] != -3:
            return self.basic_results[8]
        if self.nx_graph is None:
            self.create_nx_graph()
        result = nx.average_shortest_path_length(self.nx_graph)
        self.basic_results[8] = round(result, 5)
        return round(result, 5)

    def get_shortest_path_length_all(self):
        """Returns shortest path length of all nodes in graph using function from networkx library"""
        if self.nx_graph is None:
            self.create_nx_graph()
        return nx.shortest_path_length(self.nx_graph)

    def get_diameter(self):
        """Computes, saves and returns length of longest shortest path, also known as diameter of graph"""
        if self.basic_results[7] != -3:
            return self.basic_results[7]
        lengths = dict(self.get_shortest_path_length_all())
        maxo = 0
        for value in lengths.values():
            maxo = max(maxo, max(value.values()))
        self.basic_results[7] = maxo
        return maxo

    def get_shortest_path_length_distribution(self):
        """Computes, saves and returns distribution of shortest path length of all nodes in graph"""
        if self.distributions[2]:
            return self.distributions[2]
        lengths = dict(self.get_shortest_path_length_all())
        distributions = [0] * int(self.get_order())
        for value in lengths.values():
            for val in value.values():
                distributions[val] += 1
        distributions = [val/2 for val in distributions]
        self.distributions[2] = distributions
        return distributions

    def get_clustering_coefficient_distribution(self):
        """Computes, saves and returns distribution of clustering coefficients in graph as a map"""
        if self.distributions[3]:
            return self.distributions[3]
        distributions = defaultdict(int)
        for node in self._g.keys():
            coefficient = self.get_clustering_coefficient(node)
            distributions[coefficient] += 1
        self.distributions[3] = distributions
        return distributions

    def get_clustering_to_degree_distribution(self):
        """Computes, saves and returns distribution of average clustering coefficient to degree of nodes as a list"""
        if self.distributions[4]:
            return self.distributions[4]
        degrees = defaultdict(set)
        for node in self._g.keys():
            degrees[len(self._g[node])].add(node)
        distributions = [0] * int(self.get_order())
        for degree, nodes in degrees.items():
            average = 0
            for node in nodes:
                coefficient = self.get_clustering_coefficient(node)
                average += coefficient
            average /= len(nodes)
            distributions[degree] = average
        self.distributions[4] = distributions
        return distributions

    def get_word_count(self, word):
        """Returns number of word occurrences in text or raises Exception if no such word present"""
        """:param word: some string, makes sense to be word from text given"""
        if word not in self._g:
            raise Exception("No such word is in this graph!")
        return self._nodes[word].get_count()

    """GUI CALLED FUNCTIONS PART----------------------------------------------------------------------------------"""

    def read_orbit_matrix(self, file_name, max_size):
        """Reads matrix of orbits of graph returned in text file from orca algorithm"""
        """:param file_name: name of the file with matrix, :param max_size: maximum orbits size"""
        if not os.path.isfile(file_name):
            raise Exception("Orbit file cannot be loaded!")
        size = self.OrbitsTypesSumCount.FOUR if max_size == 4 else self.OrbitsTypesSumCount.FIVE
        self.orbit_counts = [[0 for _ in range(size)] for _ in range(self.get_order())]
        index = 0
        with open(file_name, 'r') as file:
            for line in file:
                self.orbit_counts[index] = list(map(int, line.split(" ")))
                index += 1

    def get_orbit_matrix(self, graphlet_max_size):
        """Calls orca algorithm for counting orbits in graph and function for reading resulting file"""
        """:param graphlet_max_size: maximum graphlet size"""
        if self.file_name is None:
            now_string = datetime.now().strftime("%d-%m-%Y_%H%M%S")
            name_add = f'{now_string}_{random.randint(1, 10000)}'
            name = f"interfiles\\graphlets_preparation_{name_add}.txt"
            self.save_for_cpp(name)
        out_file = self.file_name[:-4] + "_orca.txt"
        args = f' {graphlet_max_size} {self.file_name} {out_file}'
        output = subprocess.Popen(
            "orca\\orca.exe" + args)
        exit_code = output.wait()
        if exit_code != 0:
            raise Exception("Error while counting orbits!")
        self.read_orbit_matrix(out_file, graphlet_max_size)
        return out_file

    def set_next_bar_item(self, bar, label, move_bar, operation_index, operation_percentage):
        """Moves progress bar of analysis and increases index for getting right operation name"""
        """:param bar: bar object, :param label: label for text showing current operation,
           :param move_bar gui function for moving bar, :param operation_index: current operation
            index (saved in list), :param operation_percentage: percentage of new bar movement"""
        move_bar(bar, operation_percentage, label, G_OPERATIONS[operation_index])
        return operation_index + 1

    def basic_analysis(self, bar, label, move_bar):
        """Runs graph analysis, saves results and moves progress bar according to current operation"""
        """:param bar: bar object, :param label: label for text showing current operation,
           :param move_bar gui function for moving bar"""
        operations_count = 8
        operation_percentage = int(100 / operations_count)
        operation_index = 0
        all_operations = [self.get_order, self.get_size, self.get_density, self.get_maximal_degree,
                          self.get_minimal_degree, self.get_degree_average, self.get_whole_clustering_coefficient,
                          self.get_shortest_path_length_and_diameter]
        for _ in range(len(all_operations)):
            operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
            _ = all_operations[operation_index-1]()
        time.sleep(0.8)
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        operation_index -= 1

    def graphlet_analysis(self, bar, label, max_size, move_bar):
        """Runs graphlet analysis, saves results and moves progress bar according to current operation"""
        """:param bar: bar object, :param label: label for text showing current operation,
           :param max_size: maximum graphlets size, :param move_bar gui function for moving bar"""
        operations_count = 6
        operation_percentage = int(100 / operations_count)
        operation_index = 9
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        if self.file_name is not None:
            file_name = f"interfiles\\cpp_{self.file_name}"
        else:
            now_string = datetime.now().strftime("%d-%m-%Y_%H%M%S")
            name_add = f'{now_string}_{random.randint(1, 10000)}'
            file_name = f"interfiles\\cpp_preparation_{name_add}.txt"
        self.save_for_cpp(file_name)
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        out_file = self.get_orbit_matrix(max_size)
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        args = f'{max_size} {self.file_name} {out_file}'
        output = subprocess.Popen(f'graphlets-pgd\\cmake-build-debug\\graphlets.exe {args}')
        exit_code = output.wait()
        if exit_code != 0:
            raise Exception("Error during graphlet analysis!")
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        file_name = "result_graphlets.goi"
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        with open(file_name, 'r') as file:
            data = [line.strip().split() for line in file if line]
        os.remove(file_name)
        for index, dato in enumerate(data):
            if index == 1:
                self.motifs_counts = list(map(int, dato))
            elif index == 2:
                self.graphlets_counts = list(map(int, dato))
                self.graphlets_sum_counts[0] = self.graphlets_counts[0]
                self.graphlets_sum_counts[1] = sum(self.graphlets_counts[1:3])
                self.graphlets_sum_counts[2] = sum(self.graphlets_counts[3:9])
                if len(self.graphlets_counts) == self.ConnectedGraphletsTypesSumCount.FIVE:
                    self.graphlets_sum_counts[3] = sum(self.graphlets_counts[10:])
        time.sleep(0.8)
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        operation_index -= 1

    def get_gdda_rgfd(self, other_graph, bar, label, move_bar):
        """Runs comparision analysis, saves results and moves progress bar according to current operation"""
        """:param other_graph: other graph object for comparision, :param bar: bar object,
           :param label: label for text showing current operation, :param move_bar gui function for moving bar"""
        operations_count = 5
        operation_percentage = int(100 / operations_count)
        operation_index = 15
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        first_out_file = self.file_name[:-4] + "_orca.txt"
        second_out_file = other_graph.file_name[:-4] + "_orca.txt"
        args = f'{first_out_file} {second_out_file}'
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        output = subprocess.Popen(f'graphlets-pgd\\cmake-build-debug\\graphlets.exe {args}')
        exit_code = output.wait()
        if exit_code != 0:
            raise Exception("Error during graphlet analysis!")
        if not self.from_edge_list:
            os.remove(self.file_name)
        if not other_graph.from_edge_list:
            os.remove(other_graph.file_name)
        os.remove(first_out_file)
        os.remove(second_out_file)
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        file_name = "resultsx_graphlets.goi"
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        with open(file_name, 'r') as file:
            data = [line.strip().split() for line in file if line]
        os.remove(file_name)
        for index, dato in enumerate(data):
            if index == 0:
                self.comparision_results[0] = float(dato[0])
                other_graph.comparision_results[0] = float(dato[0])
            else:
                self.comparision_results[1] = tuple(map(float, dato))
                other_graph.comparision_results[1] = tuple(map(float, dato))
        time.sleep(0.8)
        operation_index = self.set_next_bar_item(bar, label, move_bar, operation_index, operation_percentage)
        operation_index -= 1

    """SAVING PART------------------------------------------------------------------------------------------------"""

    def save_words_to_file(self, file_name):
        """Saves all graph nodes values into text file"""
        """:param file_name: name of the resulting file"""
        with open(file_name, 'w') as file:
            for node in self._nodes.keys():
                file.write(f'{self._nodes[node].get_value()} : {self._nodes[node].get_count()}\n')

    def save_for_cpp(self, file_name):
        """creates and saves graph as edge list to .txt file using networkX library. Nodes are converted to numbers"""
        """:param file_name: name of the resulting file"""
        if self.file_name is not None:
            #raise Exception("Edge list already present!")
            return
        if file_name[-4:] != ".txt":
            raise Exception("Destination file is not .txt type!")
        if self.nx_graph is None:
            self.create_nx_graph()
        with open(file_name, 'w') as file:
            file.write(f"{self.get_order()} {self.get_size()}\n")
            for edge in self.nx_graph.edges:
                f, s = edge
                file.write(f"{f} {s}\n")
        self.file_name = file_name

    def save_as_gexf(self, file_name):
        """creates and saves graph to .gexf file using networkX library"""
        """:param file_name: name of the resulting file"""
        if file_name[-5:] != ".gexf":
            raise Exception("Destination file is not .csv type!")
        if self.nx_graph is None:
            self.create_nx_graph()
        nx.write_gexf(self.nx_graph, file_name)

    def save_as_csv(self, file_name, to_numbers=False):
        """creates and saves graph to .csv file using networkX library"""
        """:param file_name: name of the resulting file, :param to_numbers: conversion of nodes to numbers"""
        if file_name[-4:] != ".csv":
            raise Exception("Destination file is not .csv type!")
        if self.nx_graph is None:
            self.create_nx_graph()
        numbers = {}
        index = 0
        with open(file_name, 'w') as file:
            file.write("src,dst\n")
            for edge in self.nx_graph.edges:
                f, s = edge
                if not to_numbers:
                    file.write(f'{f},{s}\n')
                else:
                    if f in numbers:
                        f = numbers[f]
                    else:
                        numbers[f] = index
                        f = index
                        index += 1
                    if s in numbers:
                        s = numbers[s]
                    else:
                        numbers[s] = index
                        s = index
                        index += 1
                    file.write(f"{f},{s}\n")


"END OF IMPLEMENTATION-------------------------------------------------------------------------------------------------"
