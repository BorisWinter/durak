from mesa import Model
from mesa.time import StagedActivation
from DurakPlayer import DurakPlayer
from DurakDeck import DurakDeck

class DurakModel(Model):
    """A model for the game of Durak with some number of players."""

    def __init__(
        self, 
        num_players = 3,
        num_suits = 3,
        num_cards_per_suit = 3,
        num_starting_cards = 2):
        '''
        Initialize the game
        :param num_players: The number of players for this game
        :param num_suits: The number of suits being played with
        :param num_cards_per_suit: The number of cards per suit
        :param num_starting_cards: The number of cards that each player starts with
        '''
        self.num_players = num_players
        self.num_starting_cards = num_starting_cards
        self.schedule = StagedActivation(self) #TODO: Create the activation stages based on the game

        # Create agents
        for i in range(self.num_players):
            a = DurakPlayer(i, self)
            self.schedule.add(a)

        # Create the deck, shuffle it, and deal 
        deck = DurakDeck(num_suits, num_cards_per_suit)
        print(deck)



    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

m = DurakModel()
m.step()