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
os.environ["PYCSP3_SOLVERS"] = f"ace=java -jar C:/Users/hugod/AppData/Local/Programs/Python/Python313/Lib/site-packages/pycsp3/solvers/ace/ACE-2.3.jar"



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
    return True



def Resolver(final_constraint, input_grid):
    
    graph_input = Graph(input_grid)
    
    grid = []
    if ConstraintType.GRID_SIZE in final_constraint:
        size = final_constraint[ConstraintType.GRID_SIZE]['value'][0]
        for x in range (size):
            inter = []
            for y in range (size):
                inter.append(0)
            grid.append(inter)
    else:
        return

    # TODO if grid is superior than original grid, replace old grid by new one


    # VARIABLES 

    # FOR EACH NODES
    node_size = graph_input.GetNumberNodes()
    nodes = graph_input.GetNodes()

    nodex_offset_x = VarArray(size=[node_size], dom=range(-size, size))
    nodex_offset_y = VarArray(size=[node_size], dom=range(-size, size))
    nodex_color = VarArray(size=[node_size], dom=range(10))
    nodex_active = VarArray(size=[node_size], dom=(0, 1))

    print("size = ", size)
    print("node_size = ", node_size)
    print("nodes = ", nodes)
    print("nodex_offset_x = ", nodex_offset_x)
    print("nodex_offset_y = ", nodex_offset_y)
    print("nodex_color = ", nodex_color)
    print("nodex_active = ", nodex_active)
    #nodex_rot = VarArray(size=[node_size], dom=(0, 45, 90, 135))
    #nodex_extend_to = VarArray(size=[node_size], dom=range(node_size))
    



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
                        If(nodex_active[i] == 1, Then=(x_first != x_second) & (y_first != y_second))
                        # ~ (nodex_active[i] == 1) | (
                        #     (x_first != x_second) & (y_first != y_second)
                        # )
                    )

    # BASIC CONSTRAINT: number of nodes in output
    satisfy(
        Sum(nodex_active) == 1
    )

    # COMPLEX CONSTRAINT: Constraints found

    # COMPLEX CONSTRAIT: All constraint for enabling or not a node
    for i in range (len(nodes)):
        for constraint in final_constraint:
            match constraint:
                case ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT:
                    if not CreateCondition(final_constraint[constraint]['constraints_if'], nodes[i], graph_input):
                        print("nodes[i] = ", i)
                        satisfy(nodex_active[i] == 0)
                    continue
                case ConstraintType.FORM_OUTPUT_COLOR:
                    if CreateCondition(final_constraint[constraint]['constraints_if'], nodes[i], graph_input):
                        satisfy (
                            If(nodex_active[i] == 1, Then=(nodex_color[i] == final_constraint[constraint]['value']))
                        ) 
                case ConstraintType.CENTER_NODE:
                    if CreateCondition(final_constraint[constraint]['constraints_if'], nodes[i], graph_input):
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


    compile()

    
    if solve(solver="ace") is SAT:

        print("nodex_offset_x = ", values(nodex_offset_x))
        print("nodex_offset_y = ", values(nodex_offset_y))
        print("nodex_color = ", values(nodex_color))
        print("nodex_active = ", values(nodex_active))

        return {
            "nodex_offset_x": values(nodex_offset_x),
            "nodex_offset_y": values(nodex_offset_y),
            "nodex_color": values(nodex_color),
            "nodex_active":values(nodex_active)
        }
    
    else:
        print("Pas de solution (UNSAT).")
        return None