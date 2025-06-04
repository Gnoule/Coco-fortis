from Nodes import Node

class Graph:

    def __init__(self, grid):
        self.nodes = []
        self.CreateNode(grid)


    def CreateNode(self, grid):
        pos_already_visited = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if ((x,y) in pos_already_visited):
                    continue
                node = Node() 
                self.CreateNodeWithColor(grid, [x,y])
                self.nodes.append(node)

    # current_pos[0] -> x
    # current_pos[1] -> y
    def CreateNodeWithColor(self, grid, current_pos, pixel_found=[]):
        for y in range (0, 3):
            for x in range (0, 3):
                pos_tested = (current_pos[0] + x, current_pos[1] + y)
                actual_value = grid[pos_tested[1]][pos_tested[0]]
                if (actual_value != 0 and pixel_found):
                    self.CreateNodeWithColor()
    
    



    def CreateNodeWithNeighbors(self, grid):
        pass

    def CreateNodeHorizontaly(self, grid):
        pass

    def CreateNodeVertically(self, grid):
        pass

    def CreateEdges(self):
        pass

    def ShowGraph(self):
        pass