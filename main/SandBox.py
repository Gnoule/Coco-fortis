from Graph import Graph
from datetime import datetime
from Nodes import Node

graph_input = Graph([
    [0, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 4, 2, 0, 1, 1, 0],
    [0, 0, 0, 0, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

graph_output = Graph([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 0, 0, 4, 4, 1, 1, 0],
    [0, 2, 2, 0, 0, 4, 4, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

graph_node = graph_input.GetNodes()

# graph_input.ShowGrid()
# graph_input.ShowGraph()

# print(f"\n=== {len(graph_node)} nœuds détectés dans le graph_input ===")
# for i, node in enumerate(graph_node):
#     print(f"\nNode #{i + 1}")
#     print(f"  - Couleur : {node.GetColor()}")
#     print(f"  - Taille  : {node.GetSize()}")
#     print(f"  - Pixels  : {node.GetPixelPositions()}")

node = graph_node[0]

pattern = graph_input.findPattern(node, graph_input)