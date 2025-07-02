from pycsp3 import *
import os
from ConstraintFinder import ConstraintType
from ConstraintFinder import ConstraintIfType 
from Graph import Graph

#os.environ["PYCSP3_SOLVERS"] = "ace=java -jar C:/Data/Ecole/ACE/ACE/build/ACE-2.5.jar"
# OPTIONNEL : configure le solveur ACE automatiquement s'il est disponible

# solvers_path = os.path.join(os.path.dirname(__file__), "solvers")
# print("Dossier des solveurs PyCSP3 :", solvers_path)
# print("Contenu :", os.listdir(solvers_path))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# os.environ["PYCSP3_SOLVERS"] = "ace=java -jar C:/Users/mathe/OneDrive/Bureau/LIRMM/Coco-fortis/venv313/Lib/site-packages/pycsp3/solvers/ace/ACE-2.5.jar"



def CreateCondition(all_constraint_if, node, graph):
    for constraint_if in all_constraint_if:
        match constraint_if:
            case ConstraintIfType.IF_FORM_REPEAT_LARGEST_OR_LOWEST:
                if all_constraint_if[constraint_if] == "LARGE":
                    if Graph.IsNodeRepeatingLargest(node, graph) == False:
                        return False
                elif all_constraint_if[constraint_if] == "LOW":
                    if Graph.IsNodeRepeatingLowest(node, graph) == False:
                        return False
            case ConstraintIfType.IF_SIZE:
                if node.BiggerSize(all_constraint_if[constraint_if]) == False:
                    return False
            case ConstraintIfType.IF_FORM_CONTAINED:
                if node.GetCenteredInNodes() == False:
                    return False
    return True



