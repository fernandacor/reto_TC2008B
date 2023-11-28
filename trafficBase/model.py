from mesa import Model, DataCollector
from mesa.time import RandomActivation, SimultaneousActivation
from mesa.space import MultiGrid
from agent import *
import random
import json

class CityModel(Model):
    # Función para inicializar la simulación
    def __init__(self, N):

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
            
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        
        # cars = [agent for agent in self.schedule.agents if isinstance(agent, Car)]
        # for car in cars:
        #     car.move_towards_destination()
        
        # Cada 10 pasos, spawnean 4 coches nuevos    
        if (self.schedule.steps - 1) % 10 == 0:
            self.add_cars(4)