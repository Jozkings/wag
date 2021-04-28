class Degrees(object):
    """object for saving degree informatians about graph"""

    def __init__(self, graph):
        self.max_degree_node = None
        self.max_degree_value = float("-inf")
        self.min_degree_node = None
        self.min_degree_value = float("inf")
        self.avg_degree = 0
        self.degrees = {}
        self.graph_ref = graph
        self.compute_degrees()

    def get_degree(self, node):
        """returns degree of node"""
        """:param node: node of the graph"""
        return self.degrees[node]

    def get_degrees(self):
        """returns all nodes degrees as dictionary"""
        return self.degrees

    def get_min_degree(self):
        """returns minimal degree as pair: node, node degree value"""
        return self.min_degree_node, self.min_degree_value

    def get_max_degree(self):
        """returns maximum degree as pair: node, node degree value"""
        return self.max_degree_node, self.max_degree_value

    def get_avg_degree_value(self):
        """returns average degree value of nodes"""
        return self.avg_degree

    def get_stats_degrees(self):
        """returns maximum and minimal degree as pair: node, node degree value and average degree value"""
        return (self.max_degree_node, self.max_degree_value), \
               (self.min_degree_node, self.min_degree_value), self.avg_degree

    def compute_degrees(self):
        """computes degrees of nodes in graph and saves them (together with minimal, maximum and avarage degree)"""
        degree_sum = 0
        for key in self.graph_ref:
            degree = len(self.graph_ref[key])
            self.degrees[key] = degree
            if degree < self.min_degree_value:
                self.min_degree_value = degree
                self.min_degree_node = key
            if degree > self.max_degree_value:
                self.max_degree_value = degree
                self.max_degree_node = key
            degree_sum += degree
        self.avg_degree = round(degree_sum / len(self.degrees), 5) if len(self.degrees) > 0 else 0