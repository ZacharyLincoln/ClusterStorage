import requests
from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/online', methods=['GET', 'POST'])
def online():
    return "200"


@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'GET':
        id = request.args.get('id')
        data = request.args.getlist('data')

        print(id)
        print(data)

        save_file(id, data)


    return ""


@app.route('/download', methods=['GET', 'POST'])
def download():

    if request.method == 'GET':
        id = request.args.get('id')
        return retrieve_file(id)

    return 'Hello World!'


# Save a file
def save_file(id, data):
    output = {
        "id": id,
        "data": data
    }

    with open(id, "w+") as output_file:
        json.dump(output, output_file)


# Look for the file with a given id
def retrieve_file(id):

    with open(id, "r") as input_file:
        input = input_file.readlines()
        return json.loads(input.pop())


if __name__ == '__main__':
    master_node_ip = "http://10.0.0.9:8080"
    response = requests.get(url=master_node_ip + "/setup")
    app.run()

