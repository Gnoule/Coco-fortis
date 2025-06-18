from pycsp3 import *

n = 4

R, G, B = colors = 0, 1, 2

# x[i] is the color of the ith node
x = VarArray(size=n, dom=colors)

satisfy(
    x[0] != x[2],

    x[1] != x[3]
);

if solve(solver="CHOCO") is SAT:
    print(values(x))
else:
    print("zaza")