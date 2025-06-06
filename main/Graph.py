from Nodes import Node
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib import colors
from collections import defaultdict

class Graph:

    def __init__(self, grid):
        self.nodes = []
        self.grid = grid
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
                pixel_color_found = {}
                pixel_value = grid[y][x]
                # if we find a new node, we are going to find all pixels associated based on type of search
                # the functions are recursive. 
                #note: pixel_found passed through REFERENCE (no return to the fonctions)
                if type == "NEIGHBOR":
                    pixel_color_found[(x,y)] = pixel_value
                    self.CreateNodeWithNeighbors(grid, [x,y], pixel_found, pixel_color_found, pos_already_visited)
                elif type == "COLOR":
                    self.CreateNodeWithColor(grid, [x,y], pixel_found, pixel_value, pos_already_visited)
                # end of the search, we add the pixels to the node created
                node = Node(pixel_found, pixel_color_found) 
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
    # pixel color found = value of pixel (local to this node)
    # pos alreay visited = position of pixels already visited (global au parcours de la grid)
    # SAME AS CreateNodeWithColor,check for this function for more comments
    def CreateNodeWithNeighbors(self, grid, current_pos, pixel_found, pixel_color_found, pos_already_visited):
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
                    # we add the color of pixel (key=pos value=color)
                    pixel_color_found[pos_tested] = actual_value
                    pos_already_visited.append(pos_tested)
                    # recursive call to check position
                    self.CreateNodeWithNeighbors(grid, pos_tested, pixel_found, pixel_color_found, pos_already_visited)

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
                            node.AddAssociatedNode(pixels_associated[pos_tested], "HORIZONTAL")
                            break 
                
                # LEFT DIRECTION
                for x in range (pos[0], -1, -1):
                    pos_tested = (x, pos[1])
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested], "HORIZONTAL")
                            break

                # DOWN DIRECTION        
                for y in range (pos[1], len(grid)):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested], "VERTICAL")
                            break

                # UP DIRECTION        
                for y in range (pos[1], -1, -1):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            node.AddAssociatedNode(pixels_associated[pos_tested], "VERTICAL")
                            break
        print(self.nodes)



    def GetNodePositions(self):
        max_y = max(node.GetApproximatePixelPos()[1] for node in self.nodes)
        return {node: (node.GetApproximatePixelPos()[0], max_y - node.GetApproximatePixelPos()[1]) for node in self.nodes}




    # function to create the graphical graph
    def BuildGraphFromList(self, nodes):
        G = nx.Graph()

        for node in nodes:
            G.add_node(node, color=node.color, size=node.size)

            for neighbor, direction in node.associated_nodes:
                G.add_node(neighbor, color=neighbor.color, size=neighbor.size)
                G.add_edge(node, neighbor, label=direction)
        
        return G


    # function to display graph
    def ShowGraph(self):
        graph = self.BuildGraphFromList(self.nodes)
        pos = self.GetNodePositions()

        node_colors = [data.get('color') or 'gray' for _, data in graph.nodes(data=True)]
        labels = {node: data['size'] for node, data in graph.nodes(data=True)}
        edge_labels = {(u, v): data['label'] for u, v, data in graph.edges(data=True)}
    
        nx.draw(graph, pos, labels=labels, node_color=node_colors, node_size=1000, font_size=12)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='gray')

        #plt.gca().invert_xaxis()
        #plt.gca().invert_yaxis()
        
        plt.axis('equal')  # respect des proportions
        plt.show()


    def ShowGrid(self):
        array = np.array(self.grid)
        rows, cols = array.shape

        cmap = colors.ListedColormap(['black', 'red', 'green', 'blue', 'orange', 'purple'])
        bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        fig, ax = plt.subplots(figsize=(cols, rows))
        im = ax.imshow(array, cmap=cmap, norm=norm)

        # Ticks exactement sur les bords des cellules
        ax.set_xticks(np.arange(cols))
        ax.set_yticks(np.arange(rows))

        # Affichage des labels
        ax.set_xticklabels(np.arange(cols))
        ax.set_yticklabels(np.arange(rows))

        # Grille aux bonnes positions
        ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)

        # Réglages visuels
        ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
        ax.invert_yaxis()
        ax.set_aspect('equal')

        plt.show()




    ##### UTILITARIES (COMPARE BETWEEN TWO GRAPHS) #######

    @staticmethod
    def CompareTwoNodesPosition(grid_input, grid_output, node_input, node_output):
        pass

    @staticmethod
    def CompareTwoNodesColor(grid_input, grid_output, node_input, node_output):
        pass

    @staticmethod
    def CompareTwoNodesSize(grid_input, grid_output, node_input, node_output):
        pass

    @staticmethod
    def CompareGridSize(grid_input, grid_output):
        pass

    @staticmethod
    def CheckNodeOnOutput(grid_input, grid_output, node_input):
        pass

    @staticmethod
    def CheckNodeSizeOnOutput(grid_input, grid_output):
        pass



    
    def HasDuplicateShapes(self):
        shape_groups = defaultdict(list)  # Maps normalized shape → list of nodes with that shape

        for node in self.nodes:
            # Get all normalized rotations of this node
            rotated_shapes = node.GetNormalizedRotations()

            matched = False
            # Compare against all known shape keys
            for key_shape in shape_groups.keys():
                if any(rot == list(key_shape) for rot in rotated_shapes):
                    shape_groups[key_shape].append(node)
                    matched = True
                    break

            if not matched:
                # First time we see this shape, store the first rotation as key
                shape_groups[tuple(rotated_shapes[0])] = [node]

        # Extract groups that contain repeated shapes
        repeated_groups = [group for group in shape_groups.values() if len(group) > 1]

        print(f"Number of repeated shape groups: {len(repeated_groups)}")
        for group in repeated_groups:
            print(f"Shape occurs {len(group)} times:")
            for node in group:
                print(f" - {node.GetPixelPositions()}")

        return len(repeated_groups) > 0


grille = [
    [0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1],
    [0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 1, 0, 0, 0],
]

graph = Graph(grille)
for node in graph.nodes:
    print('yes = ', node.CheckUniColor()) 
#graph.ShowGrid()
graph.ShowGraph()