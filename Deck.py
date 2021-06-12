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
        self.ranking_order = []
        self.trump_suit = ""

        # Set the trump card
        self.trump_suit = self.deck[0].get_suit()
        self.trump_card = self.deck[0]

        # Create a deck of the right size
        for i in range(num_suits):
            for j in range(num_cards_per_suit):
                # Determine the ranking of the to be added card
                if Deck.AVAILABLE_SUITS[i] != self.trump_suit:
                    card_ranking = j
                else:
                    card_ranking = num_cards_per_suit + j

                self.deck.append(Card(Deck.AVAILABLE_SUITS[i], Deck.AVAILABLE_VALUES[j]), card_ranking)
                self.values.append(Deck.AVAILABLE_VALUES[j])
                self.suits.append(Deck.AVAILABLE_SUITS[i])

        self.initial_deck = self.deck.copy()

        

        # First add all non-trump cards to the ranking, then all trump cards
        # for i in range(num_cards_per_suit):
        #     rank = [card for card in self.deck if card.get_suit() != self.trump_suit and card.get_value() == Deck.AVAILABLE_VALUES[i]]
        #     self.ranking_order.append(rank)
        # for i in range(num_cards_per_suit):
        #     rank = [card for card in self.deck if card.get_suit() == self.trump_suit and card.get_value() == Deck.AVAILABLE_VALUES[i]]
        #     self.ranking_order.append(rank)

        # Shuffle the deck
        self.shuffle() ###-> turned off for debugging


        



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

    def get_trump_card(self):
        '''
        Returns the trump card of this game.
        '''
        return self.trump_card


    def get_card_at_location(self, index):
        '''
        Returns the card at a specified index in the deck.

        :param index: The index of the card whos value needs to be returned
        '''
        return self.deck[index]

    

