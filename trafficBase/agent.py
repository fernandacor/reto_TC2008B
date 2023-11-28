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
        
        # self.destination = destination;
        # self.path = None
        

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
        x, y = self.pos
        
        current_cell = self.model.grid.get_cell_list_contents([(x, y)])
        
        if any(isinstance(agent, Road) for agent in current_cell):
            self.move_Road()
            self.stepsTaken += 1

        elif any(isinstance(agent, Traffic_Light) for agent in current_cell):
            self.move_Traffic_Light()
            self.stepsTaken += 1

    def move_towards_destination(self):
        if self.destination:
            next_step = self.model.grid.get_direction_towards(self.pos, self.destination.pos)
            self.model.grid.move_agent(self, next_step)
            self.color = "pink"
        
    def move_Road(self):
        x, y = self.pos    
        
        current_cell = self.model.grid.get_cell_list_contents([(x, y)])    
        
        if any(isinstance(agent, Road) for agent in current_cell):
            road_agent = next (agent for agent in current_cell if isinstance(agent, Road))
            self.direction = road_agent.direction
            if road_agent.direction == "Right":
                self.model.grid.move_agent(self, (x+1, y))
            elif road_agent.direction == "Left":
                self.model.grid.move_agent(self, (x-1, y))
            elif road_agent.direction == "Up":
                self.model.grid.move_agent(self, (x, y+1))
            elif road_agent.direction == "Down":
                self.model.grid.move_agent(self, (x, y-1))
            elif road_agent.direction == "Up-Right":
                self.model.grid.move_agent(self, (x+1, y+1))
            elif road_agent.direction == "Up-Left":
                self.model.grid.move_agent(self, (x-1, y+1))
            elif road_agent.direction == "Down-Right":
                self.model.grid.move_agent(self, (x+1, y-1))
            elif road_agent.direction == "Down-Left":
                self.model.grid.move_agent(self, (x-1, y-1)) 
                           
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
