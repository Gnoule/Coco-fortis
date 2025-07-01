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
    CENTER_NODE = 10    # center node to the grid
    COLOR_INPUT_EQUAL_OUTPUT = 11     # the color in input is equal to output
    KEEP_CONNECTION_TO_NODES = 12        # node has keep same connection

class ConstraintIfType(Enum):
    NONE = 0    #no condition (apply to all nodes / apply to graph)
    IF_SIZE = 1     # if actual node is superior to size
    IF_COLOR = 2    # if actual node is of color
    IF_NODE_EMPTY = 3   # if actual node has a hole
    IF_FORM_NEAR_OTHER_FORM = 4     # if actual node is connected to another nodez
    IF_FORM_REPEAT = 5      # if actual node is found repeating (multiple sequences detected)
    IF_NODE_UNKNOW = 6      # if actual node is not found at all 💀
    IF_FORM_REPEAT_LARGEST_OR_LOWEST = 7      # if actual node has repeating patern the largest LARGE OR LOW
    IF_FORM_CONTAINED = 8       # if node is contained in other nodes

constraint_everywhere = [ConstraintType.COLOR_INPUT_EQUAL_OUTPUT, ConstraintType.CENTER_NODE]
constrait_equals = [ConstraintType.GRID_SIZE, ConstraintType.NUMBER_NODES_OUTPUT]
constraints_ifs_everywhere = []
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
    # graph_input.ShowGraph()
    # graph_output.ShowGrid()   
    # graph_output.ShowGraph()

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
            for output_node_raw in result_compare_nodes['matches']:
                output_node = output_node_raw[0]
                current_if_types = GetConstraintIfTypes(input_node, graph_input)
                for current in current_if_types:
                    type = current['type']
                    value = current['value']
                    AddConstraints(constraints_found, ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT, None, type, value)
                    AddConstraints(constraints_found, ConstraintType.FORM_OUTPUT_COLOR, output_node.GetColor(), type, value)
                    if input_node.GetColor() == output_node.GetColor():
                        AddConstraints(constraints_found, ConstraintType.COLOR_INPUT_EQUAL_OUTPUT, None, type, value)
                    


                    compare_pos = Graph.CompareTwoNodesPosition(graph_input, graph_output, input_node, output_node)
                    if compare_pos[0] == 0:
                        AddConstraints(constraints_found, ConstraintType.NODE_X_FIXED, None, type, value)
                    if compare_pos[1] == 0:
                        AddConstraints(constraints_found, ConstraintType.NODE_Y_FIXED, None,type, value)

                    if graph_output.IsNodeInCenter(output_node):
                        AddConstraints(constraints_found, ConstraintType.CENTER_NODE, None, type, value)
                    
                    if Graph.CompareConnectionsBetweenGraphs(input_node=input_node, output_node=output_node, output_graph=graph_output):
                        AddConstraints(constraints_found, ConstraintType.KEEP_CONNECTION_TO_NODES, None, type, value)
            
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

        involved_inputs, merged_node = Graph.CompareNodeExtended(graph_input, graph_output, input_node)
        if involved_inputs and merged_node:
            # Check if all involved input nodes have not moved (i.e., they still exist fully in the merged node)
            fixed = True
            for n in involved_inputs:
                # Each node must have all its original pixels present in the merged output node
                node_pixels = set(n.GetPixelPositions())
                merged_pixels = set(merged_node.GetPixelPositions())

                # Verify that all pixels from the input node are still present in the merged node (i.e., no displacement)
                if not node_pixels.issubset(merged_pixels):
                    fixed = False
                    break

            if fixed:
                # If the nodes are fixed in position, register a constraint indicating they are merged
                for current in GetConstraintIfTypes(input_node, graph_input):
                    type = current['type']
                    value = current['value']
                    AddConstraints(constraints_found, ConstraintType.EXTEND_TO_NODE, None, type, value)

            continue



        # AddConstraints(constraints_found, ConstraintType.DEACTIVE, None, ConstraintIfType.IF_NODE_UNKNOW, None)
        # constraints_found.append(Constraint(ConstraintType.DEACTIVE, None, ConstraintIfType.IF_NODE_UNKNOW))

    print("constraints_found = ", constraints_found)
    final_constraints = FilterConstraintsIfTypes(constraints_found)
    print("final constraint = ", final_constraints)
    return final_constraints


        
