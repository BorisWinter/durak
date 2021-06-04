class KnowledgeFact:

    def __init__(self, operator, player, card, owner_card):
        self.operator = operator    # C or K or I or whatever
        self.player = player        # K_player.
        self.card = card              # knowledge fact, can't be nested!

        self.owner_card = owner_card

    def __repr__(self):
        return self.operator + "_"+str(self.player) +" "+ str(self.card) + "_"+str(self.owner_card)

    def __eq__(self, other):
        return self.operator == other.operator and self.player == other.player and self.card == other.card and self.owner_card == other.owner_card


class KnowledgeDisjunct:

    def __init__(self, operator, player, card_list, owner_card):
        self.operator = operator    # C or K or I or whatever
        self.player = player        # K_player.
        self.card_list = card_list              # knowledge fact, can't be nested!
        self.owner_card = owner_card

    def __eq__(self, other):
        return self.operator == other.operator and self.player == other.player and self.card_list == other.card_list and self.owner_card == other.owner_card

    def __repr__(self):
        return self.operator + "_"+str(self.player) +" "+ str(self.card_list) + "_"+str(self.owner_card)

class KnowledgeConjunct:
    # this class combines
    pass


