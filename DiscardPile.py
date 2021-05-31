class DiscardPile():
    """
    Models the discard pile in the game of Durak. 
    """

    def __init__(self):
        '''
        Initializes the discard pile.
        '''
        self.cards = []

    def __repr__(self):
        '''
        Returns the representation of the discard pile.
        '''
        return str(self.cards)

    def get_all_cards(self):
        '''
        Returns all cards that have been discarded.
        '''
        return self.cards


    def add_card(self, card):
        '''
        Adds a card to the discard pile

        :param card: The card that should be added to the discard pile
        '''
        self.cards.append(card)