class Card():
    """
    Models a card from a standard deck of cards
    """

    def __init__(self, suit, value):
        '''
        Initializes the card
        '''
        self.suit = suit
        self.value = value

    def __repr__(self):
        '''
        Returns the representation of the card
        '''
        return (self.value + " OF " + self.suit)

    def get_suit(self):
        '''
        Returns the suit of the card
        '''
        return self.suit

    def get_value(self):
        '''
        Returns the value of the card
        '''
        return self.value