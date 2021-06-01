class Hand():
    """
    Models the hand of a player.
    """

    def __init__(self, player):
        '''
        Initializes the hand

        :param player: The player to whom the hand belongs
        '''
        self.player = player
        self.cards = []


    def __repr__(self):
        '''
        Returns the representation of the hand.
        '''
        return str(self.cards)


    def is_empty(self):
        '''
        Returns True if the hand is empty and False otherwise.
        '''
        if self.cards:
            return False
        else:
            return True
        

    def get_cards_in_hand(self):
        '''
        Returns a list with all cards in the hand
        '''
        return self.cards


    def add_card(self, card):
        '''
        Adds a card to the hand.

        :param card: The card that should be added to the hand
        '''
        self.cards.append(card)
        

    def remove_card(self, card):
        '''
        Removes the specified card from the hand

        :param card: The card that should be removed from the hand
        '''
        if card in self.cards:
            self.cards.remove(card)