from AttackField import AttackField
from mesa import Model
from mesa.time import StagedActivation
from Player import Player
from Deck import Deck

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
        self.players = []
        self.attack_fields = []
        self.num_players = num_players
        self.num_starting_cards = num_starting_cards
        self.schedule = StagedActivation(self) #TODO: Create the activation stages based on the game

        for i in range(self.num_players):
            # Create the attack fields
            self.attack_fields.append(AttackField())

        for i in range(self.num_players):
            # Create the players
            player = Player(i, self, self.attack_fields, self.num_players)
            self.players.append(player)
            self.schedule.add(player)

        # Create the discard pile
        self.discard_pile = []

        # Create the deck and shuffle it
        self.deck = Deck(num_suits, num_cards_per_suit)

        # Deal
        for i in range(self.num_starting_cards):
            for player in self.players:
                player.receive_card(self.deck.deal())


        # print(self.deck)
        # print(self.attack_fields)
        
        # for player in self.players:
        #     player.attack_field.add_card(self.deck.deal())
        
        # for player in self.players:
        #     print(str(player.id) + "'s attack field: " + str(player.attack_field))
        #     print(str(player.id) + "'s defence field: " + str(player.defence_field))

        # print(self.deck)

    def __repr__(self):
        '''
        Returns the representation of the entire model at the current state.
        '''
        return "Deck: " +
         str(self.deck) + "\n\nPlayers: " + str(self.players) + "\n\nAttack fields: " + str(self.attack_fields)



    def step(self):
        '''
        Advance the model by one step.
        '''
        self.schedule.step()


    def compare_cards(self, card1, card2):
        '''
        Compares two cards and returns the highest
        '''



m = DurakModel()
print(m)
m.step()