# constraint1 -> (value1->constraint_if1->[value]), value2->constraint_if1->[value]
def AddConstraints(constraints_found, constraint_type, constraint_value, constraint_if_types, constraint_if_types_value):
    if constraint_type not in constraints_found or constraint_value not in constraints_found[constraint_type]:
       constraints_found[constraint_type] = {constraint_value: {}}
    if constraint_if_types not in constraints_found[constraint_type][constraint_value]:
        constraints_found[constraint_type][constraint_value][constraint_if_types] = []
    constraints_found[constraint_type][constraint_value][constraint_if_types].append(constraint_if_types_value)
    #constraints_found[constraint_type]['constraints_if'][constraint_if_types].append(constraint_if_types_value)
    #constraints_found[constraint_type]['value'].append(constraint_value)



# function to check a lot of informations on current node to check what are the conditions for adding the constraints (color, size, edges connections, ...)
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

    is_center_in_nodes = current_node.GetCenteredInNodes()
    if is_center_in_nodes:
        all_constraint_if_types.append({"type":ConstraintIfType.IF_FORM_CONTAINED, "value": None})
    
    return all_constraint_if_types


def FilterConstraintsIfTypes(constraints_found):
    new_constraint_found = {}
    for index_constraint in constraints_found:
        constraint = constraints_found[index_constraint]
        constraint_type_if_visited = []

        # check if value same:
        # if not all(x==constraint['value'][0] for x in constraint['value']):
        #     continue

        for contraint_value in constraint:
            for constraint_type_if in constraint[contraint_value]:
                #check if value same
                if not all(x==constraint[contraint_value][constraint_type_if][0] for x in constraint[contraint_value][constraint_type_if]):
                    continue
                if index_constraint not in new_constraint_found:
                    new_constraint_found[index_constraint] = {contraint_value:{}}
                # if constraint_type_if not in new_constraint_found[index_constraint][contraint_value]:
                #     constraints_found[index_constraint][contraint_value][constraint_type_if] = 
                new_constraint_found[index_constraint][contraint_value][constraint_type_if] = constraint[contraint_value][constraint_type_if][0]
    return new_constraint_found
                


    #         for value_constraint_type_if_visited in constraint_type_if_visited:
    #             if set(constraint_type_if) == set(value_constraint_type_if_visited): 
    #                 continue
                
    #         values_possible = []
    #         for constraint_type_search in constraint['constraints_if']:
    #             # check if set is not the same
    #             for value_constraint_type_if_visited in constraint_type_if_visited:
    #                 if set(constraint_type_search) == set(value_constraint_type_if_visited):
    #                     continue

    #             #if type_if are the same (we check if set is same)
    #             if constraint_type_if == constraint_type_search:
    #                 constraint_type_if_visited.append(constraint_type_search)
    #                 # if not added before
    #                 if constraint['constraints_if'][constraint_type_search] not in values_possible:
    #                     values_possible.append(constraint['constraints_if'][constraint_type_search][0])
    #         if index_constraint not in new_constraint_found:
    #             new_constraint_found[index_constraint] = {'value': constraint['value'], 'constraints_if': {}}
    #         new_constraint_found[index_constraint]['constraints_if'][constraint_type_if] = values_possible
    # return new_constraint_found




