from AttackField import AttackField
from mesa import Model
from CustomStagedActivation import CustomStagedActivation
from Player import Player
from Deck import Deck
from DiscardPile import DiscardPile
from KnowledgeFact import KnowledgeFact
from Inference import Inference

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
        self.schedule = CustomStagedActivation(self)
        self.inference_engine = Inference()

        for i in range(self.num_players):
            # Create the attack fields
            self.attack_fields.append(AttackField())

        for i in range(self.num_players):
            # Create the players
            player = Player(i, self, self.attack_fields, self.num_players)
            self.players.append(player)
            self.schedule.add(player)

        # Create Common Knowledge
        self.common_knowledge = []

        # Create the discard pile
        self.discard_pile = DiscardPile()

        # Create the deck and shuffle it
        self.deck = Deck(num_suits, num_cards_per_suit)

        # Deal
        for i in range(self.num_starting_cards):
            for player in self.players:
                player.receive_card(self.deck.deal())

        # players know what card they have in their own hand
        for player in self.players:
            player.update_knowledge_own_hand()

        # Select starting attacker TODO: Change to player with lowest suit
        self.current_attacker = self.players[0]
        self.current_defender = self.players[1]

        # one-off action: trump card is common knowledge
        self.add_common_knowledge(self.deck.get_trump_card(), "deck")

        # get current private of knowledge of own hand


    def __repr__(self):
        '''
        Returns the representation of the entire model at the current state.
        '''
        return "---------STATE----------\n"\
            +"Deck: " + str(self.deck) \
                + "\nTrump suit: " + self.deck.trump_suit \
                + "\n\nCommon Knowledge: " + str(self.common_knowledge) \
                + "\n\nPlayers: " + str(self.players)\
                        + "\n\nAttack fields: " + str(self.attack_fields)\
                            + "\n\nDiscard pile: " + str(self.discard_pile)\
                                + "\n------------------------"


    def step(self):
        '''
        Advance the model by one step. In each step, the following happens:
        1. The current attacking player attacks
        2. The players update their knowledge.
        3. The current defending player defends.
        4. The attack is resolved and a winner is determined or the next attacker is chosen.
        5. The players update their knowledge.
        '''
        self.schedule.step(self, self.current_attacker.id, self.current_defender.id)




    def add_common_knowledge(self, card, position): # position is "deck", "attack", "defend", or "discard" (maybe players as well?)
        self.common_knowledge.append(KnowledgeFact("C", "", card, position))



    def return_winning_card(self, card1, card2):
        '''
        Compares two cards and returns the highest card or a tie
        '''
        value1 = self.deck.values.index(card1.get_value())
        suit1_trump = card1.get_suit() == self.deck.get_trump_suit()
        value2 = self.deck.values.index(card2.get_value())
        suit2_trump = card2.get_suit() == self.deck.get_trump_suit()

        if suit1_trump:
            if suit2_trump:
                if value1 > value2:
                    return card1
                else:
                    return card2
            else:
                return card1
        else:
            if suit2_trump:
                return card2
            else:
                if value1 > value2:
                    return card1
                elif value1 < value2:
                    return card2
                else:
                    return "tie"


    def resolve_attack(self, attacker_key, defender_key):
        '''
        Resolve the attack from the given attacker.

        :param attacker: The attacker in the attack
        '''
        attacker = self.players[attacker_key]
        defender = self.players[defender_key]
        field = attacker.get_attack_field()
        attack_cards = field.get_attacking_cards()
        defence_cards = field.get_defending_cards()
        attacker_wins = False

        # The attacker wins if the defender cannot place enough cards or if they defeat one of the defender's cards
        if len(attack_cards) > len(defence_cards):
            attacker_wins = True
        elif len(attack_cards) < len(defence_cards):
            print("ERROR: Defender placed more cards than attacker.")
        else:
            for i, attack_card in enumerate(attack_cards):
                if self.return_winning_card(attack_card, defence_cards[i]) == attack_card:
                    attacker_wins = True
        
        if attacker_wins:
            # Defender gets the cards if attacker wins
            for attack_card in attack_cards:
                defender.receive_card(attack_card)

                self.add_common_knowledge(attack_card, defender.id) # add common knowledge that cards go to loser

            for defend_card in defence_cards:
                defender.receive_card(defend_card)

                self.add_common_knowledge(defend_card, defender.id)



            print("Player " + str(attacker_key) + " won! The cards go to player " + str(defender_key))
        else:
            # Discard pile gets the cards otherwise
            for attack_card in attack_cards:
                self.discard_pile.add_card(attack_card)
                self.add_common_knowledge(attack_card, "discard")

            for defend_card in defence_cards:
                self.discard_pile.add_card(defend_card)
                self.add_common_knowledge(defend_card, "discard")   # maybe put this in a function

            print("Player " + str(defender_key) + " won! The cards go to the discard pile!")
        
        # Clear the attack field
        field.clear()
       
                

def play(m):
    '''
    Play a game of Durak until there is a winner

    :param m: The model to play the game with
    '''



    # while not m.deck.is_empty():
    m.step()
    print(m)


    # Currently stops with an error b/c winning conditions still need to be implemented




m = DurakModel()
print("Starting state...")
print(m)
print("Play! ")
play(m)

# print(m.return_winning_card(m.players[0].hand.get_cards_in_hand()[0], m.players[1].hand.get_cards_in_hand()[0]))