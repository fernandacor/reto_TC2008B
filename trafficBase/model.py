from mesa import Model, DataCollector
from mesa.time import RandomActivation, SimultaneousActivation
from mesa.space import MultiGrid
from agent import *
import random
import json
import networkx as nx
import matplotlib.pyplot as plt

class CityModel(Model):
    # Función para inicializar la simulación
    def __init__(self, N, mapFile):
        self.traffic_lights = []
        self.destination = []
        self.G = nx.Graph()
        self.schedule = RandomActivation(self)

         # Iterate over all agents and add them to the graph
        for agent in self.schedule.agents:
            self.G.add_node(agent)

            # Define relationships between different types of agents
        for agent in self.schedule.agents:
            if isinstance(agent, Car):
                # Example: Connect car agents to their destinations
                destination = agent.destination
                self.G.add_edge(agent, destination)

        with open(mapFile) as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "0", "2", "6", "8"]:
                        agent = Road(f"r_{r*self.width+c}", self, col)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destination.append(agent)
                    elif col == "C":
                        agent = Car(f"c_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        self.G.add_node(agent) 
                        self.G.add_edge(agent, agent.destination)

        # Cargar el diccionario del mapa base
        dataDictionary = json.load(open("city_files/mapDictionary.json"))

        # Lista vacía para guardar los semáforos
        self.traffic_lights = []
        # Inicializar el total de coches como 0
        self.total_cars = 0
        
        # Propiedad que permite recolectar datos de los agentes
        self.datacollector = DataCollector(
        agent_reporters = {"Steps": lambda a: a.stepsTaken if isinstance(a, Car) else 0})

        # Abrir y leer el mapa base
        with open('city_files/mod2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # Llamar a la función para añadir coches
            # self.add_cars(N)
            
            # Itera sobre el mapa base y crea los agentes correspondientes
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    # Calles
                    if col in ["v", "^", ">", "<", "0", "2", "6", "8"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Semáforos (no sé la diferencia entre S y S)
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                    # Obstáculos
                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    # Destinos
                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                      
        self.num_agents = N
        self.running = True
    
    # Función para añadir coches
    def add_cars(self, N):
        # Lista con las esquinas
        corner = ([(0,0), (0, self.height-1), (self.width-1, 0), (self.width-1, self.height-1)])
        
        # Itera sobre las esquinas y se agrega un coche en cada una
        for corner in corner:
            # agenteC = Car(unique_id, model, start_pos)
            car_agent = Car(self.total_cars + 1, self, corner)
            # Posiciona al agente en su posición
            self.grid.place_agent(car_agent, corner)
            # Se añade al agente
            self.schedule.add(car_agent)
            self.total_cars += 1
            
            # ?
            road_agent = self.grid.get_cell_list_contents([corner])
            road_agent = next ((agent for agent in road_agent if isinstance(agent, Road)), None)
            
            # ?
            if isinstance(road_agent, Road):
                car_agent.direction = road_agent.direction
                # agent.move()
        
    
    # def assign_random_destination(self):
    #     cars = [agent for agent in self.schedule.agents if isinstance(agent, Car)]
    #     destinations = [agent for agent in self.schedule.agents if isinstance(agent, Destination)]
        
    #     for car in cars:
    #         car.destination = random.choice(destinations)

    def visualize(self):
        # nx.draw(self.G, with_labels=True)
        # plt.show()
        # Traffic Light = Red
        # Destination = Green
        # Road = Grey
        # Obstacle = Cadetblue
        # Car = Black
        
        plt.figure(figsize=(10,10))
        plt.axis('off')
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
        plt.scatter(destination_x, destination_y, color="lightgreen", s=100)

        # Semáforos
        traffic_light = [agent for agent in self.schedule.agents if isinstance(agent, Traffic_Light)]
        traffic_light_x = [agent.pos[0] for agent in traffic_light]
        traffic_light_y = [agent.pos[1] for agent in traffic_light]
        traffic_light_color = ["red" if not agent.state else "green" for agent in traffic_light]
        plt.scatter(traffic_light_x, traffic_light_y, color=traffic_light_color, s=100)

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
        '''Advance the model by one step.'''
        self.schedule.step()
        
        # cars = [agent for agent in self.schedule.agents if isinstance(agent, Car)]
        # for car in cars:
        #     car.move_towards_destination()
        
        # Cada 10 pasos, spawnean 4 coches nuevos    
        if (self.schedule.steps - 1) % 10 == 0:
            self.add_cars(4)

if __name__ == "__main__":
    model = CityModel(10, "city_files/2023_base.txt")
    model.visualize()