# function to filter constraints found during all test examples
# examples_constraints : [['constraint1'=> (), 'constraint1'=> ()], ['constraint1'=> (), 'constraint1'=> ()]]
# cancerous function warning
def FilterConstraint(examples_constraints):
    constraint_to_add = {}
    constraint_to_delete = []
    constraint_if_deleted = {}  # will be useful to avoid putting contraint_if already deleted 
    constraint_visited = []
    # test all found examples
    for index_constraints_found in range(len(examples_constraints)): 
        constraint_is_deleted = False
        current_constraints_found = examples_constraints[index_constraints_found]
        #test all constraints of said example
        for name_constraint in current_constraints_found:
            if name_constraint in constraint_visited or name_constraint in constraint_to_delete:
                continue
            if constraint_is_deleted:
                break
            current_constraint = current_constraints_found[name_constraint]
            constraint_visited.append(name_constraint)

            constraint_to_add[name_constraint] = {}
            #constraint_to_add[name_constraint]['value'] = current_constraint['value']

            constraint_if_deleted[name_constraint] = []
            
            # check if for constraint that HAS to be in all examples, is not in the current
            # if no, then we delete this constraint
            for name_const in constraint_everywhere:
                if name_const not in current_constraints_found and name_const not in constraint_to_delete:
                    constraint_to_delete.append(name_const)
                    del constraint_to_add[name_constraint]
                    constraint_is_deleted = True
                    break
            
            # check n+1 example
            # we will add values, and constraints if value as well
            for index_constraints_found_tested in range(index_constraints_found+1, len(examples_constraints)):
                
                if constraint_is_deleted:
                    break
                
                current_constraint_found_tested = examples_constraints[index_constraints_found_tested]
                
                # found constraint in other example
                if name_constraint == ConstraintType.FORM_INPUT_EQUAL_FORM_OUTPUT:
                    b = 3
                if name_constraint in current_constraint_found_tested:
                    current_constraint_tested = current_constraint_found_tested[name_constraint]

                    # first: if value for the constraint is not the same, we add it
                    for current_constraint_value in current_constraint:
                        
                        #we enter tryhard mode
                        if current_constraint_value in current_constraint_tested:
                            
                            # for each constraints if of current constraits (of current example)
                            for current_constraint_if in current_constraint[current_constraint_value]:
                                
                                # if other constraint (on other example) as same constraint if as this one
                                if current_constraint_if in current_constraint_tested[current_constraint_value]:

                                    # if constraints if values of both are same (not contradicting) so we add it to the official values (+check before if already in list so no double values + if not deleted on previous constraint search)
                                    if current_constraint[current_constraint_value][current_constraint_if] == current_constraint_tested[current_constraint_value][current_constraint_if]:
                                        if current_constraint_if not in constraint_if_deleted[name_constraint]:
                                            if current_constraint_value not in constraint_to_add[name_constraint]:
                                                constraint_to_add[name_constraint][current_constraint_value] = {}
                                            constraint_to_add[name_constraint][current_constraint_value][current_constraint_if] = current_constraint[current_constraint_value][current_constraint_if]
                                    # else, constraints are contradicting, if already in the liste, we delete it
                                    else:

                                        # we append this to never use for this constraint the constraint_if
                                        if current_constraint_if not in constraint_if_deleted[name_constraint]:
                                            constraint_if_deleted[name_constraint].append(current_constraint_if)
                                        
                                        if current_constraint_value in constraint_to_add[name_constraint] and current_constraint_if in constraint_to_add[name_constraint][current_constraint_value]:
                                            del constraint_to_add[name_constraint][current_constraint_value][current_constraint_if]
                                else:
                                    # if not found but in deleted, we dont add it
                                    if current_constraint_if in constraint_if_deleted[name_constraint]:
                                            continue
                                    
                                    if current_constraint_value not in constraint_to_add[name_constraint]:
                                        constraint_to_add[name_constraint][current_constraint_value] = {}
                                    # if the current_if was already in constraint to add, it means that in this new constraint it was not here anymore
                                    # so we delete it (because it wasnt found in all constraint)
                                    if current_constraint_if in constraint_to_add[name_constraint][current_constraint_value]:
                                        del constraint_to_add[name_constraint][current_constraint_value][current_constraint_if] 
                                        constraint_if_deleted[name_constraint].append(current_constraint_if)
                                    # if we find a new constraint if, we add it (because never found before and why not)
                                    # else:
                                    #     constraint_to_add[name_constraint][current_constraint_value][current_constraint_if] = current_constraint[current_constraint_value][current_constraint_if]
                                #else:
                                #    constraint_to_add[name_constraint][current_constraint_value][current_constraint_if] = current_constraint[current_constraint_value][current_constraint_if]
                        
                        # simply adding the constraint value + constraints ifs
                        else:
                            if name_constraint in constrait_equals:
                                constraint_to_delete.append(name_const)
                                del constraint_to_add[name_constraint]
                                constraint_is_deleted = True
                                break
                            # if current_constraint_value not in constraint_to_add[name_constraint]:
                            #     constraint_to_add[name_constraint][current_constraint_value] = {}
                            # constraint_to_add[name_constraint][current_constraint_value] = current_constraint_tested[current_constraint_value]
                    # if current_constraint_tested != constraint_to_add[name_constraint]['value']:
                    # if current_constraint_tested['value'] != constraint_to_add[name_constraint]['value']:
                    #     del constraint_to_add[name_constraint]
                    #     break
                        # constraint_to_add[name_constraint]['value'].append(current_constraint_tested['value'])  #TODO


                    # second: constraints_if, we check if there is same constraints_if
                    # if yes, check if the value changes. if yes, we erase this constraints_if (not the same between nodes so not important)
                    # if no, we can keep it

                    
                
                # if name_constraint in constraint_everywhere, then we need that constraint is in all examples found
                # if not, we delete it
                elif name_constraint in constraint_everywhere:
                    if name_constraint not in constraint_visited:
                        constraint_visited.append(name_constraint)
                    del constraint_to_add[name_constraint]
                    break

    return constraint_to_add                 





