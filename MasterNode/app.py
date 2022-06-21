import random
import flask
import requests
from flask import Flask, request
import json

available_nodes = []

app = Flask(__name__)


@app.route('/setup', methods=['GET', 'POST'])
def setupNode():
    if request.method == 'GET':
        ip = "http://"+flask.request.remote_addr+":8080"

        print(ip)
        available_nodes.append(ip)
        serialize()
        return "Setup Complete"


@app.route('/getnodes', methods=['GET', 'POST'])
def getNodes():
    if request.method == 'GET':
        amount = int(request.args.get('amount'))

        # Check to see if nodes are still online
        for node in available_nodes:
            try:
                response = requests.get(url=node + "/online")
            except requests.exceptions.ConnectionError:
                available_nodes.remove(node)

            if response.text == "200":
                # Node is online keep in array
                pass
            else:
                # Node is offline remove from array
                available_nodes.remove(node)

        if len(available_nodes) < amount:
            return "400"

        indexs = random.sample(range(len(available_nodes)), amount)

        selected_nodes = []
        for index in indexs:
            selected_nodes.append(available_nodes[index])

        return str(selected_nodes)


def serialize():
    output = {
        "nodes": available_nodes
    }
    with open("/serv/Cluster/MasterNode/save.nodes", "w") as output_file:
        json.dump(output, output_file)


def load():
    global available_nodes
    try:
        with open("/serv/Cluster/MasterNode/save.nodes", "r") as input_file:
            input = input_file.readlines()
            json_in = json.loads(input.pop())


            available_nodes = json_in["nodes"]
    except FileNotFoundError:
        available_nodes = []

    print(available_nodes)


load()