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

    def step(self, model, current_attacker_key, current_defender_key) -> None:
        """ 
        Executes all the stages for all agents. 
        """
        agent_keys = list(self._agents.keys())

        # 1. Attack stage
        getattr(self._agents[current_attacker_key], "attack")()
        self.time += self.stage_time

        # 2. Knowledge update stage
        getattr(self._agents[current_defender_key], "update_knowledge_own_hand")()
        self.time += self.stage_time

        # 3. Defence stage
        getattr(self._agents[current_defender_key], "defend")()
        self.time += self.stage_time

        # 4. Resolve attack stage
        model.resolve_attack(current_attacker_key, current_defender_key)
        self.time += self.stage_time

        # 5. Update the knowledge of all agents
        for agent_key in agent_keys:
            getattr(self._agents[agent_key], "update_knowledge_own_hand")()
        self.time += self.stage_time

        # 6. We do inference in the inference engine
        model.inference_engine.inference_for_players(model)
        self.time += self.stage_time










        

        self.steps += 1