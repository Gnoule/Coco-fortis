from Nodes import Node
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib import colors
from collections import defaultdict
from matplotlib import colors
import json

class Graph:

    def __init__(self, grid):
        self.nodes = []
        self.grid = grid
        # first, we create the nodes (by giving the type of graph construction)
        self.CreateNode(grid, 'NEIGHBOR')
        #then, we create the edges of the graph
        self.CreateEdges(grid)
        # print(self.HasDuplicateShapes())
        self.active = True


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
                    node = Node(pixel_found, pixel_color_found) 
                elif type == "COLOR":
                    self.CreateNodeWithColor(grid, [x,y], pixel_found, pixel_value, pos_already_visited)
                    node = Node(pixel_found, color=pixel_value) 
                # end of the search, we add the pixels to the node created
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
                    self.CreateNodeWithColor(grid, pos_tested, pixel_found, pixel_value, pos_already_visited)


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

    def SortNodesByColorAndSize(self):
        grouped_nodes = defaultdict(list)

        for node in self.nodes:
            color = node.GetColor()
            size = node.GetSize()
            key = (color, size)
            grouped_nodes[key].append(node)

        # Keep only groups with more than one node
        grouped_nodes = {k: v for k, v in grouped_nodes.items() if len(v) > 1}

        # Sort by color (as string) and then by size
        sorted_keys = sorted(grouped_nodes.keys(), key=lambda k: (str(k[0]), k[1]))

        sorted_nodes = []
        for key in sorted_keys:
            sorted_nodes.extend(grouped_nodes[key])

        return sorted_nodes


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


    def IsNodeInCenter(self, node=None, pixel_pos=None):
        if node != None:
            max_min = Node.GetMinMaxPos(node.GetPixelPositions())
        if pixel_pos != None:
            max_min = Node.GetMinMaxPos(pixel_pos)
        
        
        dist_left = max_min['min_x']
        dist_right = len(self.grid[0]) - max_min['max_x'] - 1

        dist_up = max_min['min_y']
        dist_down = len(self.grid) - max_min['max_y'] - 1
        if dist_left == dist_right and dist_up == dist_down:
            return True
        return False



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
    def ExtractFirstRepeatedGroup(nodes):
        if not nodes:
            return []

        first_group = []
        first_key = (nodes[0].GetColor(), nodes[0].GetSize())

        for node in nodes:
            key = (node.GetColor(), node.GetSize())
            if key == first_key:
                first_group.append(node)
            else:
                break

        return first_group

    
    @staticmethod
    def FindPattern(start_node, graph_instance):
        # Access all nodes via the instance method
        sorted_nodes = graph_instance.SortNodesByColorAndSize()
        work_section = Graph.ExtractFirstRepeatedGroup(sorted_nodes)

        pos_to_node = {}
        for node in graph_instance.nodes:
            for pos in node.GetPixelPositions():
                pos_to_node[pos] = node

        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }

        taboo = set()
        result = []

        # Step 1: Pair initialization
        for i in range(len(work_section)):
            n1 = work_section[i]
            pos1 = n1.GetPixelPositions()[0]
            for j in range(i + 1, len(work_section)):
                n2 = work_section[j]
                pos2 = n2.GetPixelPositions()[0]
                if n1.GetColor() == n2.GetColor() and n1.GetSize() == n2.GetSize():
                    for _, (dx, dy) in directions.items():
                        neighbor_pos1 = (pos1[0] + dx, pos1[1] + dy)
                        neighbor_pos2 = (pos2[0] + dx, pos2[1] + dy)
                        if (neighbor_pos1, neighbor_pos2) in taboo or (neighbor_pos2, neighbor_pos1) in taboo:
                            continue
                        node_voisin_1 = pos_to_node.get(neighbor_pos1)
                        node_voisin_2 = pos_to_node.get(neighbor_pos2)
                        if node_voisin_1 and node_voisin_2:
                            if node_voisin_1.GetColor() == node_voisin_2.GetColor() and node_voisin_1.GetSize() == node_voisin_2.GetSize():
                                result.append([[n1, node_voisin_1], [n2, node_voisin_2]])
                            else:
                                taboo.add((neighbor_pos1, neighbor_pos2))
                        else:
                            taboo.add((neighbor_pos1, neighbor_pos2))

        # Step 2: Pattern growth to true stability
        while True:
            changed = False
            new_result = []

            for group in result:
                chain1, chain2 = group
                last1 = chain1[-1]
                last2 = chain2[-1]
                pos1 = last1.GetPixelPositions()[0]
                pos2 = last2.GetPixelPositions()[0]

                extended = False
                for _, (dx, dy) in directions.items():
                    n_pos1 = (pos1[0] + dx, pos1[1] + dy)
                    n_pos2 = (pos2[0] + dx, pos2[1] + dy)

                    if (n_pos1, n_pos2) in taboo or (n_pos2, n_pos1) in taboo:
                        continue

                    n1 = pos_to_node.get(n_pos1)
                    n2 = pos_to_node.get(n_pos2)

                    if n1 and n2:
                        if (n1.GetColor() == n2.GetColor() and
                            n1.GetSize() == n2.GetSize() and
                            n1 not in chain1 and n2 not in chain2):
                            new_result.append([chain1 + [n1], chain2 + [n2]])
                            changed = True
                            extended = True
                            break
                        else:
                            taboo.add((n_pos1, n_pos2))
                    else:
                        taboo.add((n_pos1, n_pos2))

                if not extended:
                    new_result.append(group)

            if not changed:
                break

            result = new_result

        # Export JSON with pattern length >= 3
        motifs_json = []
        for group in result:
            motif = []
            valid = True
            for chain in group:
                if len(chain) < 3:
                    valid = False
                    break
                chain_positions = [node.GetPixelPositions() for node in chain]
                motif.append(chain_positions)
            if valid:
                motifs_json.append(motif)

        json_result = {
            "total_motifs": len(motifs_json),
            "taboo_combinations": len(taboo),
            "patterns": motifs_json
        }

        with open("patterns.json", "w") as f:
            json.dump(json_result, f, indent=2)
        print("Pattern result saved to 'patterns.json'.")

        return json_result


    

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

    # check if two nodes have same color
    @staticmethod
    def CompareTwoNodesColor(graph_input, graph_output, node_input, node_output):
        color_input = node_input.GetColor()
        color_output = node_output.GetColor()
        return color_input == color_output

    
    #  check number of pixels of two nodes
    @staticmethod
    def CompareTwoNodesSize( node_input, node_output):
        color_input = node_input.GetSize()
        color_output = node_output.GetSize()
        return color_input == color_output
        

    @staticmethod
    def CompareNodeExtended(input_graph, output_graph, node_input):
        input_pixels = set(node_input.GetPixelPositions())

        for node_out in output_graph.GetNodes():
            output_pixels = set(node_out.GetPixelPositions())

            # Check if this output node contains all pixels of the input node
            if input_pixels.issubset(output_pixels):
                # Check if it also contains pixels from other input nodes
                extra_input_pixels = set()
                for other_node in input_graph.GetNodes():
                    if other_node == node_input:
                        continue
                    other_pixels = set(other_node.GetPixelPositions())
                    if other_pixels & output_pixels:
                        extra_input_pixels |= other_pixels

                # If there are additional pixels from other input nodes → it's a merge
                if extra_input_pixels:
                    return True

        return False
    









    #### FUNCTION POUR MODIFIER LE GRAPH APRES COUP ####


    def RebuildGridAndGraph(self):
        pass

    def DeactivateNode(self, node):
        #node.DeactivateNode()
        all_pos = node.GetPixelPositions()
        for pos in all_pos:
            self.grid[pos[1]][pos[0]] = 0

    def MoveNode(self, node, move_x, move_y):
        all_pos = node.GetPixelPositions()
        all_new_pos = []
        for pos in all_pos:
            new_pos = (pos[0] + move_x, pos[1] + move_y)
            all_new_pos.append(new_pos)
            self.grid[pos[1]][pos[0]] = 0
            self.grid[new_pos[1]][new_pos[0]] = 1
        node.SetPixelPositions(all_new_pos)

    def RecolorNode(self, node, color):
        all_pos = node.GetPixelPositions()
        for pos in all_pos:
            self.grid[pos[1]][pos[0]] = color