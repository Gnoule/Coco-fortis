from Nodes import Node
import networkx as nx
import matplotlib.pyplot as plt

class Graph:

    def __init__(self, grid):
        self.nodes = []
        self.CreateNode(grid, 'NEIGHBOR')
        self.CreateEdges(grid)


    def CreateNode(self, grid, type="NEIGHBOR"):
        pos_already_visited = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if ((x,y) in pos_already_visited or (grid[y][x] == 0)):
                    continue
                pixel_found = [(x,y)]
                pixel_value = [(x,y)]
                if type == "NEIGHBOR":
                    self.CreateNodeWithNeighbors(grid, [x,y], pixel_found, pos_already_visited)
                elif type == "COLOR":
                    self.CreateNodeWithColor(grid, [x,y], pixel_found, pixel_value, pos_already_visited)
                node = Node(pixel_found) 
                self.nodes.append(node)
        print(pos_already_visited)


    # current_pos[0] -> x
    # current_pos[1] -> y
    # pixel found = position of pixels (local to this node)
    # pos alreay visited = position of pixels already visited (global au parcours de la grid)
    def CreateNodeWithColor(self, grid, current_pos, pixel_found, pixel_value, pos_already_visited):
         for y in range (-1, 2):
            for x in range (-1, 2):
                if (x == 0 and y == 0):
                    continue
                # position in grid
                pos_tested = (current_pos[0] + x, current_pos[1] + y)
                if ((pos_tested[0] < 0 or pos_tested[0] >= len(grid[0])) or (pos_tested[1] < 0 or pos_tested[1] >= len(grid))):
                    continue
                # value in grid
                actual_value = grid[pos_tested[1]][pos_tested[0]]
                if (actual_value == pixel_value and pos_tested not in pixel_found):
                    pixel_found.append(pos_tested)
                    pos_already_visited.append(pos_tested)
                    self.CreateNodeWithColor(grid, pos_tested, pixel_found, pos_already_visited)




    # current_pos[0] -> x
    # current_pos[1] -> y
    # pixel found = position of pixels (local to this node)
    # pos alreay visited = position of pixels already visited (global au parcours de la grid)
    def CreateNodeWithNeighbors(self, grid, current_pos, pixel_found, pos_already_visited):
        for y in range (-1, 2):
            for x in range (-1, 2):
                if (x == 0 and y == 0):
                    continue
                # position in grid
                pos_tested = (current_pos[0] + x, current_pos[1] + y)
                if ((pos_tested[0] < 0 or pos_tested[0] >= len(grid[0])) or (pos_tested[1] < 0 or pos_tested[1] >= len(grid))):
                    continue
                # value in grid
                actual_value = grid[pos_tested[1]][pos_tested[0]]
                if (actual_value != 0 and pos_tested not in pixel_found):
                    pixel_found.append(pos_tested)
                    pos_already_visited.append(pos_tested)
                    self.CreateNodeWithNeighbors(grid, pos_tested, pixel_found, pos_already_visited)

    def CreateNodeHorizontaly(self, grid):
        pass

    def CreateNodeVertically(self, grid):
        pass

    def CreateEdges(self, grid):

        pixels_associated = {}
        for node in self.nodes:
            pixels = node.GetPixelPositions()
            for pos in pixels:
                pixels_associated[pos] = node


        i = 0
        for node in self.nodes:
            i += 1
            if i == 2:
                print("")
            pixels = node.GetPixelPositions()
            for pos in pixels:
                for x in range (pos[0], len(grid[0])):
                    pos_tested = (x, pos[1])
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested])
                            break 
                for x in range (pos[0], -1, -1):
                    pos_tested = (x, pos[1])
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested])
                            break
                for y in range (pos[1], len(grid)):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested])
                            break
                for y in range (pos[1], -1, -1):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested])
                            break
        print(self.nodes)


    def build_graph_from_list(self, nodes):
        G = nx.Graph()
        seen = set()

        for node in nodes:
            if node not in seen:
                G.add_node(node, color=node.color)
                seen.add(node)
            for neighbor in node.associated_nodes:
                G.add_node(neighbor, color=neighbor.color)
                G.add_edge(node, neighbor)
        return G

    def ShowGraph(self):
        graph = self.build_graph_from_list(self.nodes)
        pos = nx.spring_layout(graph)
        node_colors = [data['color'] for _, data in graph.nodes(data=True)]

        nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color="gray",
                node_size=1000, font_size=12)
        plt.show()




grille = [
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 0, 0, 1],
    [0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1],
]

graph = Graph(grille)
graph.ShowGraph()
input = ("wait")