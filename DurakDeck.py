import random

class DurakDeck():
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
        self.num_suits = num_suits
        self.num_cards_per_suit = num_cards_per_suit
        self.num_cards = self.num_suits * self.num_cards_per_suit
        self.deck = []

        # Create a deck of the right size, and determine the ranking order of the cards
        for i in range(num_suits):
            for j in range(num_cards_per_suit):
                self.deck.append(Card(DurakDeck.AVAILABLE_SUITS[i], DurakDeck.AVAILABLE_VALUES[j]))

        self.value_ranking_order = DurakDeck.AVAILABLE_VALUES[:num_cards_per_suit]

    def __repr__(self):
        '''
        Returns the representation of the deck
        '''
        return str(self.deck)


    def shuffle(self):
        '''
        Shuffles the deck
        '''
        random.shuffle(self.deck)


    def assign_trump_suit(self):
        '''

        '''
        

    def draw_top_card(self):
        '''
        Returns and removes the top card of the deck
        '''
        return self.deck.pop()

        
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

