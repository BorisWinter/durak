from mesa.time import BaseScheduler

class CustomStagedActivation(BaseScheduler):
    """A scheduler which allows agent activation to be divided into several
    stages instead of a single `step` method. All agents execute one stage
    before moving on to the next.

    Agents must have all the stage methods implemented. Stage methods take a
    model object as their only argument.

    This schedule tracks steps and time separately. Time advances in fractional
    increments of 1 / (# of stages), meaning that 1 step = 1 unit of time.

    """

    def __init__(
        self,
        model,
        stage_list = None,
    ) -> None:
        """Create an empty Staged Activation schedule.

        Args:
            model: Model object associated with the schedule.
            stage_list: List of strings of names of stages to run, in the
                         order to run them in.
            shuffle: If True, shuffle the order of agents each step.
            shuffle_between_stages: If True, shuffle the agents after each
                                    stage; otherwise, only shuffle at the start
                                    of each step.

        """
        super().__init__(model)
        self.stage_list = ["step"] if not stage_list else stage_list
        self.stage_time = 1 / len(self.stage_list) #TODO: Make sure the time matches with the stages

    def step(self, current_attacker_key, current_defender_key) -> None:
        """ 
        Executes all the stages for all agents. 
        """
        # agent_keys = list(self._agents.keys())

        # Attack stage
        getattr(self._agents[current_attacker_key], "attack")()  # Run stage
        

        # Update knowledge stage

        # Defence stage
        getattr(self._agents[current_defender_key], "defend")()  # Run stage

        self.time += self.stage_time # Update time after each stage

        self.steps += 1