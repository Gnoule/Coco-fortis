import json

example = ['39a8645d','28bf18c6','27a28665','25d487eb','08ed6ac7','7f4411dc']

data = None
with open('training/7f4411dc.json') as json_file:
    data = json.load(json_file)

print(data)
training_examples = data['train']
training_examples[0]