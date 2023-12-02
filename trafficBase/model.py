from mesa import Model, DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import random
import json
import networkx as nx
import matplotlib.pyplot as plt

class CityModel(Model):
    # Función para inicializar la simulación
    def __init__(self, N):
        # Cargar el diccionario del mapa base
        dataDictionary = json.load(open("city_files/mapDictionary.json"))
        
        self.total_cars = 0
        
        # Lista vacía para guardar los semáforos
        self.traffic_lights = []
        
        # Lista vacía para guardar los destinos
        self.destinations = []
        
        # Crear grafo dirigido para representar la ciudad
        self.G = nx.DiGraph()

        # Abrir y leer el mapa base
        with open('city_files/mod2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)
            
            # Itera sobre el mapa base y crea los agentes correspondientes
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    # Todo este if andy lo reemplazo por process_cell
                    # Calles
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.G.add_node((c, self.height - r - 1), type = "road")
                    # Semáforos (no sé la diferencia entre S y S)
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        self.G.add_node((c, self.height - r - 1), type = "traffic_light")
                    # Obstáculos
                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Destinos
                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinations.append((c, self.height - r - 1))
                        self.G.add_node((c, self.height - r - 1), type = "destination")
                      
        self.num_agents = N
        self.running = True
        # Andres tiene un self.add_edges()
    
    # Función para añadir coches
    def add_cars(self, N):
        # Lista con las esquinas
        corners = ([(0,0), (0, self.height-1), (self.width-1, 0), (self.width-1, self.height-1)])
        
        # Itera sobre las esquinas y se agrega un coche en cada una
        for start_pos in corners:
            destination = random.choice(self.destinations)
            car_agent = Car(self.total_cars + 1, self, start_pos, destination)
            # Posiciona al agente en su posición
            self.grid.place_agent(car_agent, start_pos)
            # Se añade al agente
            self.schedule.add(car_agent)
            self.total_cars += 1

    def add_edges(self, directions):
        x, y = self.pos
        directions = {'Up': (0, 1), 'Down': (0, -1), 'Left': (-1, 0), 'Right': (1, 0)}
        # Aqui irian las diagonal directions pero omitamoslo por ahora
        
        # Recorre el mapa
        for x in range(self.width):
            for y in range(self.height):
                contents = self.grid.get_cell_list_contents((x, y))
                if any(isinstance(content, Road) for content in contents):
                    #self.add_xagent_edges(x,y, directions)
                    return 0
                elif any(isinstance(content, Obstacle) for content in contents):
                    for direction in directions.values():
                        dir_x, dir_y = direction
                        new_x, new_y = x + dir_x, y + dir_y
                        
            
    # Función para generar y visualizar grafo  
    def visualizeGraph(self):
        plt.figure(figsize=(10,10))
        plt.axis('on')
        plt.title("Traffic Simulation")

        # Calles
        road = [agent for agent in self.schedule.agents if isinstance(agent, Road)]
        road_x = [agent.pos[0] for agent in road]
        road_y = [agent.pos[1] for agent in road]
        plt.scatter(road_x, road_y, color="grey", s=100)

        # Destinos
        destination = [agent for agent in self.schedule.agents if isinstance(agent, Destination)]
        destination_x = [agent.pos[0] for agent in destination]
        destination_y = [agent.pos[1] for agent in destination]
        plt.scatter(destination_x, destination_y, color="lightgreen", s=100) #la s es el tamaño de la bolita

        # Semáforos
        traffic_light = [agent for agent in self.schedule.agents if isinstance(agent, Traffic_Light)]
        traffic_light_x = [agent.pos[0] for agent in traffic_light]
        traffic_light_y = [agent.pos[1] for agent in traffic_light]
        traffic_light_color = ["red" if not agent.state else "green" for agent in traffic_light]
        plt.scatter(traffic_light_x, traffic_light_y, color=traffic_light_color, s=1000)

        # Obstáculos
        obstacle = [agent for agent in self.schedule.agents if isinstance(agent, Obstacle)]
        obstacle_x = [agent.pos[0] for agent in obstacle]
        obstacle_y = [agent.pos[1] for agent in obstacle]
        plt.scatter(obstacle_x, obstacle_y, color="cadetblue", s=100)

        # Coches
        car = [agent for agent in self.schedule.agents if isinstance(agent, Car)]
        car_x = [agent.pos[0] for agent in car]
        car_y = [agent.pos[1] for agent in car]
        plt.scatter(car_x, car_y, color="black", s=100)

        plt.show()
             
    def step(self):
        # Avanzar el modelo
        self.schedule.step()
        
        # Cada 10 pasos, se añaden 4 coches nuevos    
        if (self.schedule.steps - 1) % 10 == 0:
            self.add_cars(4)

if __name__ == "__main__":
    model = CityModel(10)
    model.visualizeGraph()