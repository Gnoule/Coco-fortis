from pycsp3 import *
import os
from ConstraintFinder import ConstraintType
from ConstraintFinder import ConstraintIfType 
from Graph import Graph

os.environ["PYCSP3_SOLVERS"] = "ace=java -jar C:/Data/Ecole/ACE/ACE/build/ACE-2.5.jar"

def Resolver(final_constraint, input_grid):
    
    graph_input = Graph(input_grid)
    
    grid = []
    if ConstraintType.GRID_SIZE in final_constraint:
        size = final_constraint[ConstraintType.GRID_SIZE]['value']
        for x in range (size):
            inter = []
            for y in range (size):
                inter.append(0)
            grid.append(inter)
    else:
        return


    for node in graph_input.GetNumberNodes():
        x = VarArray(size=[rows,columns], dom=range(10))
    
    satisfy(

        *(AllDifferent(x[i]) for i in range(rows)),
        
        *(AllDifferent([x[i][j] for i in range(rows)]) for j in range(columns)),

        *(AllDifferent([x[I][J] for I in range (3*i, 3*(i+1)) for J in range (3*j, 3*(j+1))]) for i in range (3) for j in range (3)),
        
        

        
        

        # DOIT PRENDRE LE NOMBRE DE LA GRILLE
        *(x[i][j] == grid[i][j] 
        for i in range(rows) 
        for j in range(columns) 
        if grid[i][j] != 0),
        

    );
    if solve(solver="ace") is SAT:
        print(values(x))
