from mesa import Agent


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, start_pos):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        
        self.direction = "Right" # default
        self.destination = None
        self.stepsTaken = 0
        self.start = start_pos
    
    # Función que determina si el agente se puede mover en la dirección escogida
    def move(self):     
        x, y = self.pos
        current_cell = self.model.grid.get_cell_list_contents([(x, y)])
        
        if any(isinstance(agent, Road) for agent in current_cell):
            self.move_Road()
            self.stepsTaken += 1

        elif any(isinstance(agent, Traffic_Light) for agent in current_cell):
            self.move_Traffic_Light()
            self.stepsTaken += 1
        
    def move_Road(self):
        x, y = self.pos    
        # current_cell = self.model.grid.get_cell_list_contents([(x, y)]) 
        road_agents = [agent for agent in self.model.grid.get_cell_list_contents([(x, y)]) if isinstance(agent, Road)]  

        if road_agents:
            road_agent = road_agents[0]
            self.direction = road_agent.direction
            next_position = self.calculate_next_position()
            
        # Check if the next cell has a Car agent
        next_cell_contents = self.model.grid.get_cell_list_contents([next_position])
        has_car = any(isinstance(agent, Car) for agent in next_cell_contents)
        
        if not has_car:
            # Move the agent if the next cell is empty or contains a car
            self.model.grid.move_agent(self, next_position)
        
        # if any(isinstance(agent, Road) for agent in current_cell):
        #     road_agent = next (agent for agent in current_cell if isinstance(agent, Road))
            # self.direction = road_agent.direction
            # self.model.grid.move_agent(self, self.calculate_next_position())
            # self.stepsTaken += 1
            
            # # Check if the next cell has a Car agent
            # next_cell_contents = self.model.grid.get_cell_list_contents([(next_x, next_y)])
            # has_car = any(isinstance(agent, Car) for agent in next_cell_contents)

            # if not has_car:
            #     # Move the agent if the next cell is empty or contains a Road and no Car is present
            #     self.model.grid.move_agent(self, self.calculate_next_position())

    # def calculate_next_position(self):
    #     x, y = self.pos
    #     next_x, next_y = x, y
        
    #     if self.direction == "Right":
    #         next_x, next_y = x + 1, y
    #     elif self.direction == "Left":
    #         next_x, next_y = x - 1, y
    #     elif self.direction == "Up":
    #         next_x, next_y = x, y + 1
    #     elif self.direction == "Down":
    #         next_x, next_y = x, y - 1
    #     elif self.direction == "Up-Right":
    #         next_x, next_y = x + 1, y + 1
    #     elif self.direction == "Up-Left":
    #         next_x, next_y = x - 1, y + 1
    #     elif self.direction == "Down-Right":
    #         next_x, next_y = x + 1, y - 1
    #     elif self.direction == "Down-Left":
    #         next_x, next_y = x - 1, y - 1
            
    #     return next_x, next_y     
    
    def calculate_next_position(self):
        x, y = self.pos
        directions = {
            "Right": (x + 1, y),
            "Left": (x - 1, y),
            "Up": (x, y + 1),
            "Down": (x, y - 1),
            "Up-Right": (x + 1, y + 1),
            "Up-Left": (x - 1, y + 1),
            "Down-Right": (x + 1, y - 1),
            "Down-Left": (x - 1, y - 1)
        }  
        return directions[self.direction]
                      
    def move_Traffic_Light(self):
        x, y = self.pos  
        # current_cell = self.model.grid.get_cell_list_contents([(x, y)]) 
        traffic_light_agents = [agent for agent in self.model.grid.get_cell_list_contents([(x, y)]) if isinstance(agent, Traffic_Light)]
        
        if traffic_light_agents:
            traffic_light_agent = traffic_light_agents[0]
            
            if traffic_light_agent.state and self.check_distance_to_cars():
                next_position = self.calculate_next_position()
                self.model.grid.move_agent(self, next_position)
                self.stepsTaken += 1
            # else:
            #     # Wait for the light to turn green
            #     pass
        # if any(isinstance(agent, Traffic_Light) for agent in current_cell):
        #     traffic_light_agent = next (agent for agent in current_cell if isinstance(agent, Traffic_Light))
            
        #     if traffic_light_agent.state and self.check_distance_to_cars():
        #         next_position = self.calculate_next_position()
        #         self.model.grid.move_agent(self, next_position)
        #         self.stepsTaken += 1        
        #     else: 
        #         # Wait for the light to turn green
        #         pass
    
    def check_distance_to_cars(self):
        x, y = self.pos
        neighbors = self.model.grid.get_neighbors((x, y), moore=True, include_center=False)

        for neighbor in neighbors:
            if isinstance(neighbor, Car):
                min_distance = 2  # Adjust as needed
                if self.calculate_distance(self.pos, neighbor.pos) < min_distance:
                    return False
            elif isinstance(neighbor, Traffic_Light) and not neighbor.state:
                min_distance = 1  # Adjust as needed
                if self.calculate_distance(self.pos, neighbor.pos) < min_distance:
                    return False
        return True

    def check_distance_to_cars(self):
        x, y = self.pos
        neighbors = self.model.grid.get_neighbors((x, y), moore=True, include_center=False)

        for neighbor in neighbors:
            if isinstance(neighbor, Car):
                min_distance = 2
                if self.calculate_distance(self.pos, neighbor.pos) < min_distance:
                    return False
            elif isinstance(neighbor, Traffic_Light) and not neighbor.state:
                min_distance = 1
                if self.calculate_distance(self.pos, neighbor.pos) < min_distance:
                    return False

    def calculate_distance(self, pos_1, pos_2):
        x1, y1 = pos_1
        x2, y2 = pos_2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    
    # Función que determina la nueva dirección que el agente tomará, y avanza 
    def step(self):
        self.move()

# Clase para crear y posicionar semáforos en el grid
class Traffic_Light(Agent):
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
