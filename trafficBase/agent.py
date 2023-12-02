from mesa import Agent
import networkx as nx # creo esto solo es necesario si uso nx.astar_path

# Heurística para el algoritmo A*
def manhattanDistance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])
class Car(Agent):
    # Función para definir parametros iniciales del agente
    def __init__(self, unique_id, model, start_pos, destination):
        super().__init__(unique_id, model)

        self.start = start_pos
        self.destination = destination
        print(f"Car {self.unique_id} spawned at {self.pos} tryna reach destination {self.destination}")
        self.path = []
    
    # Función que utiliza el algoritmo de A* para encontrar el camino que debe tomar  
    def find_path(self):
        # Usando nx.astar_path
        G = self.model.G
        try: self.path = nx.astar_path(G, self.start, self.destination, heuristic = manhattanDistance)
        except nx.exception.NetworkXNoPath: self.path = None
        
        # Usando algoritmo A* "manual"
        # if self.destination:
        #     def path_clear(current_cell, next_step):
        #         content = self.model.grid.get_cell_list_contents([next_step])
        #         if any(isinstance(agent, Obstacle) for agent in content):
        #             return False
        #         if any(isinstance(agent, (Road, Traffic_Light, Destination)) for agent in content):
        #             road_agents = [agent for agent in content if isinstance(agent, Road)]
        #             if road_agents:
        #                 road_agent = road_agents[0]
        #                 return self.check_path(current_cell, next_step, road_agent.direction)
        #             return True
        #         return False
        #     return a_star(self.model.grid, self.start, self.destination, path_clear)
        # return None 

    def move(self):
        x, y = self.pos
        
        current_cell = self.model.grid.get_cell_list_contents([(x, y)])
        
        if any(isinstance(agent, Road) for agent in current_cell):
            self.move_Road()

        elif any(isinstance(agent, Traffic_Light) for agent in current_cell):
            self.move_Traffic_Light()
            
        directions = {"Up": (0, 1), "Down": (0, -1), "Left": (-1, 0), "Right": (1, 0), "Up-Right": (1, 1), "Up-Left": (-1, 1), "Down-Right": (1, -1), "Down-Left": (-1, -1)}
        direction = self.move_Road()
        next_position = None
        
        if direction:
            x, y = directions[direction]
            front_x, front_y = self.pos[0] + x, self.pos[1] + y
            next_position = self.model.grid.get_cell_list_contents([(front_x, front_y)])
        
        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_agent(self, next_position)
            if self.pos == self.destination:
                print (f"Car {self.unique_id} reached destination {self.destination} in {self.stepsTaken} steps")
        
    def move_Road(self):
        x, y = self.pos
    

        current_cell = self.model.grid.get_cell_list_contents([(x, y)])

        if any(isinstance(agent, Road) for agent in current_cell):
            road_agent = next(agent for agent in current_cell if isinstance(agent, Road))
            self.direction = road_agent.direction

            next_x, next_y = x, y

            # Determine la siguiente posición basada en la dirección
            if road_agent.direction == "Right":
                next_x, next_y = x + 1, y
            elif road_agent.direction == "Left":
                next_x, next_y = x - 1, y
            elif road_agent.direction == "Up":
                next_x, next_y = x, y + 1
            elif road_agent.direction == "Down":
                next_x, next_y = x, y - 1
            elif road_agent.direction == "Up-Right":
                next_x, next_y = x + 1, y + 1
            elif road_agent.direction == "Up-Left":
                next_x, next_y = x - 1, y + 1
            elif road_agent.direction == "Down-Right":
                next_x, next_y = x + 1, y - 1
            elif road_agent.direction == "Down-Left":
                next_x, next_y = x - 1, y - 1

            # Check if the next cell has a Car agent
            next_cell_contents = self.model.grid.get_cell_list_contents([(next_x, next_y)])
            has_car = any(isinstance(agent, Car) for agent in next_cell_contents)

            if not has_car:
                # Move the agent if the next cell is empty or contains a Road and no Car is present
                self.model.grid.move_agent(self, (next_x, next_y))
                         
    def move_Traffic_Light(self):
        x, y = self.pos 
           
        current_cell = self.model.grid.get_cell_list_contents([(x, y)])    
        
        if any(isinstance(agent, Traffic_Light) for agent in current_cell):
            traffic_light_agent = next (agent for agent in current_cell if isinstance(agent, Traffic_Light))
            if traffic_light_agent.state:
                if self.direction == "Right":
                    self.model.grid.move_agent(self, (x + 1, y))
                elif self.direction == "Left":
                    self.model.grid.move_agent(self, (x - 1, y))
                elif self.direction == "Up":
                    self.model.grid.move_agent(self, (x, y + 1))
                elif self.direction == "Down":
                    self.model.grid.move_agent(self, (x, y - 1))
                elif self.direction == "Up-Right":
                    self.model.grid.move_agent(self, (x + 1, y + 1))
                elif self.direction == "Up-Left":
                    self.model.grid.move_agent(self, (x - 1, y + 1))
                elif self.direction == "Down-Right":
                    self.model.grid.move_agent(self, (x + 1, y - 1))
                elif self.direction == "Down-Left":
                    self.model.grid.move_agent(self, (x - 1, y - 1))
            else: 
                # Wait for the light to turn green 
                pass
        
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if not self.path:
            self.find_path()
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass