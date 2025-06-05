# COLOR : NONE(GREY), RED, BLUE, GREEN, 

class Node:
    def __init__(self, pixel_position):
        self.size = len(pixel_position)
        self.color = 'grey'
        self.associated_nodes = []
        self.pixel_positions = pixel_position


    def AddAssociatedNode(self, new_node):
        if (new_node in self.associated_nodes):
            return
        self.associated_nodes.append(new_node)

    def GetAssociatedNode(self):
        return self.associated_nodes
    
    def GetPixelPositions(self):
        return self.pixel_positions

    def BiggerSize(self, size):
        if (size >= self.size):
            return True
        return False