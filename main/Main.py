import json
from ConstraintFinder import *
from datetime import datetime

example = ['39a8645d','28bf18c6','27a28665','25d487eb','08ed6ac7','7f4411dc']

data = None
with open('training/7f4411dc.json') as json_file:
    data = json.load(json_file)


training_examples = data['train']
input_example = training_examples[0]['input']
output_example = training_examples[0]['output']

input_example1 = [
    [0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

output_example1 = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0],
    [0, 0, 3, 3, 3, 0, 0],
    [0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

input_example2 = [
    [0, 0, 2, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 2, 0],
    [0, 0, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 2, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

output_example2 = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0],
    [0, 0, 3, 3, 3, 0, 0],
    [0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


evaluation_example = [
    [0, 4, 0, 0, 0, 4, 0],
    [4, 4, 4, 0, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 4, 0, 0, 1],
    [0, 0, 4, 4, 4, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
]

constraints_brut = []
startTime = datetime.now()
constraints_brut.append(FindConstraintFromExample(input_example1, output_example1))
constraints_brut.append(FindConstraintFromExample(input_example2, output_example2))
final_constraint = FilterConstraint(constraints_brut)
print("FINDING CONSTRAINTS = ", datetime.now() - startTime)
print("final_constraint = ", final_constraint)