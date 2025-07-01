from pycsp3 import *

clear()

node_size = 9
nodex_active = VarArray(size=[node_size], dom=(0, 1))
nodex_offset_x = VarArray(size=[node_size], dom=range(-10, 10))
nodex_offset_y = VarArray(size=[node_size], dom=range(-10, 10))
nodex_color = VarArray(size=[node_size], dom=range(0, 10))

satisfy(
    Sum(nodex_active) >= 1,
    Sum(nodex_offset_x) >= -10*node_size
)

maximize(
    Sum(nodex_active)
)

compile()

solution = solve(solver="ace", verbose=1)

if solution:
    print("Solution trouvée :", values(nodex_active))
    print("Solution trouvée :", values(nodex_offset_x))
    # print("Solution trouvée :", values(nodexa))
else:
    print("Aucune solution trouvée.")