# def FilterConstraint(examples_constraints):
#     constraint_to_add = {}
#     constraint_to_delete = []
#     constraint_if_deleted = {}  # will be useful to avoid putting contraint_if already deleted 
#     constraint_visited = []
#     # test all found examples
#     for index_constraints_found in range(len(examples_constraints)): 
#         current_constraints_found = examples_constraints[index_constraints_found]
#         #test all constraints of said example
#         for name_constraint in current_constraints_found:
#             if name_constraint in constraint_visited or name_constraint in constraint_to_delete:
#                 continue
#             current_constraint = current_constraints_found[name_constraint]
#             constraint_visited.append(name_constraint)

#             constraint_to_add[name_constraint] = {'value': [], 'constraints_if': {}}
#             constraint_to_add[name_constraint]['value'] = current_constraint['value']

#             constraint_if_deleted[name_constraint] = []
            
#             # check if for constraint that HAS to be in all examples, is not in the current
#             # if no, then we delete this constraint
#             for name_const in constraint_everywhere:
#                 if name_const not in current_constraints_found and name_const not in constraint_to_delete:
#                     constraint_to_delete.append(name_const)
            
#             # check n+1 example
#             # we will add values, and constraints if value as well
#             for index_constraints_found_tested in range(index_constraints_found+1, len(examples_constraints)):
#                 current_constraint_found_tested = examples_constraints[index_constraints_found_tested]
                
#                 # found constraint in other example
#                 if name_constraint == ConstraintType.COLOR_INPUT_EQUAL_OUTPUT:
#                     b = 3
#                 if name_constraint in current_constraint_found_tested:
#                     current_constraint_tested = current_constraint_found_tested[name_constraint]

#                     # first: if value for the constraint is not the same, we add it
#                     if current_constraint_tested['value'] != constraint_to_add[name_constraint]['value']:
#                         del constraint_to_add[name_constraint]
#                         break
#                         # constraint_to_add[name_constraint]['value'].append(current_constraint_tested['value'])  #TODO


#                     # second: constraints_if, we check if there is same constraints_if
#                     # if yes, check if the value changes. if yes, we erase this constraints_if (not the same between nodes so not important)
#                     # if no, we can keep it

#                     # for each constraints if of current constraits (of current example)
#                     for current_constraint_if in current_constraint['constraints_if']:
#                         # if other constraint (on other example) as same constraint if as this one
#                         if current_constraint_if in current_constraint_tested['constraints_if']:

#                             # if constraints if values of both are same (not contradicting) so we add it to the official values (+check before if already in list so no double values + if not deleted on previous constraint search)
#                             if set(current_constraint['constraints_if'][current_constraint_if]) == set(current_constraint_tested['constraints_if'][current_constraint_if]):
#                                 if current_constraint_if not in constraint_if_deleted[name_constraint] and current_constraint_if not in constraint_to_add[name_constraint]['constraints_if']:
#                                     constraint_to_add[name_constraint]['constraints_if'][current_constraint_if] = current_constraint['constraints_if'][current_constraint_if][0]    # TODO [0] not sure
#                             # else, constraints are contradicting, if already in the liste, we delete it
#                             else:

#                                 # we append this to never use for this constraint the constraint_if
#                                 constraint_if_deleted[name_constraint].append(current_constraint_if)
                                
#                                 if current_constraint_if in constraint_to_add[name_constraint]['constraints_if']:
#                                     del constraint_to_add[name_constraint]['constraints_if'][current_constraint_if]
#                         else:
#                             constraint_to_add[name_constraint]['constraints_if'][current_constraint_if] = current_constraint['constraints_if'][current_constraint_if][0]  # TODO [0] not sure
                
#                 # if name_constraint in constraint_everywhere, then we need that constraint is in all examples found
#                 # if not, we delete it
#                 elif name_constraint in constraint_everywhere:
#                     if name_constraint not in constraint_visited:
#                         constraint_visited.append(name_constraint)
#                     del constraint_to_add[name_constraint]
#                     break

#     return constraint_to_add                 
