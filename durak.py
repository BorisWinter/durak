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
        num_starting_cards = 1):
        '''
        Initialize the game
        :param num_players: The number of players for this game
        :param num_suits: The number of suits being played with
        :param num_cards_per_suit: The number of cards per suit
        :param num_starting_cards: The number of cards that each player starts with
        '''
        self.players = []
        self.winners = []
        self.durak = None
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

        for player in self.players:
            # Set the order of play
            player.set_next_player(self.players[(player.get_id() + 1) % num_players])
            player.set_previous_player(self.players[(player.get_id() - 1) % num_players])

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



    def __repr__(self):
        '''
        Returns the representation of the entire model at the current state.
        '''
        return "---------STATE----------\n"\
            +"Deck: " + str(self.deck) \
                + "\nTrump suit: " + self.deck.trump_suit \
                    + "\n\nCommon Knowledge: " + str(self.common_knowledge) \
                        + "\n\nWinners: " + str(self.winners)\
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
        self.schedule.step(self, self.current_attacker, self.current_defender)




    def add_common_knowledge(self, card, position): # position is "deck", "attack", "defend", or "discard" (maybe players as well?)
        self.common_knowledge.append(KnowledgeFact("C", "", card, position))

    def add_common_knowledge_num(self, num, position): # every player knows how many cards are where
        self.common_knowledge.append(KnowledgeFact("C", "", num, position))

    def remove_old_hand_num_knowledge(self, knowledge):
        to_remove = []
        for fact in knowledge:
            if type(fact.card) == int:  # BAD! REFACTOR!
                to_remove.append(fact)
        return to_remove

    def resolve_discard_pile(self):
        pass



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


    def resolve_attack(self, attacker, defender):
        '''
        Resolve the attack from the given attacker.

        :param attacker: The attacker in the attack
        '''
        # attacker = self.players[attacker_key]
        # defender = self.players[defender_key]
        field = attacker.get_attack_field()
        attack_cards = field.get_attacking_cards()
        defence_cards = field.get_defending_cards()
        attacker_wins = False
        to_remove = []

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
            print("Player " + str(attacker.get_id()) + " won! The cards go to player " + str(defender.get_id()))
            # Defender gets the cards if attacker wins
            for attack_card in attack_cards:
                defender.receive_card(attack_card)

                for fact in self.common_knowledge:
                    if fact.card == attack_card and fact.owner_card != defender.get_id():
                        to_remove.append(fact)

                self.add_common_knowledge(attack_card, defender.id) # add common knowledge that cards go to loser

            for defend_card in defence_cards:
                defender.receive_card(defend_card)

                for fact in self.common_knowledge:
                    if fact.card == defend_card and fact.owner_card != defender.get_id():
                        to_remove.append(fact)

                self.add_common_knowledge(defend_card, defender.id)

        else:
            print("Player " + str(defender.get_id()) + " won! The cards go to the discard pile!")
            # Discard pile gets the cards otherwise

            for attack_card in attack_cards:
                self.discard_pile.add_card(attack_card)

                for fact in self.common_knowledge:
                    if fact.card == attack_card and fact.owner_card != "discard":
                        to_remove.append(fact)

                self.add_common_knowledge(attack_card, "discard")

            for defend_card in defence_cards:
                self.discard_pile.add_card(defend_card)

                for fact in self.common_knowledge:
                    if fact.card == defend_card and fact.owner_card != "discard":
                        to_remove.append(fact)

                self.add_common_knowledge(defend_card, "discard")   # maybe put this in a function


            for fact in to_remove:
                self.common_knowledge.remove(fact)

        if self.deck.is_empty():
            # Check if the attacking player has won the game
            if attacker.hand.is_empty():

                # Make the attack fields match the new situation
                defender.set_defence_field(attacker.get_defence_field())

                # Make the turns match the new situation
                attacker.get_previous_player().set_next_player(defender)
                defender.set_previous_player(attacker.get_previous_player())

                print("Player " + str(attacker.get_id()) + " has won the game!!")
                self.winners.append(attacker)
                self.players.remove(attacker)

                # Check if the game is over
                if len(self.players) == 1:
                    print("Player " + str(defender.get_id()) + " has lost the game and is now the DURAK!!")
                    self.durak = defender
        
            # Check if the defending player has won the game
            if defender.hand.is_empty():
                print("Player " + str(defender.get_id()) + " has won the game!!")

                # Make the attack fields match the new situation
                attacker.set_attack_field(defender.get_attack_field())

                # Make the turns match the new situation
                attacker.set_next_player(defender.get_next_player())
                defender.get_next_player().set_previous_player(attacker)

                self.winners.append(defender)
                self.players.remove(defender)

                # Check if the game is over
                if len(self.players) == 1:
                    self.durak = attacker


        # Take cards if needed
        num_cards_attacker = len(attacker.hand.get_cards_in_hand())
        num_cards_defender = len(defender.hand.get_cards_in_hand())
        if num_cards_attacker < self.num_starting_cards:
            attacker.take_cards_from_deck(self, self.num_starting_cards - num_cards_attacker)
        if num_cards_defender < self.num_starting_cards:
            defender.take_cards_from_deck(self, self.num_starting_cards - num_cards_defender)

        ## every player knows how many cards every player/location has
        # first remove all old common knowledge about hand limit

        common_to_remove = self.remove_old_hand_num_knowledge(self.common_knowledge)
        for item in common_to_remove:
            self.common_knowledge.remove(item)



        for player in self.players:
            # remove knowledge about old hands from players
            player_to_remove = self.remove_old_hand_num_knowledge(player.private_knowledge)
            for item in player_to_remove:
                player.private_knowledge.remove(item)

            num = player.get_number_of_cards_in_hand()
            player_id = player.id
            self.add_common_knowledge_num(num, player_id)

        self.add_common_knowledge_num(len(self.deck.deck), "deck") # the players also know the number of cards in a deck


        # Determine who's turn it is now

        if attacker_wins:
            self.current_attacker = defender.get_next_player()
            self.current_defender = defender.get_next_player().get_next_player()
            print("It is now player " + str(self.current_attacker.get_id()) + "'s turn")
        else:
            if defender.hand.is_empty():
                self.current_attacker = defender.get_next_player()
                self.current_defender = defender.get_next_player().get_next_player()
            else:
                self.current_attacker = defender
                self.current_defender = defender.get_next_player()
                print("It is now player " + str(self.current_attacker.get_id()) + "'s turn")
        
        # Clear the attack field
        field.clear()




def play(m):
    '''
    Play a game of Durak until there is a winner

    :param m: The model to play the game with
    '''



    while not m.durak:
        m.step()   
        print(m)


    # Currently stops with an error b/c winning conditions still need to be implemented



m = DurakModel()
print("Starting state...")
print(m)
print("Play! ")
play(m)

# print(m.return_winning_card(m.players[0].hand.get_cards_in_hand()[0], m.players[1].hand.get_cards_in_hand()[0]))