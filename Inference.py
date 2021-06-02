from KnowledgeFact import KnowledgeFact, KnowledgeDisjunct

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

    def other_owns_card(self, card, other_player, knowledge):
        for fact in knowledge:
            if type(fact) != KnowledgeDisjunct:
                if fact.card == card:
                    #print(fact.card, fact.owner_card, other_player)

                    if fact.owner_card == other_player:
                        return True
                    else:
                        return False

    def from_C_to_K(self, common_knowledge, player):
        for fact in common_knowledge:
            if fact not in player.private_knowledge:
                player.private_knowledge.append(KnowledgeFact("K", player.id, fact.card, fact.owner_card))






    def do_inference(self, common_knowledge, private_knowledge, player, other, model):
        new_knowledge = []
        disjunct_deck = list(model.deck.initial_deck).copy()

        for card in disjunct_deck:
            if not self.other_owns_card(card, other, private_knowledge):
                disjunct_deck.remove(card)


        # todo intersect with the number of cards that an agent has in their hand?
        # todo: does not take handlimit into account (yet)#
        # probably inefficient as heelll
        player.private_knowledge.append(KnowledgeDisjunct("K", player.id, disjunct_deck, other))

        # all possible facts in disjunction?
        disjunct_other = []
        return new_knowledge


    def inference_for_players(self, model):
        print("inference magic here (under construction)")

        common_knowledge = model.common_knowledge
        for player in model.players:
            private_knowledge = player.private_knowledge
            player_id = player.id

            # reason from common knowledge:
            self.from_C_to_K(common_knowledge, player)



            # reason about other agents
            for other_player in model.players:
                if other_player.id != player.id:    # other player
                    self.do_inference(common_knowledge, private_knowledge, player, other_player.id, model)