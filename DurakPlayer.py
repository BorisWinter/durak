from mesa import Agent

class DurakPlayer(Agent):
    """Models a player in the game of Durak"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        print ("Hi, I am player " + str(self.unique_id) +".")