def Resolver(final_constraint, input_grid):
    
    graph_input = Graph(input_grid)
    
    grid = []
    if ConstraintType.GRID_SIZE in final_constraint:
        size =  list(final_constraint[ConstraintType.GRID_SIZE].keys())[0]
        for x in range (size):
            inter = []
            for y in range (size):
                inter.append(0)
            grid.append(inter)
    else:
        size = graph_input.GetGridSize()
        

    # TODO if grid is superior than original grid, replace old grid by new one



    if ConstraintType.NUMBER_NODES_OUTPUT in final_constraint:
        nb_nodes = list(final_constraint[ConstraintType.NUMBER_NODES_OUTPUT].keys())[0]
    else:
        nb_nodes = 5

    # VARIABLES 

    # FOR EACH NODES
    node_size = graph_input.GetNumberNodes()
    nodes = graph_input.GetNodes()
    original_size = graph_input.GetGridSize()
    graph_input.SetNewGrid(grid)

    nodex_offset_x = VarArray(size=[node_size], dom=range(-original_size, original_size))
    nodex_offset_y = VarArray(size=[node_size], dom=range(-original_size, original_size))
    nodex_color = VarArray(size=[node_size], dom=range(10))
    nodex_active = VarArray(size=[node_size], dom=(0, 1))
    grid_size = Var(dom=(size))

    print("size = ", size)
    print("node_size = ", node_size)
    print("nodes = ", nodes)
    print("nodex_offset_x = ", nodex_offset_x)
    print("nodex_offset_y = ", nodex_offset_y)
    print("nodex_color = ", nodex_color)
    print("nodex_active = ", nodex_active)
    print("grid_size = ", grid_size)
    #nodex_rot = VarArray(size=[node_size], dom=(0, 45, 90, 135))
    #nodex_extend_to = VarArray(size=[node_size], dom=range(node_size))
    

    satisfy(
        grid_size == size
    )

    # CONSTRAINTS

    # BASIC CONSTRAINT: let the nodes dont go outside the grid
    pos_found = []
    for i in range(len(nodes)):
        current_node = nodes[i]
        current_pos = []
        for x, y in current_node.GetPixelPositions():
            current_x = x + nodex_offset_x[i]
            current_y = y + nodex_offset_y[i]
            current_pos.append((current_x, current_y))
            satisfy(
                ~ (nodex_active[i] == 1) | (
                    (current_x >= 0) & (current_x < size) &
                    (current_y >= 0) & (current_y < size)
                )
            )
        pos_found.append(current_pos)

    # BASIC CONSTRAINT: let the nodes dont overlap
    for i in range (len(nodes)):
        for j in range (i+1, len(nodes)):
            first_node = pos_found[i]
            second_node = pos_found[j]
            for x_first, y_first in first_node:
                for x_second, y_second in second_node:
                   satisfy(
                       If(
                            (nodex_active[i] == 1) & (nodex_active[j] == 1),
                            Then=(x_first != x_second) | (y_first != y_second)
                        )
                    )

    # BASIC CONSTRAINT: number of nodes in output
    satisfy(
        Sum(nodex_active) >= 1,
        Sum(nodex_offset_x) >= -original_size*node_size,
        Sum(nodex_offset_y) >= -original_size*node_size,
        *[nodex_color[i] >= 1 for i in range(node_size)]
    )

    
    if nb_nodes != None:
        satisfy(
            Sum(nodex_active) == nb_nodes
        )
    else:
        maximize(
            Sum(nodex_active)
        )

    # COMPLEX CONSTRAINT: Constraints found

    # COMPLEX CONSTRAIT: All constraint for enabling or not a node
    for i in range (len(nodes)):
        for constraint in final_constraint:
            for constraint_value in final_constraint[constraint]:
                all_constraints = final_constraint[constraint][constraint_value]
                match constraint:
                    case ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT:
                        if not CreateCondition(all_constraints, nodes[i], graph_input):
                            print("nodes[i] = ", i)
                            satisfy(nodex_active[i] == 0)
                        continue
                    case ConstraintType.FORM_OUTPUT_COLOR:
                        if CreateCondition(all_constraints, nodes[i], graph_input):
                            satisfy (
                                If(nodex_active[i] == 1, Then=(nodex_color[i] == constraint_value))
                            ) 
                    case ConstraintType.COLOR_INPUT_EQUAL_OUTPUT:
                        if CreateCondition(all_constraints, nodes[i], graph_input):
                            satisfy (
                                If(nodex_active[i] == 1, Then=(nodex_color[i] == nodes[i].GetColor()))
                            ) 
                    case ConstraintType.CENTER_NODE:
                        if CreateCondition(all_constraints, nodes[i], graph_input):
                            node_pos = pos_found[i]
                            x_coords = [x for x, y in node_pos]
                            y_coords = [y for x, y in node_pos]

                            min_x = Minimum(x_coords)
                            max_x = Maximum(x_coords)
                            min_y = Minimum(y_coords)
                            max_y = Maximum(y_coords)

                            grid_width = size
                            grid_height = size
                            dist_left = min_x
                            dist_right = grid_width - max_x - 1
                            dist_up = min_y
                            dist_down = grid_height - max_y - 1

                            satisfy(
                                If(nodex_active[i] == 1,
                                    Then=(abs(dist_left - dist_right) <= 1) & (abs(dist_up - dist_down) <= 1)
                                )
                            )
                    case ConstraintType.KEEP_CONNECTION_TO_NODES:
                        if CreateCondition(all_constraints, nodes[i], graph_input):
                                associated = nodes[i].GetAssociatedNode()
                                (x_i, y_i) = pos_found[i][0]
                                for current_associated in associated:
                                    index_associated = nodes.index(current_associated[1])
                                    (x_j, y_j) = pos_found[index_associated][0]

                                    # dir = current_associated[1]
                                    # dist = current_associated[2]
                                    
                                    delta_x = nodes[i].GetPixelPositions()[0][0] - current_associated[1].GetPixelPositions()[0][0]
                                    delta_y = nodes[i].GetPixelPositions()[0][1] - current_associated[1].GetPixelPositions()[0][1]
                                    print("for node = ", i, "node voisin ")
                                    
                                    satisfy(
                                        If((nodex_active[i] == 1) & (nodex_active[index_associated] == 1),
                                            Then=(
                                                (x_i == x_j + delta_x) &
                                                (y_i == y_j + delta_y)
                                            )
                                        )
                                    )

    # compile()



    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # if solve(solver="ace") is SAT:
    #     print("----------------------On solve--------------------------------")
    
    if solve(solver="choco"):

        print("nodex_offset_x = ", values(nodex_offset_x))
        print("nodex_offset_y = ", values(nodex_offset_y))
        print("nodex_color = ", values(nodex_color))
        print("nodex_active = ", values(nodex_active))

        return {
            "nodex_offset_x": values(nodex_offset_x),
            "nodex_offset_y": values(nodex_offset_y),
            "nodex_color": values(nodex_color),
            "nodex_active":values(nodex_active),
            "grid_size":value(grid_size),
            "grid_size_active": ConstraintType.GRID_SIZE in final_constraint
        }
    
    else:
        print("Pas de solution (UNSAT).")
        return None