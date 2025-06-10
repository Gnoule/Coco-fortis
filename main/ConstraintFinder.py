from Graph import Graph
from datetime import datetime
from enum import Enum

class ConstraintType(Enum):
    GRID_SIZE = 0   # size of the grid of output
    FORM_INPUT_EQUAL_FORM_OUTPUT = 1    # actual node needs to be in the output form
    FORM_OUTPUT_COLOR = 2   # actual node needs to have specified color
    NUMBER_NODES_OUTPUT = 3     # graph needs to have specified number of nodes
    FORM_NEAR_OTHER_FORM = 4     # actual node needs to have moved to another node
    NODE_SIZE = 5   # actual node needs to have specified size
    NODE_X_FIXED = 6    # actual node needs to NOT move in X direction
    NODE_Y_FIXED = 7    # actual node needs to NOT move in y direction
    DEACTIVE = 8    #actual node needs to be deactivated
    EXTEND_TO_NODE = 9      # actual node needs to be extended to other node

class ConstraintIfType(Enum):
    NONE = 0    #no condition (apply to all nodes / apply to graph)
    IF_SIZE = 1     # if actual node is superior to size
    IF_COLOR = 2    # if actual node is of color
    IF_NODE_EMPTY = 3   # if actual node has a hole
    IF_FORM_NEAR_OTHER_FORM = 4     # if actual node is connected to another nodez
    IF_FORM_REPEAT = 5      # if actual node is found repeating (multiple sequences detected)
    IF_NODE_UNKNOW = 6      # if actual node is not found at all 💀



class Constraint:
    def __init__(self, type, value, type_if):
        self.constraint_type = type
        self.constraint_value = value
        self.constraint_if = type_if


def FindConstraintFromExample(training_input, training_output):
    
    constraints_found = []

    # initialization
    startTime = datetime.now()
    graph_input = Graph(training_input)
    graph_output = Graph(training_output)
    print(datetime.now() - startTime)

    graph_input.ShowGrid()
    graph_input.ShowGraph()
    graph_output.ShowGrid()
    graph_output.ShowGraph()

    # start finding constraint

    # taille grid
    size = graph_output.GetGridSize()
    constraints_found.append(Constraint(ConstraintType.GRID_SIZE, size, ConstraintIfType.NONE))

    # nb noeuds
    nb_nodes = graph_output.GetNumberNodes()
    constraints_found.append(Constraint(ConstraintType.NUMBER_NODES_OUTPUT, nb_nodes, ConstraintIfType.NONE))


    # main loop
    for input_node in graph_input.GetNodes():

        result_compare_nodes = Graph.CompareNodeBetweenGraphs(input_node, graph_input)
        if result_compare_nodes['match_count'] > 0:
            current_if_types = GetConstraintIfTypes(input_node, graph_input)

            constraints_found.append(Constraint(ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT, None, current_if_types))
            constraints_found.append(Constraint(ConstraintType.FORM_OUTPUT_COLOR, input_node.GetColor(), current_if_types))
            constraints_found.append(Constraint(ConstraintType.NODE_X_FIXED, None, current_if_types))
            constraints_found.append(Constraint(ConstraintType.NODE_Y_FIXED, None, current_if_types))
            
            continue


        result_compare_sequences = Graph.CompareNodeSequenceBetweenGraphs()
        if result_compare_sequences['match_count'] > 0:
            current_if_types = GetConstraintIfTypes(input_node, graph_input)

            constraints_found.append(Constraint(ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT, None, current_if_types))
            constraints_found.append(Constraint(ConstraintType.FORM_OUTPUT_COLOR, input_node.GetColor(), current_if_types))
            constraints_found.append(Constraint(ConstraintType.NODE_X_FIXED, None, current_if_types))
            constraints_found.append(Constraint(ConstraintType.NODE_Y_FIXED, None, current_if_types))

            continue
        
        result_compare_extended = Graph.CompareNodeExtended(graph_input, graph_output, input_node)
        if result_compare_extended['match_found'] > 0:
            current_if_types = GetConstraintIfTypes(input_node, graph_input)

            constraints_found.append(Constraint(ConstraintType.EXTEND_TO_NODE, None, current_if_types))
        
            continue

        constraints_found.append(Constraint(ConstraintType.DEACTIVE, None, ConstraintIfType.IF_NODE_UNKNOW))


        

        


# TODO function to check a lot of informations on current node to check what are the conditions for adding the constraints (color, size, edges connections, ...)
def GetConstraintIfTypes(current_node, node_found, graph):
    pass


# TODO function to filter constraints found during all test examples
def FilterConstraint():
    pass