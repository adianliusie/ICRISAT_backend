import json
from backend import BackendCalculator

with open('json_test_data.txt') as json_file:
    json_string = json_file.read()
data = json.loads(json_string)

backendCalculator = BackendCalculator()

backendCalculator.add_data_to_spreadsheet(data)
