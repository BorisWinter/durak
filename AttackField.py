class AttackField():
    """
    Models an attack field in the game of Durak. 
    Each player has one attack field where they attack, and one where they defend
    """

    def __init__(self):
        '''
        Initializes the attack field. The field is given by a dictionary with attacking cards as keys and defending cards as values.
        '''
        self.cards = {}

    def __repr__(self):
        '''
        Returns the representation of the attack field
        '''
        return str(self.cards)

    def get_attacking_cards(self):
        '''
        Returns all cards that are currently attacking (the keys in the dictionary)
        '''
        return list(self.cards.keys())


    def get_defending_cards(self):
        '''
        Returns all cards that are currently defending (the values in the dictionary)
        '''
        return list(self.cards.values())


    def add_attack_card(self, card):
        '''
        Adds a card to the attack field if allowed.

        :param card: The card that should be added to the field
        '''
        self.cards[card]  = None
        # Only add if defender has enough cards to defend and the max is not yet present


    def add_defence_card(self, attacking_card, defending_card):
        '''
        Adds a card to the defence field if allowed.

        :param card: The card that should be added to the field
        '''
        self.cards[attacking_card]  = defending_card
