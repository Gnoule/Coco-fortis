from Nodes import Node
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib import colors
from collections import defaultdict
from matplotlib import colors
import json
import copy
from math import sqrt
from collections import deque

class Graph:

    def __init__(self, grid, graph_type="COLOR"):
        self.nodes = []
        self.grid = grid
        # first, we create the nodes (by giving the type of graph construction)
        self.CreateNode(grid, graph_type)
        #then, we create the edges of the graph
        self.CreateEdges(grid)
        # we then check special properties
        self.CheckProperties()
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
                    node = Node(pixel_found, pixel_color_found, name=len(self.nodes)) 
                elif type == "COLOR":
                    self.CreateNodeWithColor(grid, [x,y], pixel_found, pixel_value, pos_already_visited)
                    node = Node(pixel_found, color=pixel_value, name=len(self.nodes)) 
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
            index_pos = -1
            for pos in pixels:
                index_pos += 1
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
                            node.AddAssociatedNode(index_pos, pixels_associated[pos_tested], "HORIZONTAL", [diff, 0])
                            break 
                
                # LEFT DIRECTION
                for x in range (pos[0], -1, -1):
                    pos_tested = (x, pos[1])
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            diff = pos[0] - x
                            node.AddAssociatedNode(index_pos, pixels_associated[pos_tested], "HORIZONTAL", [-diff, 0])
                            break

                # DOWN DIRECTION        
                for y in range (pos[1], len(grid)):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            diff = y - pos[1]
                            node.AddAssociatedNode(index_pos, pixels_associated[pos_tested], "VERTICAL", [0, diff])
                            break

                # UP DIRECTION        
                for y in range (pos[1], -1, -1):
                    pos_tested = (pos[0], y)
                    if (grid[pos_tested[1]][pos_tested[0]] != 0 and pos_tested not in pixels):
                        if pos_tested in pixels_associated:
                            diff = pos[1] - y
                            node.AddAssociatedNode(index_pos, pixels_associated[pos_tested], "VERTICAL", [0, -diff])
                            break
        print(self.nodes)



    def node_signature(self, nodes):
        return tuple(sorted(id(n) for n in nodes))


    def CheckProperties(self):
        centered = []
        all_visited = []
        for node in self.nodes:
            if node in all_visited:
                continue
            association = node.GetAssociatedNode()
            result, path = self.CheckGroup(node, association, [], all_visited)
            if result:
                path.append(node)
                min_x_found = path[0].GetPixelPositions()[0][0]
                max_x_found = path[0].GetPixelPositions()[0][0]
                min_y_found = path[0].GetPixelPositions()[0][1]
                max_y_found = path[0].GetPixelPositions()[0][1]
                for n in path:
                    all_visited.append(n)
                    for pos in n.GetPixelPositions():
                        if pos[0] < min_x_found:
                            min_x_found = pos[0]
                        if pos[1] < min_y_found:
                            min_y_found = pos[1]
                        if pos[0] > max_x_found:
                            max_x_found = pos[0]
                        if pos[1] > max_y_found:
                            max_y_found = pos[1]
                        
                print("for node =", node, "FOUND CENTERED !!!", path)
                centered.append({
                    "position": {
                        "min_x_found": min_x_found,
                        "min_y_found": min_y_found,
                        "max_x_found": max_x_found,
                        "max_y_found": max_y_found,
                    },
                    "nodes": path
                })

        for center in centered:
            all_node_found = [] 
            for node in self.nodes:
                if node in center['nodes']:
                    continue
                found = True
                for pos in node.GetPixelPositions():
                        if (pos[0] < center["position"]["min_x_found"] or pos[0] > center["position"]["max_x_found"] 
                         or pos[1] < center["position"]["min_y_found"] or pos[1] > center["position"]["max_y_found"]):
                            found = False
                            break
                if found:
                    node.SetCenteredInNodes(True)
                    all_node_found.append(node)
                    print("success", node)   

            # we connect all found node together 
            for node_found in all_node_found:
                for next_found in all_node_found:
                    delta_x = (next_found.GetPixelPositions()[0][0] - node_found.GetPixelPositions()[0][0]) 
                    delta_y = (next_found.GetPixelPositions()[0][1] - node_found.GetPixelPositions()[0][1])
                    dist = sqrt(delta_x**2 + delta_y**2)
                    if delta_x > 0 and delta_y > 0:
                        node_found.AddAssociatedNode(0, next_found, "DIAGONALE", [delta_x, delta_y])   

    
    def CheckGroup(self, origin_node, associations, path, global_visited):
        for association in associations:
            node = association[1]
            if node in path or node in global_visited:
                continue
            new_path = []
            for i in path:
                new_path.append(i)
            if node == origin_node and len(new_path) > 1:
                return (True, new_path)
            elif node != origin_node:
                new_path.append(node)
            elif node == origin_node and len(new_path) <= 1:
                continue
            
            next_associations = node.GetAssociatedNode()
            result, found_path = self.CheckGroup(origin_node, next_associations, new_path, global_visited)
            if result:
                return (True, found_path)
        return (False, None)


            


    def GetNodePositions(self):
        max_y = max(node.GetApproximatePixelPos()[1] for node in self.nodes)
        return {node: (node.GetApproximatePixelPos()[0], max_y - node.GetApproximatePixelPos()[1]) for node in self.nodes}



    # function to create the graphical graph
    def BuildGraphFromList(self, nodes):
        G = nx.Graph()

        for node in nodes:
            G.add_node(node, color=node.color, size=node.size)

            for neighbor, direction, dist in node.associated_nodes:
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
        cmap = colors.ListedColormap(['black', 'red', 'green', 'blue', 'orange', 'purple', 'yellow', 'cyan', 'grey', 'brown', 'pink'])
        bounds = np.arange(-0.5, 11.5, 1)
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
        # grouped_nodes = {k: v for k, v in grouped_nodes.items() if len(v) > 1}

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
    
    def SetNewGrid(self, new_grid):
        self.grid = new_grid

    def CheckIfPosEmpty(self, x, y):
        if x >= len(self.grid[0]) or x < 0 or y >= len(self.grid) or y < 0:
            return True
        if self.grid[y][x] == 0:
            return True
        return False

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
    def CompareConnectionsBetweenGraphs(input_node, output_node, output_graph):
        if len(input_node.GetAssociatedNode()) == 0:
            return False
        for connection_input in input_node.GetAssociatedNode():
            dir = connection_input[2] 
            diff = connection_input[3]
            size = connection_input[1].GetSize()
            current_x = output_node.GetPixelPositions()[connection_input[0]][0] + diff[0]
            current_y = output_node.GetPixelPositions()[connection_input[0]][1] + diff[1]
            if output_graph.CheckIfPosEmpty(current_x, current_y):
                return False
                
        return True
            
        #     for connection_output in output_node.GetAssociatedNode():
        #         # if true, the connected node is "probably" the same than input
        #         if (connection_output[1] == dir and 
        #         connection_output[0].GetSize() == size and 
        #         connection_output[2] == diff):
        #             found = True
        #             break
        #     if not found:
        #         return False
        # return True
        
        


    
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
    def FindMatchingNodes(start_node, graph_instance):
        matching_nodes = []
        start_colors = set(start_node.GetAllColor())

        for node in graph_instance.GetNodes():
            if node is start_node:
                continue

            node_colors = set(node.GetAllColor())

            if node.GetSize() > 1 and start_colors.intersection(node_colors):
                matching_nodes.append(node)

        return matching_nodes
    
    @staticmethod
    def get_node_by_position(position, nodes):
        for node in nodes:
            if position in node.GetPixelPositions():
                return node
        return None
    

    @staticmethod
    def findPattern(start_node, graph_instance):

        print("--------------start of findPattern--------------")

        if not start_node:
            raise ValueError("Need a node to start")
        
        work_node = [start_node] + Graph.FindMatchingNodes(start_node, graph_instance)

        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }

        taboo = set()
        used_nodes = set()
        result = []

        n1 = work_node[0]
        pos1_position = n1.GetPixelPositions()[0]
        pos1_color = n1.GetPixelColor()[pos1_position]
        print("color", pos1_color, "position", pos1_position)

        for i in range (len(work_node)-1):
            for j in range(work_node[i+1].GetSize()):
                n2 = work_node[i+1]
                pos2_position = n2.GetPixelPositions()[j]
                pos2_color = n2.GetPixelColor()[pos2_position]
                # print("couleur de la positon2", pos2_color, "Emplacement de la position2", pos2_position)
                if pos1_color == pos2_color:
                    for _, (dx, dy) in directions.items():
                        neighbor_pos1 = (pos1_position[0] + dx, pos1_position[1] + dy)
                        neighbor_pos2 = (pos2_position[0] + dx, pos2_position[1] + dy)
                        if (neighbor_pos1, neighbor_pos2) in taboo or (neighbor_pos2, neighbor_pos1) in taboo:
                            continue    

                        node_voisin_1 = Graph.get_node_by_position(neighbor_pos1, work_node)
                        node_voisin_2 = Graph.get_node_by_position(neighbor_pos2, work_node)

                        if node_voisin_1 and node_voisin_2:

                            node_voisin1_color = node_voisin_1.GetPixelColor()[neighbor_pos1]
                            node_voisin2_color = node_voisin_2.GetPixelColor()[neighbor_pos2]

                            if node_voisin1_color == node_voisin2_color:
                                if n1 in used_nodes or n2 in used_nodes:
                                    continue
                                result.append([[n1, neighbor_pos1], [n2, neighbor_pos2]])
                                used_nodes.update([n1, n2])
                            else:
                                taboo.add((neighbor_pos1, neighbor_pos2))
                        else:
                            taboo.add((neighbor_pos1, neighbor_pos2))
            while True:
                break

        Graph.pretty_print_result(result)
        return False
    
    @staticmethod
    def FindPatternOneNode(start_node, graph_instance):
        if not start_node:
            raise ValueError("Need a node to start")

        work_section = [start_node] + Graph.FindMatchingNodes(start_node, graph_instance)
        print(work_section)
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
                involved_inputs = [node_input]

                # Check if it also contains pixels from other input nodes
                for other_node in input_graph.GetNodes():
                    if other_node == node_input:
                        continue
                    other_pixels = set(other_node.GetPixelPositions())
                    if other_pixels & output_pixels:
                        involved_inputs.append(other_node)

                if len(involved_inputs) > 1:
                    return involved_inputs, node_out  # Return all involved nodes and merged output node

        return None, None
    

    @staticmethod
    def extract_shapes_with_value(grid):

        visited = [[False] * len(row) for row in grid]
        shapes = []

        def bfs(y, x, value):
            queue = deque([(y, x)])
            coords = []

            while queue:
                cy, cx = queue.popleft()
                if (0 <= cy < len(grid) and
                    0 <= cx < len(grid[cy]) and
                    not visited[cy][cx] and
                    grid[cy][cx] == value):
                    visited[cy][cx] = True
                    coords.append((cy, cx))
                    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                        queue.append((cy + dy, cx + dx))
            return coords

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if not visited[y][x]:
                    val = grid[y][x]
                    shape_coords = bfs(y, x, val)
                    if len(shape_coords) > 1:
                        min_y = min(c[0] for c in shape_coords)
                        min_x = min(c[1] for c in shape_coords)
                        normalized = sorted([(cy - min_y, cx - min_x) for cy, cx in shape_coords])
                        shapes.append((val, normalized))
        return shapes


    @staticmethod
    def CompareFinalGrid(first_grid, second_grid):
        shapes1 = Graph.extract_shapes_with_value(first_grid)
        shapes2 = Graph.extract_shapes_with_value(second_grid)
        matched = [False] * len(shapes2)

        full_matches = 0
        partial_matches = 0

        for val1, form1 in shapes1:
            found = False
            for i, (val2, form2) in enumerate(shapes2):
                if not matched[i] and form1 == form2:
                    matched[i] = True
                    found = True
                    if val1 == val2:
                        full_matches += 1
                    else:
                        partial_matches += 1
                    break
            # Si pas trouvé : 0 point

        total = len(shapes1)
        if total == 0:
            return 0 if len(shapes2) > 0 else 100

        score = ((full_matches * 1.0) + (partial_matches * 0.7)) / total * 100
        return round(score, 2)

    


    









    #### FUNCTION POUR MODIFIER LE GRAPH APRES COUP ####


    def RebuildGridAndGraph(self):
        pass

    def DeactivateNode(self, node):
        node.DeactivateNode()
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


    def ResizeGrid(self, size_x, size_y):
        new_grid = []
        for y in range (size_y):
            grid_inter = []
            for x in range (size_x):
                grid_inter.append(self.grid[y][x])
            new_grid.append(grid_inter)
        self.grid = new_grid

    def ResizeGridOnNodes(self):
        max_x_found = self.nodes[0].GetPixelPositions()[0][0]
        max_y_found = self.nodes[0].GetPixelPositions()[0][1]
        for node in self.nodes:
            if node.GetActiveStatus() == False:
                continue
            for pos in node.GetPixelPositions():
                if pos[0] > max_x_found:
                    max_x_found = pos[0]
                if pos[1] > max_y_found:
                    max_y_found = pos[0]
        return max_x_found+1, max_y_found

