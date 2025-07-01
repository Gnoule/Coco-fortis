from Graph import Graph

def CreateResult(CP_result, input_grid):
    if CP_result == None:
        return
    
    size = CP_result['grid_size']

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

    if (CP_result['grid_size_active']):
        input_graph.ResizeGrid(size, size)
    else:
        size_x, size_y = input_graph.ResizeGridOnNodes()
        #input_graph.ResizeGrid(size_x, size_y)
    return input_graph
