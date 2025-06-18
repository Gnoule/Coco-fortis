import json
from ConstraintFinder import *
from ConstraintResolver import *
from ResolverFromCP import *
from datetime import datetime
import copy

example = ['39a8645d','28bf18c6','27a28665','25d487eb','08ed6ac7','7f4411dc']

data = None
with open('training/39a8645d.json') as json_file:
    data = json.load(json_file)


training_examples = data['train']

#print(training_examples[2]['input'])
#graph = Graph(training_examples[2]['input'])
#graph.ShowGrid()
# input_example = training_examples[0]['input']
# output_example = training_examples[0]['output']



def Finder(examples, evaluation):
    constraints_brut = []
    startTime = datetime.now()
    for example in examples:
        constraints_brut.append(FindConstraintFromExample(example['input'], example['output']))
    final_constraint = FilterConstraint(constraints_brut)
    print("final_constraint = ", final_constraint)
    
    input_graph = Graph(copy.deepcopy(evaluation[0]['input']))

    result = Resolver(final_constraint, evaluation[0]['input'])

    graph = CreateResult(result, evaluation[0]['input'])
    print("FINDING CONSTRAINTS = ", datetime.now() - startTime)
    if graph != None:
        input_graph.ShowGrid()
        graph.ShowGrid()


Finder(data['train'], data['test'])