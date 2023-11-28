from mesa import Model
from mesa.time import RandomActivation, SimultaneousActivation
from mesa.space import MultiGrid
from agent import *
import random
import json

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, N):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("city_files/mapDictionary.json"))

        self.traffic_lights = []

        # self.total_cars = 0

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('city_files/mod2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # Add cars
            self.add_cars(N)
            
            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "0", "2", "6", "8"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        
        self.num_agents = N
        self.running = True

    def add_cars(self, N):
        for i in range(N):
            car_agent = Car(i, self)
            self.schedule.add(car_agent)
            
            corner = random.choice([(0,0), (0, self.height-1), (self.width-1, 0), (self.width-1, self.height-1)])
            
            road_agent = self.grid.get_cell_list_contents([corner])
            road_agent = next ((agent for agent in road_agent if isinstance(agent, Road)), None)
            
            if isinstance(road_agent, Road):
                car_agent.direction = road_agent.direction
                # agent.move()
        
            self.grid.place_agent(car_agent, corner)
    
    def assign_random_destination(self):
        cars = [agent for agent in self.schedule.agents if isinstance(agent, Car)]
        destinations = [agent for agent in self.schedule.agents if isinstance(agent, Destination)]
        
        for car in cars:
            car.destination = random.choice(destinations)
            
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        
        cars = [agent for agent in self.schedule.agents if isinstance(agent, Car)]
        for car in cars:
            car.move_towards_destination()