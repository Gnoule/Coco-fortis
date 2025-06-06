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

FindConstraintFromExample(input_example, output_example)

