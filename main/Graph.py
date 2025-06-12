from Nodes import Node
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib import colors
from collections import defaultdict
from matplotlib import colors

class Graph:

    def __init__(self, grid):
        self.nodes = []
        self.grid = grid
        # first, we create the nodes (by giving the type of graph construction)
        self.CreateNode(grid, 'NEIGHBOR')
        #then, we create the edges of the graph
        self.CreateEdges(grid)
        # print(self.HasDuplicateShapes())


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
                            diff = x - pos[0]
                            # we associate current node to the node found
                            node.AddAssociatedNode(pixels_associated[pos_tested], "HORIZONTAL", diff)
                            break 
                
                # LEFT DIRECTION
                for x in range (pos[0], -1, -1):
                    pos_tested = (x, pos[1])
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            diff = pos[0] - x
                            node.AddAssociatedNode(pixels_associated[pos_tested], "HORIZONTAL", diff)
                            break

                # DOWN DIRECTION        
                for y in range (pos[1], len(grid)):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            diff = y - pos[1]
                            node.AddAssociatedNode(pixels_associated[pos_tested], "VERTICAL", diff)
                            break

                # UP DIRECTION        
                for y in range (pos[1], -1, -1):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            diff = pos[1] - y
                            node.AddAssociatedNode(pixels_associated[pos_tested], "VERTICAL", diff)
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

        # Ajouter une grille optionnelle
        plt.grid(which='both', color='gray', linewidth=0.5)
        plt.xticks(np.arange(len(self.grid[0])))
        plt.yticks(np.arange(len(self.grid)))
        plt.gca().invert_yaxis()  # pour garder (0,0) en haut à gauche
        plt.gca().set_aspect('equal')
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


    ##### GETTER / SETTER ######

    # get grid size
    # TODO: return x len and y len
    def GetGridSize(self):
        return len(self.grid)

    # TODO
    def GetNumberNodes(self):
        return len(self.nodes)

    # get nodes
    def GetNodes(self):
        return self.nodes


    ##### UTILITARIES (COMPARE BETWEEN TWO GRAPHS) #######


    # return same as CompareNodeBetweenGraphs if node is in the graph_output
    @staticmethod
    def CompareNodeBetweenGraphs(node, graph):
        base_rot1 = node.GetNormalizedRotations()[0]  # forme de base
        match_list = []

        for node2 in graph.nodes:
            node2_rotations = node2.GetNormalizedRotations()

            for j, rot2 in enumerate(node2_rotations):
                if rot2 == base_rot1:
                    rotation_angle = j * 90  # Combien node2 doit tourner pour devenir node1
                    match_list.append((node2, rotation_angle))
                    break  # stop at first match for this node2

        return {
            "matches": match_list,
            "match_count": len(match_list),
        }
    

    @staticmethod
    def IsNodeRepeatingLargest(node, graph):
        match_count = Graph.CompareNodeBetweenGraphs(node, graph)['match_count']
        for node1 in graph.nodes:
            if node1 == node:
                continue
            current_count = Graph.CompareNodeBetweenGraphs(node1, graph)['match_count']
            if match_count < current_count:
                return False
        return True
    
    @staticmethod
    def IsNodeRepeatingLowest(node, graph):
        match_count = Graph.CompareNodeBetweenGraphs(node, graph)['match_count']
        for node1 in graph.nodes:
            if node1 == node:
                continue
            current_count = Graph.CompareNodeBetweenGraphs(node1, graph)['match_count']
            if match_count > current_count:
                return False
        return True

    @staticmethod
    def CompareNodesBetweenGraphs(graph1, graph2):
        results = []

        for node1 in graph1.nodes:
            base_rot1 = node1.GetNormalizedRotations()[0]  # forme de base
            match_list = []

            for node2 in graph2.nodes:
                node2_rotations = node2.GetNormalizedRotations()

                for j, rot2 in enumerate(node2_rotations):
                    if rot2 == base_rot1:
                        rotation_angle = j * 90  # Combien node2 doit tourner pour devenir node1
                        match_list.append((node2, rotation_angle))
                        break  # stop at first match for this node2

            results.append({
                "node_input": node1,
                "matches": match_list,
                "match_count": len(match_list)
            })

        return results


    # TODO check if sequence in other graph 
    @staticmethod
    def CompareNodeSequenceBetweenGraphs(node, output_graph):
        pass

    # check if the two nodes are at same place (note: node input and output have the same pixel pos structure)
    # TODO: DO NOT APPLY TO ROTATED structures
    #returns: [x, y] => offset of the nodes ex: [2, 3] => output node is 2 on X axis and 3 on y axis compared to original
    @staticmethod
    def CompareTwoNodesPosition(input_graph, output_graph, node_input, node_output):
        first_pixel_input = node_input.GetPixelPositions()[0]
        first_pixel_output = node_output.GetPixelPositions()[0]

        return (first_pixel_output[0] - first_pixel_input[0], first_pixel_output[1], first_pixel_input[1])

    # TODO check if two nodes have same color
    @staticmethod
    def CompareTwoNodesColor(input_graph, output_graph, node_input, node_output):
        pass
    
    # TODO check number of pixels of two nodes
    @staticmethod
    def CompareTwoNodesSize(input_graph, output_graph, node_input, node_output):
        pass

    # TODO check if node extend to another node
    @staticmethod
    def CompareNodeExtended(input_graph, output_graph, node_input):
        pass

    # @staticmethod
    # def CompareGridSize(grid_input, grid_output):
    #     pass

    # @staticmethod
    # def CheckNodeOnOutput(grid_input, grid_output, node_input):
    #     pass



