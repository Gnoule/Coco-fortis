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
    CENTER_NODE = 10    # TODO center node to the grid

class ConstraintIfType(Enum):
    NONE = 0    #no condition (apply to all nodes / apply to graph)
    IF_SIZE = 1     # if actual node is superior to size
    IF_COLOR = 2    # if actual node is of color
    IF_NODE_EMPTY = 3   # if actual node has a hole
    IF_FORM_NEAR_OTHER_FORM = 4     # if actual node is connected to another nodez
    IF_FORM_REPEAT = 5      # if actual node is found repeating (multiple sequences detected)
    IF_NODE_UNKNOW = 6      # if actual node is not found at all 💀
    IF_FORM_REPEAT_LARGEST_OR_LOWEST = 7      # if actual node has repeating patern the largest LARGE OR LOW



class Constraint:
    def __init__(self, type, value, type_if):
        self.constraint_type = type
        self.constraint_value = value
        self.constraint_if = type_if


def FindConstraintFromExample(training_input, training_output, want_time_log=False):
    
    constraints_found = {}

    # initialization
    startTime = datetime.now()
    graph_input = Graph(training_input)
    graph_output = Graph(training_output)
    if want_time_log:
        print(datetime.now() - startTime)

    # graph_input.ShowGrid()
    graph_input.ShowGraph()
    # graph_output.ShowGrid()   
    graph_output.ShowGraph()

    # start finding constraint

    # taille grid
    size = graph_output.GetGridSize()
    #constraints_found.append(Constraint(ConstraintType.GRID_SIZE, size, ConstraintIfType.NONE))
    AddConstraints(constraints_found, ConstraintType.GRID_SIZE, size, ConstraintIfType.NONE, None)

    # nb noeuds
    nb_nodes = graph_output.GetNumberNodes()
    AddConstraints(constraints_found, ConstraintType.NUMBER_NODES_OUTPUT, nb_nodes, ConstraintIfType.NONE, None)
    #constraints_found.append(Constraint(ConstraintType.NUMBER_NODES_OUTPUT, nb_nodes, ConstraintIfType.NONE))


    # main loop
    for input_node in graph_input.GetNodes():

        result_compare_nodes = Graph.CompareNodeBetweenGraphs(input_node, graph_output)
        if result_compare_nodes['match_count'] > 0:
            output_node = result_compare_nodes['matches'][0][0]
            current_if_types = GetConstraintIfTypes(input_node, graph_input)
            for current in current_if_types:
                type = current['type']
                value = current['value']
                AddConstraints(constraints_found, ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT, None, type, value)
                AddConstraints(constraints_found, ConstraintType.FORM_OUTPUT_COLOR, input_node.GetColor(), type, value)

                compare_pos = Graph.CompareTwoNodesPosition(graph_input, graph_output, input_node, output_node)
                if compare_pos[0] == 0:
                    AddConstraints(constraints_found, ConstraintType.NODE_X_FIXED, None, type, value)
                if compare_pos[1] == 0:
                    AddConstraints(constraints_found, ConstraintType.NODE_Y_FIXED, None,type, value)
            
            
            # constraints_found.append(Constraint(ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT, None, current_if_types))
            # constraints_found.append(Constraint(ConstraintType.FORM_OUTPUT_COLOR, input_node.GetColor(), current_if_types))
            # constraints_found.append(Constraint(ConstraintType.NODE_X_FIXED, None, current_if_types))
            # constraints_found.append(Constraint(ConstraintType.NODE_Y_FIXED, None, current_if_types))
            
            continue


        # result_compare_sequences = Graph.CompareNodeSequenceBetweenGraphs()
        # if result_compare_sequences['match_count'] > 0:
        #     current_if_types = GetConstraintIfTypes(input_node, graph_input)
        #     for current in current_if_types:
        #         type = current['type']
        #         value = current['value']
        #         AddConstraints(ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT, None, type, value)
        #         AddConstraints(ConstraintType.FORM_OUTPUT_COLOR, input_node.GetColor(), type, value)
        #         AddConstraints(ConstraintType.NODE_X_FIXED, None, type, value)
        #         AddConstraints(ConstraintType.NODE_Y_FIXED, None,type, value)

           

        #     continue
        
        # result_compare_extended = Graph.CompareNodeExtended(graph_input, graph_output, input_node)
        # if result_compare_extended['match_found'] > 0:
        #     current_if_types = GetConstraintIfTypes(input_node, graph_input)

        #     # constraints_found.append(Constraint(ConstraintType.EXTEND_TO_NODE, None, current_if_types))
        
        #     continue

        #AddConstraints(constraints_found, ConstraintType.DEACTIVE, None, ConstraintIfType.IF_NODE_UNKNOW, None)
        #constraints_found.append(Constraint(ConstraintType.DEACTIVE, None, ConstraintIfType.IF_NODE_UNKNOW))

    print("constraints_found = ", constraints_found)
    final_constraints = FilterConstraintsIfTypes(constraints_found)
    print(final_constraints)
    return final_constraints


        

def AddConstraints(constraints_found, constraint_type, constraint_value, constraint_if_types, constraint_if_types_value):
    if constraint_type not in constraints_found:
       constraints_found[constraint_type] = {'value': constraint_value, 'constraints_if': {}}
    constraints_found[constraint_type]['constraints_if'][constraint_if_types] = constraint_if_types_value



