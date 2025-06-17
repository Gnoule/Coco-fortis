from Graph import Graph

def CreateResult(CP_result, input_grid):
    if CP_result == None:
        return
    
    input_graph = Graph(input_grid)

    node_size = input_graph.GetNumberNodes()
    nodes = input_graph.GetNodes()
    for i in range(node_size):
        if CP_result["nodex_active"][i] == 0:
            input_graph.DeactivateNode(nodes[i])
    for i in range(node_size):
        if CP_result["nodex_active"][i] == 1:
            input_graph.MoveNode(nodes[i], CP_result["nodex_offset_x"][i], CP_result["nodex_offset_y"][i])
            input_graph.RecolorNode(nodes[i], CP_result["nodex_color"][i])
        # "nodex_offset_x": values(nodex_offset_x),
        #     "nodex_offset_y": values(nodex_offset_y),
        #     "nodex_color": values(nodex_color),
        #     "nodex_active":values(nodex_active)
    return input_graph
