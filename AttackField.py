class AttackField():
    """
    Models an attack field in the game of Durak. 
    Each player has one attack field where they attack, and one where they defend
    """

    def __init__(self):
        '''
        Initializes the attack field.
        '''
        self.cards = []

    def __repr__(self):
        '''
        Returns the representation of the attack field
        '''
        return str(self.cards)

    def add_card(self, card):
        '''
        Adds a card to the attack field if allowed.

        :param card: The card that should be added to the field
        '''
        self.cards.append(card)
        # Only add if defender has enough cards to defend and the max is not yet present