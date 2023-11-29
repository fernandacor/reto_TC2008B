from agent import *
from model import CityModel
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
import random

# Función para definir como se va a mostrar cada agente
def agent_portrayal(agent):
    # Vacío
    if agent is None: return
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "w": 1,
                 "h": 1
                 }
    # Calles
    if (isinstance(agent, Road)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
    # Destinos
    if (isinstance(agent, Destination)):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0
    # Semáforos
    if (isinstance(agent, Traffic_Light)):
        portrayal["Color"] = "red" if not agent.state else "green"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
    # Obstáculos
    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
    # Coches
    if(isinstance(agent, Car)):
        # portrayal["Color"] = random.choice(["blue", "yellow", "purple", "pink", "orange"])
        portrayal["Color"] = "black"
        portrayal["Layer"] = 2
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    return portrayal

# Altura y ancho del grid
width = 0
height = 0

# Abrir y leer el archivo con el mapa base
with open('city_files/2023_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

# Definición de los parametros del modelo
model_params = {"N":0, "mapFile":"city_files/2023_base.txt"} # N = número de coches

# Imprimir altura y ancho del grid
print("W: ", width, ", H: ", height)

# Definición de la visualización
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

# Gráfica para mostrar la cantidad de agentes que hay en el modelo
bar_chart = BarChartModule (
    [{"Label": "Cars", "Color": "black"}],
    scope = "agent", sorting = "ascending", sort_by = "Steps")

# Definición del servidor
server = ModularServer(CityModel, [grid], "Traffic Base", model_params)
                       
server.port = 8522 # The default
server.launch()