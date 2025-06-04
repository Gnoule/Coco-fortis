# COLOR : NONE(GREY), RED, BLUE, GREEN, 

class Node:
    def __init__(self):
        self.size = 0
        self.color = 'NONE'
        self.associated_nodes = []
        self.pixel_positions = []


    def AddAssociatedNode(self, new_node):
        self.associated_nodes.append(new_node)

    def BiggerSize(self, size):
        if (size >= self.size):
            return True
        return False