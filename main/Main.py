import json
from ConstraintFinder import *
from ConstraintResolver import *
from ResolverFromCP import *
from datetime import datetime
import copy

example = ['39a8645d','28bf18c6','27a28665','25d487eb','08ed6ac7','7f4411dc']

#3de23699
data = None
with open('training/8a004b2b.json') as json_file:
    data = json.load(json_file)


training_examples = data['train']

#print(training_examples[2]['input'])
#graph = Graph(training_examples[2]['input'])
#graph.ShowGrid()
# input_example = training_examples[0]['input']
# output_example = training_examples[0]['output']

# input_example1 = [
#     [0, 1, 0, 0, 0, 0, 0],
#     [1, 1, 1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0],
#     [0, 0, 0, 1, 1, 1, 0],
#     [0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]

# output_example1 = [
#     [0, 1, 0, 0, 0, 0, 0],
#     [1, 1, 1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0],
#     [0, 1, 1, 1, 1, 1, 0],
#     [0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]

# input_example2 = [
#     [0, 0, 2, 0, 0, 0, 0],
#     [0, 2, 2, 2, 0, 0, 0],
#     [0, 0, 2, 0, 0, 2, 0],
#     [0, 0, 0, 0, 2, 2, 2],
#     [0, 0, 0, 0, 0, 2, 0],
#     [0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]

# output_example2 = [
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 3, 3, 3, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]


# evaluation_example = [
#     [0, 4, 0, 0, 0, 4, 0],
#     [4, 4, 4, 0, 4, 4, 4],
#     [0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 4, 0, 0, 1],
#     [0, 0, 4, 4, 4, 0, 1],
#     [0, 0, 0, 0, 0, 0, 0],
# ]

# input_example1 = [
#     [0, 1, 0, 0, 0, 1, 0],
#     [1, 1, 1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0],
#     [0, 0, 0, 1, 1, 1, 0],
#     [0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]

# output_example1 = [
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 3, 3, 3, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]

# input_example2 = [
#     [0, 0, 2, 0, 0, 0, 0],
#     [0, 2, 2, 2, 0, 0, 0],
#     [0, 0, 2, 0, 0, 2, 0],
#     [0, 0, 0, 0, 2, 2, 2],
#     [0, 0, 0, 0, 0, 2, 0],
#     [0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]

# output_example2 = [
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 3, 3, 3, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]


# evaluation_example = [
#     [0, 4, 0, 0, 0, 4, 0],
#     [4, 4, 4, 0, 4, 4, 4],
#     [0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 4, 0, 0, 1],
#     [0, 0, 4, 4, 4, 0, 1],
#     [0, 0, 0, 0, 0, 0, 0],
# ]



def Finder(examples, evaluation):
    constraints_brut = []
    startTime = datetime.now()
    # input = Graph(examples[3]['input'])
    # FindConstraintFromExample(examples[3]['input'], examples[3]['output'])
    # input.ShowGraph()
    # input.ShowGrid()
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

# input_example2 = [
#     [0, 2, 0, 0, 0, 0, 0],
#     [2, 2, 2, 0, 0, 0, 0],
#     [0, 2, 2, 0, 0, 2, 0],
#     [0, 0, 0, 0, 2, 2, 2],
#     [0, 0, 0, 0, 0, 2, 0],
#     [0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]
# g = Graph(input_example2)
# g.ShowGraph()