# grille = [
#     [0, 0, 0, 0, 0, 1],
#     [1, 1, 1, 0, 1, 1],
#     [0, 1, 0, 0, 0, 1],
#     [0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 0, 0],
#     [0, 0, 1, 0, 0, 1],
# ]
# startTime = datetime.now()
# graph = Graph(grille)
# for node in graph.nodes:
#     print('yes = ', node.CheckUniColor()) 
# print(datetime.now() - startTime)
# graph.ShowGrid()


# grid1 = [
#     [9, 6, 5, 6, 9, 5, 3, 3, 5, 9, 6, 5, 6, 9, 5, 3, 3, 5, 9, 6, 5],
#     [6, 3, 2, 3, 6, 2, 9, 9, 2, 0, 0, 0, 0, 0, 2, 9, 9, 2, 6, 3, 2],
#     [5, 2, 1, 2, 5, 1, 8, 8, 1, 0, 0, 0, 0, 0, 1, 8, 8, 1, 5, 2, 1],
#     [6, 3, 2, 3, 6, 2, 9, 9, 2, 0, 0, 0, 0, 0, 2, 9, 9, 2, 6, 3, 2],
#     [9, 6, 5, 6, 9, 5, 3, 3, 5, 9, 6, 5, 6, 9, 5, 3, 3, 5, 9, 6, 5],
#     [5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1],
#     [3, 9, 8, 9, 3, 8, 6, 6, 8, 3, 9, 8, 9, 3, 8, 6, 6, 8, 3, 9, 8],
#     [3, 9, 8, 9, 3, 8, 6, 6, 8, 3, 9, 8, 9, 3, 8, 6, 6, 8, 3, 9, 8],
#     [5, 2, 1, 2, 0, 0, 0, 0, 1, 5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1],
#     [9, 6, 5, 6, 0, 0, 0, 0, 5, 9, 6, 5, 6, 9, 5, 3, 3, 5, 9, 6, 5],
#     [6, 3, 2, 3, 0, 0, 0, 0, 2, 6, 3, 2, 3, 6, 2, 9, 9, 2, 6, 3, 2],
#     [5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1],
#     [6, 3, 2, 3, 6, 2, 9, 9, 2, 6, 3, 2, 3, 6, 0, 0, 9, 2, 6, 3, 2],
#     [9, 6, 5, 6, 9, 5, 3, 3, 5, 9, 6, 5, 6, 9, 0, 0, 3, 5, 9, 6, 5],
#     [5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1, 2, 5, 0, 0, 8, 1, 5, 2, 1],
#     [0, 0, 8, 9, 0, 0, 0, 6, 8, 3, 9, 8, 9, 3, 0, 0, 6, 8, 3, 9, 8],
#     [0, 0, 8, 9, 0, 0, 0, 6, 8, 3, 9, 8, 9, 3, 8, 6, 6, 8, 3, 9, 8],
#     [5, 2, 1, 2, 0, 0, 0, 8, 1, 5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1],
#     [9, 6, 5, 6, 0, 0, 0, 3, 5, 9, 6, 5, 6, 9, 5, 3, 3, 5, 9, 6, 5],
#     [6, 3, 2, 3, 0, 0, 0, 9, 2, 6, 3, 2, 3, 6, 2, 9, 9, 2, 6, 3, 2],
#     [5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1, 2, 5, 1, 8, 8, 1, 5, 2, 1],
# ]

# graph = Graph(grid1)
# groups = graph.FindNodesWithSameInternalPattern(2)

# for i, group in enumerate(groups):
#     print(f"\nPattern {i+1} trouvé dans {len(group)} nœuds :")
#     for node in group:
#         print(f" → Pixels: {sorted(node.GetPixelPositions())}")
#         print(f" → Sous-pattern (valeurs = 2) : {sorted(node.ExtractSubPatternPositions(2))}")

# grid1 = [
#     [1, 0, 0, 0, 0],
#     [0, 0, 0, 2, 0],
#     [0, 0, 2, 2, 0],
#     [1, 0, 0, 2, 0],
#     [1, 1, 0, 0, 0],
# ]

# grid2 = [
#     [0, 0, 0, 0, 0],
#     [2, 0, 0, 0, 1],
#     [2, 2, 0, 0, 0],
#     [2, 0, 0, 0, 1],
#     [0, 0, 0, 1, 1],
# ]

# g1 = Graph(grid1)
# g2 = Graph(grid2)

# print("Résultat de comparaison entre les deux graphes:")
# results = Graph.CompareNodesBetweenGraphs(g1, g2)

# for result in results:
#     node1_pixels = sorted(result['node_input'].GetPixelPositions())
#     print(f"\n→ Node in Graph 1: {node1_pixels}")
#     print(f"Matches found: {result['match_count']}")
#     for matched_node, rotation in result["matches"]:
#         print(f"  Match with: {sorted(matched_node.GetPixelPositions())} — rotation: {rotation}°")




