class Node(object):
    """object for saving useful nodes information"""
    def __init__(self, value='', number_value=None, count=0):
        """Init function"""
        """:param value: text of node, :param count: number of occurrences of node"""
        self.value = value
        self.count = count
        self.number_value = number_value

    def add_count(self):
        """Adds count of node, aka times current node was referenced in text"""
        self.count += 1

    def substract_count(self):
        """Substracts count of node, aka times current node was referenced in text"""
        self.count += 1

    def get_count(self):
        """Returns count of node, aka times current node was referenced in text"""
        return self.count

    def get_value(self):
        """Returns value (text) of node"""
        return self.value

    def set_number_value(self, number):
        """Sets number value of node"""
        self.number_value = number

    def get_number_value(self):
        """Returns number value of node"""
        return self.number_value

    def __repr__(self):
        """Returns value and count representation of node"""
        return f'Node value: {self.value}, node count: {self.count}'
