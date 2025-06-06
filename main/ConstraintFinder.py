from Graph import Graph
from datetime import datetime

def FindConstraintFromExample(training_input, training_output):
    startTime = datetime.now()

    graph = Graph(training_input)
    graph.ShowGrid()
    graph.ShowGraph()
    
    print(datetime.now() - startTime)

def FilterConstraint():
    pass