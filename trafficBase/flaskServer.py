# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2023git

from flask import Flask, request, jsonify
# from randomAgents.model import RandomModel
# from randomAgents.agent import RandomAgent, ObstacleAgent
from model import *
from agent import *
from model import CityModel

citymodel = None

# Size of the board:
number_agents = 10
width = 24
height = 25
randomModel = None
currentStep = 0

app = Flask("Traffic example")

@app.route('/init', methods=['GET', 'POST'])
def initModel():
    # global currentStep, randomModel, number_agents, width, height
    global citymodel

    # if request.method == 'POST':
    number_agents = int(request.form.get('NAgents', 10))
    width = int(request.form.get('width', 20))
    height = int(request.form.get('height', 20))
    currentStep = 0

    print(request.form)
    print(number_agents, width, height)
    # randomModel = RandomModel(number_agents, width, height)
    citymodel = CityModel(number_agents)

    return jsonify({"message":"Parameters recieved, model initiated."})
    # elif request.method == 'GET':
    #     number_agents = 10
    #     width = 30
    #     height = 30
    #     currentStep = 0
    #     randomModel = RandomModel(number_agents, width, height)

    #     return jsonify({"message":"Default parameters recieved, model initiated."})


@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel
    
    if citymodel is None: return
    agent_data = citymodel.get_agent_data()

    # if request.method == 'GET':
    #     agentPositions = [{"id": str(a.unique_id), "x": x, "y":1, "z":z}
    #                       for a, (x, z) in randomModel.grid.coord_iter()
    #                       if isinstance(a, RandomAgent)]
    print (agent_data)
    return jsonify({'positions': agent_data})


@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global citymodel

    # if request.method == 'GET':
    #     carPositions = [{"id": str(a.unique_id), "x": x, "y":1, "z":z}
    #                     for a, (x, z) in randomModel.grid.coord_iter()
    #                     if isinstance(a, ObstacleAgent)]

    return jsonify({'positions':[]})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        citymodel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})


if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)
