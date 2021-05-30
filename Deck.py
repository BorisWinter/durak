import random
from Card import Card

class Deck():
    """
    Models the deck in the game of Durak
    """

    AVAILABLE_SUITS = ["DIAMONDS", "CLUBS", "HEARTS", "SPADES"]
    AVAILABLE_VALUES =["TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING", "ACE"]

    def __init__(self, num_suits, num_cards_per_suit):
        '''
        Initializes the deck by creating it, shuffling it, and drawing a trump card

        :param num_suits: The number of suits in the deck
        :param num_cards_per_suit: The number of cards from each suit
        '''

        self.values = []
        self.suits = []
        self.deck = []
        self.trump_suit = ""

        # Create a deck of the right size, and determine the ranking order of the cards
        for i in range(num_suits):
            for j in range(num_cards_per_suit):
                self.deck.append(Card(Deck.AVAILABLE_SUITS[i], Deck.AVAILABLE_VALUES[j]))
                self.values.append(Deck.AVAILABLE_VALUES[j])
                self.suits.append(Deck.AVAILABLE_SUITS[i])
        
        # Shuffle the deck
        self.shuffle()

        # Set the trump card
        self.trump_suit = self.deck[0].get_suit()


    def __repr__(self):
        '''
        Returns the representation of the deck.
        '''
        return str(self.deck)


    def is_empty(self):
        '''
        Returns True if the deck is empty and False otherwise.
        '''
        if self.deck:
            return False
        else:
            return True


    def shuffle(self):
        '''
        Shuffles the deck.
        '''
        random.shuffle(self.deck)
        

    def deal(self):
        '''
        Returns and removes the top card of the deck.
        '''
        if self.deck:
            return self.deck.pop()


    def get_trump_suit(self):
        '''
        Returns the trump suit of this game.
        '''
        return self.trump_suit


    def get_card_at_location(self, index):
        '''
        Returns the card at a specified index in the deck.

        :param index: The index of the card whos value needs to be returned
        '''
        return self.deck[index]

    

