import random

import flask
import requests
from flask import Flask, request
import json

app = Flask(__name__)

available_nodes = []

@app.route('/setup', methods=['GET', 'POST'])
def setupNode():
    if request.method == 'GET':
        ip = "http:"+flask.request.remote_addr+":8080"

        print(ip)
        available_nodes.append(ip)
        return "Setup Complete"

@app.route('/getnodes', methods=['GET', 'POST'])
def getNodes():
    if request.method == 'GET':
        amount = int(request.args.get('amount'))

        # Check to see if nodes are still online
        for node in available_nodes:
            response = requests.get(url=node + "/online")
            if response.text == "200":
                # Node is online keep in array
                pass
            else:
                # Node is offline remove from array
                available_nodes.remove(node)

        if len(available_nodes) <= amount:
            return "400"

        indexs = random.sample(range(len(available_nodes)), amount)

        selected_nodes = []
        for index in indexs:
            selected_nodes.append(available_nodes[index])

        return selected_nodes



