import random

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


    def get_random_card(self):
        '''
        Return a random card.
        '''
        return random.choice(self.get_cards_in_hand())


    def get_lowest_card(self, deck):
        '''
        Return the lowest card in the hand
        '''
        options = self.get_cards_in_hand()
        lowest_card = options[0]
        for card in options:
            if card.get_ranking() < lowest_card.get_ranking():
                lowest_card = card
        return lowest_card


    def get_highest_card(self):
        '''
        Return the highest card in the hand
        '''
        options = self.get_cards_in_hand()
        highest_card = options[0]
        for card in options:
            if card.get_ranking() > highest_card.get_ranking():
                highest_card = card
        return highest_card


    def get_lowest_card_that_wins_defence(self, attacking_card):
        '''
        Return the lowest card from the player's hand that beats the given card, if there is one.
        '''
        return_card = None
        options = self.get_cards_in_hand()
        for card in options:
            if card.get_ranking() < return_card.get_ranking() and card.get_ranking() >= attacking_card.get_ranking():
                return_card = card
        if return_card:
            return return_card
        else:
            return None


    def get_lowest_card_that_wins_attack(self, defending_card):
        '''
        Return the lowest card from the player's hand that beats the given card, if there is one.
        '''
        return_card = None
        options = self.get_cards_in_hand()
        for card in options:
            if card.get_ranking() < return_card.get_ranking() and card.get_ranking() >= defending_card.get_ranking():
                return_card = card
        if return_card:
            return return_card
        else:
            return None