def CreateResult(CP_result, input_graph):
    if CP_result == None:
        return
    
    node_size = input_graph.GetNumberNodes()
    for i in range(len(node_size)):
        if CP_result["nodex_active"][i] == 1:

        # "nodex_offset_x": values(nodex_offset_x),
        #     "nodex_offset_y": values(nodex_offset_y),
        #     "nodex_color": values(nodex_color),
        #     "nodex_active":values(nodex_active)
