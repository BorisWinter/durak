class Inference:

    def __init__(self):
        print("todo")
        '''
        for each player, reason
        with common knowledge combined with
        their private knowledge
        (for some levels deep?) - > vary
        In order to gain new knowledge about the hand of some other player.


        todo: include hidden statistics as well, for us,
        to see if the inference reached is correct (not a statistic, really, but debugging,
        as it should always be valid if it's a K operator etc etc.
        
        Or like, number of correctly predicted cards per player
        0> give players different inference abilities? Tournament structure?
        
        
        '''


    def do_inference(self, common_knowledge, private_knowledge):
        new_knowledge = []
        print("inference magic here")
        return new_knowledge


    def inference_for_players(self, model):
        common_knowledge = model.common_knowledge
        for player in model.players:
            private_knowledge = player.private_knowledge
            self.do_inference(common_knowledge, private_knowledge)