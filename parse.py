from flask import Flask, jsonify, request
import json

from backend import BackendCalculator

app = Flask(__name__)


# Initialise the data from the database
backendCalculator = BackendCalculator()


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json(force=True)
    #name = data['name']
    #location = data['location']
    #randomlist = data['randomlist']
    with open("json_output.json", 'w') as outfile:
        json.dump(data,outfile)

    backendCalculator.add_data_to_spreadsheet(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
