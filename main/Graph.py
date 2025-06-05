from Nodes import Node
import networkx as nx
import matplotlib.pyplot as plt
import math

class Graph:

    def __init__(self, grid):
        self.nodes = []
        # first, we create the nodes (by giving the type of graph construction)
        self.CreateNode(grid, 'NEIGHBOR')
        #then, we create the edges of the graph
        self.CreateEdges(grid)
        print(self.HasDuplicateShapes())


    # function to create the nodes of the graph (not the edges)
    # grid = 2D Array of the grid (input) giving example : [[0,0,0],[1,0,0]]
    # type = type of contruction for graph
    def CreateNode(self, grid, type="NEIGHBOR"):
        # global list to stock all visited position
        pos_already_visited = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                # if already visited or is nothing (0)
                if ((x,y) in pos_already_visited or (grid[y][x] == 0)):
                    continue
                pixel_found = [(x,y)]
                pixel_value = [(x,y)]
                # if we find a new node, we are going to find all pixels associated based on type of search
                # the functions are recursive. 
                #note: pixel_found passed through REFERENCE (no return to the fonctions)
                if type == "NEIGHBOR":
                    self.CreateNodeWithNeighbors(grid, [x,y], pixel_found, pos_already_visited)
                elif type == "COLOR":
                    self.CreateNodeWithColor(grid, [x,y], pixel_found, pixel_value, pos_already_visited)
                # end of the search, we add the pixels to the node created
                node = Node(pixel_found) 
                self.nodes.append(node)
        print(pos_already_visited)


    # current_pos[0] -> x
    # current_pos[1] -> y
    # pixel found = position of pixels (local to this node)
    # pos alreay visited = position of pixels already visited (global to the search) VALUE OF RETURN, PASSED THROUGH REFERENCE
    # pixel_value = color of first nodes
    def CreateNodeWithColor(self, grid, current_pos, pixel_found, pixel_value, pos_already_visited):
         # double for, checking around the current pixel
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

                # if value is a new value 
                if (actual_value == pixel_value and pos_tested not in pixel_found):
                    # we add to pixel_found (passed throug hreference)
                    pixel_found.append(pos_tested)
                    pos_already_visited.append(pos_tested)
                    # recursive call to check position
                    self.CreateNodeWithColor(grid, pos_tested, pixel_found, pos_already_visited)


    # current_pos[0] -> x
    # current_pos[1] -> y
    # pixel found = position of pixels (local to this node)
    # pos alreay visited = position of pixels already visited (global au parcours de la grid)
    # SAME AS CreateNodeWithColor,check for this function for more comments
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

                # if value is a new value 
                if (actual_value != 0 and pos_tested not in pixel_found):
                    # we add to pixel_found (passed throug hreference)
                    pixel_found.append(pos_tested)
                    pos_already_visited.append(pos_tested)
                    # recursive call to check position
                    self.CreateNodeWithNeighbors(grid, pos_tested, pixel_found, pos_already_visited)

    def CreateNodeHorizontaly(self, grid):
        pass

    def CreateNodeVertically(self, grid):
        pass

    # function to create the edges
    # grid = input grid
    def CreateEdges(self, grid):

        # 1 : dictionnary (key=>value) with key = position and value=node associated for this pixel position
        # useful for the search 
        pixels_associated = {}
        for node in self.nodes:
            pixels = node.GetPixelPositions()
            for pos in pixels:
                pixels_associated[pos] = node


        # foreach node
        for node in self.nodes:
            # get all pixel for this node
            pixels = node.GetPixelPositions()
            for pos in pixels:

                # we do 4 for: in for left, right, up, down
                # we will check in all direction if there is a pixel, if yes, we check for the associated node (with pixels_associated)

                # RIGHT DIRECTION
                for x in range (pos[0], len(grid[0])):
                    pos_tested = (x, pos[1])
                    # if there is a node 
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            # we associate current node to the node found
                            node.AddAssociatedNode(pixels_associated[pos_tested])
                            break 
                
                # LEFT DIRECTION
                for x in range (pos[0], -1, -1):
                    pos_tested = (x, pos[1])
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested])
                            break

                # DOWN DIRECTION        
                for y in range (pos[1], len(grid)):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested])
                            break

                # UP DIRECTION        
                for y in range (pos[1], -1, -1):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested])
                            break
        print(self.nodes)


    # function to create the graphical graph
    def BuildGraphFromList(self, nodes):
        G = nx.Graph()
        seen = set()

        # foreach node, we add it to the nx graph type
        for node in nodes:
            if node not in seen:
                G.add_node(node, color=node.color)
                seen.add(node)
            for neighbor in node.associated_nodes:
                G.add_node(neighbor, color=neighbor.color)
                G.add_edge(node, neighbor)
        return G

    # function to display graph
    def ShowGraph(self):
        # create graphical graph
        graph = self.BuildGraphFromList(self.nodes)
        pos = nx.spring_layout(graph)
        node_colors = [data['color'] for _, data in graph.nodes(data=True)]

        # draw graph
        nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color="gray",
                node_size=1000, font_size=12)
        plt.show()

    def HasDuplicateShapes(self):

        def normalize(pixels):
            # Center around (0,0) and sort
            min_x = min(p[0] for p in pixels)
            min_y = min(p[1] for p in pixels)
            return sorted([(x - min_x, y - min_y) for x, y in pixels])

        def get_rotated_forms(node):
            rotations = []
            original = node.GetPixelPositions()
            x_sum = sum(p[0] for p in original)
            y_sum = sum(p[1] for p in original)
            n = len(original)
            center = (x_sum / n, y_sum / n)

            for i in range(4):
                angle = i * (math.pi / 2)  # 0, 90, 180, 270
                rotated = [Node.Rotate(center, p, angle) for p in original]
                rotations.append(normalize(rotated))
            return rotations

        normalized_nodes = []

        for node in self.nodes:
            rotated_shapes = get_rotated_forms(node)

            for other_shapes in normalized_nodes:
                if any(shape in other_shapes for shape in rotated_shapes):
                    return True  # Duplicate found

            normalized_nodes.append(rotated_shapes)

        return False






grille = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0],
    [1, 0, 0, 0, 1],
    [0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1],
]

graph = Graph(grille)
graph.ShowGraph()
input = ("wait")