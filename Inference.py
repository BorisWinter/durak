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
        print(knowledge)
        print(card)
        for fact in knowledge:
            if fact.card == card:
                print("in here", fact.card)
                print(fact.owner_card)

                if fact.owner_card == other_player:
                    return True

        return False



    def from_C_to_K(self, common_knowledge, player):
        for fact in common_knowledge:
            if fact not in player.private_knowledge:
                player.private_knowledge.append(KnowledgeFact("K", player.id, fact.card, fact.owner_card))






    def do_inference(self, common_knowledge, private_knowledge, player, other, model):
        disjunct_knowledge = []
        full_deck = list(model.deck.initial_deck).copy()


        ## get the possible cards in someone's hand ###
        # a card can be in someone's hand if we don't
        ## know for sure that it is in someone
        # else's hand
        for card in full_deck:
            flag = 0
            for fact in private_knowledge:  # TODO this can probably be done with sets more efficiently but don't want to work it out rn
                if (fact.card == card):
                    flag = 1    # we know something about this card
                    if (fact.owner_card == other):  # if we know that the owner owns it, its ok
                        disjunct_knowledge.append(card)  # if we know that someone else's owns it, it cant be owned by the other player.
            if flag == 0:   # we don't know anything about this card, so it could be in the hand of the other player
                disjunct_knowledge.append(card)

        # probably inefficient as heelll
        player.private_disjunct_knowledge.append(KnowledgeDisjunct("K", player.id, disjunct_knowledge, other))

    def disjunct_elimination(self, common_knowledge, private_knowledge, player, other, model):
        for_sure_count = 0
        print("\tthis is player ", player.id, " 's own hand ", player.hand)
        print("\tthis is player ", player.id, " 's knowledge about player ", other)
        for fact in common_knowledge:
            #print("FACT ", fact)
            if fact.owner_card == other and type(fact.card) == int: ### THIS IS BAD REFACTOR THIS LATER!
                number_of_cards_of_other_player = fact.card
                single_fact_other, disjunct_fact_other = player.get_knowledge_about_other_player(other)

                print("\tplayer ", player.id, " knows that player ", other, " has ", number_of_cards_of_other_player, " cards")

                print("\tplayer ", player.id, " knows this for sure about player ", other, single_fact_other)
                print("\tplayer ", player.id, " considers these cards to be possible in ", other, " 's hand ", disjunct_fact_other)

                if type(disjunct_fact_other) == KnowledgeDisjunct:
                    player.private_disjunct_knowledge.remove(disjunct_fact_other)
                    # get the facts that we know for sure
                    for sure_card in single_fact_other:
                            if sure_card.card in disjunct_fact_other.card_list:
                                disjunct_fact_other.card_list.remove(sure_card.card)
                                for_sure_count += 1


                    if for_sure_count < number_of_cards_of_other_player:
                        print("\tplayer ", player.id, " is doubting between ", disjunct_fact_other.card_list, " in ", other, " 's hand ")
                        player.private_disjunct_knowledge.append(KnowledgeDisjunct("K", player.id, disjunct_fact_other.card_list, other)) # if we still have doubts we append
                        # here we know that we've eliminated everything
                        # we know for sure what the other one has
                    else:
                        print("\tplayer ", player.id, " knows for sure that ", player.get_private_single_knowledge_about_other_player(other), " in ", other, " 's hand ")


        print()


    def inference_for_players(self, model):
        #print("inference magic here (under construction)")

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
                    self.disjunct_elimination(common_knowledge, private_knowledge, player, other_player.id, model)

            ## reasoning from disjunct:
            # the other player owns X, Y and Z, and then the two empty spots can be filled with things in the disjunct