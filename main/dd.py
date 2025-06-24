from pycsp3 import *

x = VarArray(size=4, dom=range(3))

satisfy(
    x[0] != x[2],
    x[1] != x[3]
)

solver("ace")
print("Solveur actif :", solver())


if solve() is SAT:
    print("SAT :", values(x))
else:
    print("UNSAT (zaza)")