# TODO function to check a lot of informations on current node to check what are the conditions for adding the constraints (color, size, edges connections, ...)
def GetConstraintIfTypes(current_node, input_graph):
    all_constraint_if_types = []

    nodes_input_repeating = Graph.CompareNodeBetweenGraphs(current_node, input_graph)['match_count']
    if nodes_input_repeating > 0:
        all_constraint_if_types.append({"type":ConstraintIfType.IF_FORM_REPEAT, "value": nodes_input_repeating})
    
    if Graph.IsNodeRepeatingLargest(current_node, input_graph):
        all_constraint_if_types.append({'type':ConstraintIfType.IF_FORM_REPEAT_LARGEST_OR_LOWEST, 'value':'LARGE'})
    elif Graph.IsNodeRepeatingLowest(current_node, input_graph):
        all_constraint_if_types.append({'type':ConstraintIfType.IF_FORM_REPEAT_LARGEST_OR_LOWEST, 'value':'LOW'})

    node_color = current_node.GetColor()
    all_constraint_if_types.append({"type":ConstraintIfType.IF_COLOR, "value": node_color})

    node_size = current_node.GetSize()
    all_constraint_if_types.append({"type":ConstraintIfType.IF_SIZE, "value": node_size})

    node_empty = current_node.IsEmpty()
    if node_empty:
        all_constraint_if_types.append({"type":ConstraintIfType.IF_NODE_EMPTY, "value": None})

    is_connected = current_node.IsConnected()
    if is_connected:
        all_constraint_if_types.append({"type":ConstraintIfType.IF_FORM_NEAR_OTHER_FORM, "value": None})
    
    return all_constraint_if_types


def FilterConstraintsIfTypes(constraints_found):
    new_constraint_found = {}
    for index_constraint in constraints_found:
        constraint = constraints_found[index_constraint]
        constraint_type_if_visited = []
        for constraint_type_if in  constraint['constraints_if']:
            if constraint_type_if in constraint_type_if_visited:
                    continue
            values_possible = []
            for constraint_type_search in constraint['constraints_if']:
                if constraint_type_search in constraint_type_if_visited:
                    continue
                #if type_if are the same
                if constraint_type_if == constraint_type_search:
                    constraint_type_if_visited.append(constraint_type_search)
                    # if not added before
                    if constraint['constraints_if'][constraint_type_search] not in values_possible:
                        values_possible.append(constraint['constraints_if'][constraint_type_search])
            if index_constraint not in new_constraint_found:
                new_constraint_found[index_constraint] = {'value': constraint['value'], 'constraints_if': {}}
            new_constraint_found[index_constraint]['constraints_if'][constraint_type_if] = values_possible
    return new_constraint_found




# function to filter constraints found during all test examples
# examples_constraints : [['constraint1'=> (), 'constraint1'=> ()], ['constraint1'=> (), 'constraint1'=> ()]]
# cancerous function warning
def FilterConstraint(examples_constraints):
    constraint_to_add = {}
    constraint_visited = []
    # test all found examples
    for index_constraints_found in range(len(examples_constraints)): 
        current_constraints_found = examples_constraints[index_constraints_found]
        #test all constraints of said example
        for name_constraint in current_constraints_found:
            if name_constraint in constraint_visited:
                continue
            current_constraint = current_constraints_found[name_constraint]
            constraint_visited.append(name_constraint)

            constraint_to_add[name_constraint] = {'value': [], 'constraints_if': {}}
            constraint_to_add[name_constraint]['value'].append(current_constraint['value'])
            

            # check n+1 example
            # we will add values, and constraints if value as well
            for index_constraints_found_tested in range(index_constraints_found+1, len(examples_constraints)):
                current_constraint_found_tested = examples_constraints[index_constraints_found_tested]
                
                # found constraint in other example
                if name_constraint in current_constraint_found_tested:
                    current_constraint_tested = current_constraint_found_tested[name_constraint]

                    # first: if value for the constraint is not the same, we add it
                    if constraint_to_add[name_constraint]['value'] != current_constraint_tested['value']:
                        constraint_to_add[name_constraint]['value'].append(current_constraint_tested['value'])


                    # second: constraints_if, we check if there is same constraints_if
                    # if yes, check if the value changes. if yes, we erase this constraints_if (not the same between nodes so not important)
                    # if no, we can keep it

                    # for each constraints if of current constraits (of current example)
                    for current_constraint_if in current_constraint['constraints_if']:
                        # if other constraint (on other example) as same constraint if as this one
                        if current_constraint_if in current_constraint_tested['constraints_if']:
                            
                            # if constraints if values of both are same (not contradicting) so we add it to the official values (+check before if already in list so no double values)
                            if (set(current_constraint['constraints_if'][current_constraint_if]) == set(current_constraint_tested['constraints_if'][current_constraint_if]) 
                            and current_constraint_if not in constraint_to_add[name_constraint]['constraints_if']):
                                constraint_to_add[name_constraint]['constraints_if'][current_constraint_if] = current_constraint['constraints_if'][current_constraint_if]
                            # else, constraints are contradicting, if already in the liste, we delete it 
                            else:
                                if current_constraint_if in constraint_to_add[name_constraint]['constraints_if']:
                                    del constraint_to_add[name_constraint]['constraints_if'][current_constraint_if]
                        else:
                            constraint_to_add[name_constraint]['constraints_if'][current_constraint_if] = current_constraint_tested['constraints_if'][current_constraint_if]

    return constraint_to_add                 
