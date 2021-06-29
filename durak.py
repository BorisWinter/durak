from AttackField import AttackField
from mesa import Model
from CustomStagedActivation import CustomStagedActivation
from Player import Player
from Deck import Deck
from DiscardPile import DiscardPile
from KnowledgeFact import KnowledgeFact
from Inference import Inference
import random
from newKripke import *


class DurakModel(Model):
    """A model for the game of Durak with some number of players."""

    def __init__(
            self,
            multiple={},
            num_players=2,
            num_suits=2,
            num_cards_per_suit=2,
            num_starting_cards=1,
            player_strategies=["normal", "normal"],
            player_depths=[1, 1],
            verbose=True,
            multiple_runs=False):
        '''
        Initialize the game
        :param num_players: The number of players for this game
        :param num_suits: The number of suits being played with
        :param num_cards_per_suit: The number of cards per suit
        :param num_starting_cards: The number of cards that each player starts with
        '''

        if multiple:
            '''
            When running multiple games, all this is passed from experiments.ipynb
            This makes running games with the same settings significantly faster
            '''
            self.players = []
            self.winners = []
            self.durak = None
            self.attack_fields = []

            self.player_strategies = multiple["player_strategies"]
            self.player_depths = multiple["player_depths"]
            self.num_players = multiple["num_players"]
            self.num_suits = multiple["num_suits"]
            self.num_cards_per_suit = multiple["num_cards_per_suit"]
            self.num_starting_cards = multiple["num_starting_cards"]
            self.schedule = CustomStagedActivation(self)
            self.verbose = verbose

            for i in range(self.num_players):
                # Create the attack fields
                self.attack_fields.append(AttackField())

            for i in range(self.num_players):
                # Create the players
                player = Player(i, self, self.attack_fields, self.num_players, self.player_strategies[i],
                                self.player_depths[i])
                self.players.append(player)
                self.schedule.add(player)

            for player in self.players:
                # Set the order of play
                player.set_next_player(self.players[(player.get_id() + 1) % num_players])
                player.set_previous_player(self.players[(player.get_id() - 1) % num_players])

            # Create the discard pile
            self.discard_pile = DiscardPile()

            # Create the deck and shuffle it
            self.deck = Deck(num_suits, num_cards_per_suit)

            self.kripke_deck = []
            self.kripke_discard_pile = []
            self.kripke_players = []
            self.kripke_card_locations = []
            self.kripke_worlds = None
            self.kripke_model = None
            self.reachable_worlds = None

        else:
            '''
            Initialize all these values if we run a single game
            '''
            self.players = []
            self.player_strategies = player_strategies
            self.player_depths = player_depths
            self.winners = []
            self.durak = None
            self.attack_fields = []
            self.num_players = num_players
            self.num_suits = num_suits
            self.num_cards_per_suit = num_cards_per_suit
            self.num_starting_cards = num_starting_cards
            self.schedule = CustomStagedActivation(self)
            # self.inference_engine = Inference(verbose)
            self.verbose = verbose

            for i in range(self.num_players):
                # Create the attack fields
                self.attack_fields.append(AttackField())

            for i in range(self.num_players):
                # Create the players
                player = Player(i, self, self.attack_fields, self.num_players, self.player_strategies[i],
                                self.player_depths[i])
                self.players.append(player)
                self.schedule.add(player)

            for player in self.players:
                # Set the order of play
                player.set_next_player(self.players[(player.get_id() + 1) % num_players])
                player.set_previous_player(self.players[(player.get_id() - 1) % num_players])

            # Create the discard pile
            self.discard_pile = DiscardPile()

            # Create the deck and shuffle it
            self.deck = Deck(num_suits, num_cards_per_suit)

            # Create the initial Kripke model with all players and all cards in the deck
            self.kripke_deck = [str(c) for c in self.deck.deck]
            self.kripke_discard_pile = [str(c) for c in self.discard_pile.cards]
            self.kripke_players = [str(p.get_id()) for p in self.players]
            self.kripke_card_locations = ["Deck", "Discard"]
            self.kripke_card_locations.extend(self.kripke_players)
            self.kripke_worlds = gen_worlds(self.kripke_deck, self.kripke_card_locations, self.kripke_players,
                                            self.num_starting_cards)
            self.kripke_model, self.reachable_worlds = gen_empty_kripke(self.kripke_worlds, self.kripke_players)

            '''
            This part of the initalization happens for every game, no matter how it was run. 
            '''
            # Deal
            for i in range(self.num_starting_cards):
                for player in self.players:
                    player.receive_card(self.deck.deal())

            # Select a random starting attacker and set the defender
            self.current_attacker = random.choice(self.players)
            self.current_defender = self.current_attacker.get_next_player()

        # Add the starting card knowledge to the Kripke model
        for player in self.players:
            print("Updating model at start of game")
            kripke_player = str(player.get_id())
            statement = make_statement_cards(self.deck.initial_deck, [kripke_player + str(c) for c in player.hand.get_cards_in_hand()], kripke_player,
                                             True, len(self.deck.deck), len(self.discard_pile.cards))
            # print("\t Statement:", statement)
            # print("cards are", player.hand.get_cards_in_hand())
            self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                                                                 statement, self.reachable_worlds)

    def __repr__(self):
        '''
        Returns the representation of the entire model at the current state.
        '''
        return "---------STATE----------\n" \
               + "Deck: " + str(self.deck) \
               + "\nTrump suit: " + self.deck.trump_suit \
               + "\n\nWinners: " + str(self.winners) \
               + "\n\nPlayers: " + str(self.players) \
               + "\n\nAttack fields: " + str(self.attack_fields) \
               + "\n\nDiscard pile: " + str(self.discard_pile) \
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

    def add_common_knowledge(self, card,
                             position):  # position is "deck", "attack", "defend", or "discard" (maybe players as well?)
        self.common_knowledge.append(KnowledgeFact("C", "", card, position))

    def add_common_knowledge_num(self, num, position):  # every player knows how many cards are where
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

        Returns the Durak if there is one, else None
        '''
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

        # Resolving of the attack if the attacker wins
        if attacker_wins:
            if self.verbose:
                print("Player " + str(attacker.get_id()) + " won! The cards go to player " + str(defender.get_id()))
                print("------------------------")
            # Defender gets the cards if attacker wins
            for attack_card in attack_cards:
                defender.receive_card(attack_card)
            for defend_card in defence_cards:
                defender.receive_card(defend_card)

            # Update the knowledge of all players
            for player in self.players:
                kripke_player = str(player.get_id())
                kripke_defender = str(defender.get_id())
                kripke_attacker = str(attacker.get_id())
                kripke_attack_card = str(attack_card)
                kripke_defence_card = str(defend_card)

                # known_cards_attacker = list(player_knows_cards_of_player(player, self.reachable_worlds, kripke_attacker))
                # known_cards_attacker.remove(kripke_attacker + kripke_attack_card)
                # statement = make_statement_cards(self.deck.initial_deck, known_cards_list, kripke_player,
                #                                  len(self.deck.deck), len(self.discard_pile.cards))
                #
                # self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                #                                                      statement, self.reachable_worlds)
                # self.kripke_model, self.reachable_worlds = remove_links(self.kripke_model, kripke_player,
                #                                                         statement, self.reachable_worlds)
                print("Updating model after unsuccessful defense")
                # known_cards_defender = list(player_knows_cards_of_player(player, self.reachable_worlds, kripke_defender))
                known_cards_defender = list(knowledge_base(player, self.reachable_worlds))
                known_cards_defender.append(kripke_defender + kripke_defence_card)
                known_cards_defender.append(kripke_defender + kripke_attack_card)
                # print("YOEEEEEEEEEEEEEEEEEEEHOEEEEEEEEEEEEEEEEEEEEEEE", known_cards_defender)
                statement = make_statement_cards(self.deck.initial_deck, known_cards_defender, kripke_defender,
                                                 False, len(self.deck.deck), len(self.discard_pile.cards))
                statement = And(statement, Not(Atom(kripke_attacker + kripke_attack_card)))
                # print("\t Statement:", statement)

                self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                                                                     statement, self.reachable_worlds)
                self.kripke_model, self.reachable_worlds = remove_links(self.kripke_model, kripke_player,
                                                                        statement, self.reachable_worlds)
            print("------------------------")

        # Resolving of the attack if the defender wins
        else:
            if self.verbose:
                print("Player " + str(defender.get_id()) + " won! The cards go to the discard pile!")
                print("------------------------")
            # Discard pile gets the cards otherwise
            for attack_card in attack_cards:
                self.discard_pile.add_card(attack_card)
            for defend_card in defence_cards:
                self.discard_pile.add_card(defend_card)

            # Update the knowledge of all players
            # --> REMOVE relations to all worlds where the discard pile does not have those cards
            for player in self.players:
                kripke_player = str(player.get_id())
                kripke_attacker = str(attacker.get_id())
                kripke_defender = str(defender.get_id())
                kripke_discard_pile = "Discard"
                kripke_attack_card = str(attack_card)
                kripke_defence_card = str(defend_card)

                # known_cards_attacker = list(player_knows_cards_of_player(player, self.reachable_worlds, kripke_attacker))
                # print("testing...")
                # if (kripke_attacker + kripke_attack_card) in known_cards_attacker:
                #     known_cards_attacker.remove(kripke_attacker + kripke_attack_card)
                #     statement = make_statement_cards(self.deck.initial_deck, known_cards_attacker, kripke_player,
                #                                      len(self.deck.deck), len(self.discard_pile.cards))
                #
                #     self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                #                                                          statement, self.reachable_worlds)
                #     self.kripke_model, self.reachable_worlds = remove_links(self.kripke_model, kripke_player,
                #                                                             statement, self.reachable_worlds)

                print("Updating model after successful defense")

                # known_cards_discard = list(player_knows_cards_of_player(player, self.reachable_worlds, kripke_discard_pile))
                known_cards_discard = list(knowledge_base(player, self.reachable_worlds))
                # print("known cards on discard pile:", known_cards_discard)
                known_cards_discard.append(kripke_discard_pile + kripke_defence_card)
                known_cards_discard.append(kripke_discard_pile + kripke_attack_card)
                # print("\t\t\t now We know: ", known_cards_discard)
                statement = make_statement_cards(self.deck.initial_deck, known_cards_discard, kripke_discard_pile,
                                                 False, len(self.deck.deck), len(self.discard_pile.get_all_cards()))


                # statement.append(Not(Atom(kripke_attacker + kripke_attack_card)))
                statement = And(statement, Not(Atom(kripke_attacker + kripke_attack_card)))
                statement = And(statement, Not(Atom(kripke_defender + kripke_defence_card)))
                # print("\t Statement:", statement)

                self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                                                                     statement, self.reachable_worlds)
                self.kripke_model, self.reachable_worlds = remove_links(self.kripke_model, kripke_player,
                                                                        statement, self.reachable_worlds)
                # print("\t\t\t AFTER UPDATING")
                # now_known = list(player_knows_cards_of_player(player, self.reachable_worlds, kripke_discard_pile))

                # self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                #                                                      Atom(kripke_discard_pile + kripke_attack_card),
                #                                                      self.reachable_worlds)
                # self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                #                                                      Atom(kripke_discard_pile + kripke_defence_card),
                #                                                      self.reachable_worlds)
                # self.kripke_model, self.reachable_worlds = remove_links(self.kripke_model, kripke_player,
                #                                                         Atom(kripke_discard_pile + kripke_attack_card),
                #                                                         self.reachable_worlds)
                # self.kripke_model, self.reachable_worlds = remove_links(self.kripke_model, kripke_player,
                #                                                         Atom(kripke_discard_pile + kripke_defence_card),
                #                                                         self.reachable_worlds)
            print("------------------------")

        # If the deck is empty, no cards can be taken: check if there are winners
        if self.deck.is_empty():
            # Check if the attacking player has won the game
            if attacker.hand.is_empty():

                # Make the attack fields match the new situation
                defender.set_defence_field(attacker.get_defence_field())

                # Make the turns match the new situation
                attacker.get_previous_player().set_next_player(defender)
                defender.set_previous_player(attacker.get_previous_player())

                if self.verbose:
                    print("Player " + str(attacker.get_id()) + " has won the game!!")
                self.winners.append(attacker)
                self.players.remove(attacker)

                # Check if the game is over
                if len(self.players) == 1:
                    if self.verbose:
                        print("Player " + str(defender.get_id()) + " has lost the game and is now the DURAK!!")
                    return defender

            # Check if the defending player has won the game
            if defender.hand.is_empty():
                if self.verbose:
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
                    if attacker in self.winners:
                        return defender.get_next_player()
                    else:
                        if self.verbose:
                            print("Player " + str(defender.get_id()) + " has lost the game and is now the DURAK!!")
                        return attacker

        # The deck is not empty
        else:
            # Take cards if needed
            num_cards_attacker = len(attacker.hand.get_cards_in_hand())
            num_cards_defender = len(defender.hand.get_cards_in_hand())
            if num_cards_attacker < self.num_starting_cards:
                attacker.take_cards_from_deck(self, self.num_starting_cards - num_cards_attacker)

                # Update the knowledge of attacker
                kripke_player = str(attacker.get_id())
                print("Updating model after attacker draws")
                statement = make_statement_cards(self.deck.initial_deck, [kripke_player + str(c) for c in attacker.hand.get_cards_in_hand()],
                                                 kripke_player, False, len(self.deck.deck), len(self.discard_pile.cards))

                # print("\t Statement:", statement)
                self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                                                                     statement, self.reachable_worlds)
                self.kripke_model, self.reachable_worlds = remove_links(self.kripke_model, kripke_player,
                                                                        statement, self.reachable_worlds)

            # After the attacker has taken enough cards, check if the deck is now empty and the defender has won
            if self.deck.is_empty():
                if defender.hand.is_empty():
                    if self.verbose:
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
                        return attacker

            if num_cards_defender < self.num_starting_cards:
                defender.take_cards_from_deck(self, self.num_starting_cards - num_cards_defender)
                # Update the knowledge of defender
                print("Updating knowledge after defender draws")
                kripke_player = str(defender.get_id())
                statement = make_statement_cards(self.deck.initial_deck, [kripke_player + str(c) for c in defender.hand.get_cards_in_hand()],
                                                 kripke_player, False, len(self.deck.deck), len(self.discard_pile.cards))
                # print("\t Statement:", statement)

                self.kripke_model, self.reachable_worlds = add_links(self.kripke_model, kripke_player,
                                                                     statement, self.reachable_worlds)
                self.kripke_model, self.reachable_worlds = remove_links(self.kripke_model, kripke_player,
                                                                        statement, self.reachable_worlds)

        # Determine who's turn it is now
        if attacker_wins:
            self.current_attacker = defender.get_next_player()
            self.current_defender = defender.get_next_player().get_next_player()
            if self.verbose:
                print("It is now player " + str(self.current_attacker.get_id()) + "'s turn")
        else:
            if defender.hand.is_empty():
                self.current_attacker = defender.get_next_player()
                self.current_defender = defender.get_next_player().get_next_player()
            else:
                self.current_attacker = defender
                self.current_defender = defender.get_next_player()
                if self.verbose:
                    print("It is now player " + str(self.current_attacker.get_id()) + "'s turn")

        # Clear the attack field
        field.clear()

        # Return None if there is no Durak yet
        return None

    def test(self):
        print("GAME STATE")
        print(self.players)

        for player in self.players:
            print(player.hand.get_cards_in_hand())

        print("END GAME STATE")

    def set_durak(self, durak):
        '''
        Sets the Durak.
        '''
        self.durak = durak

    def get_game_data(self):
        '''
        Returns the current state of the game.
        '''
        game_state = {
            "num_players": self.num_players,
            "num_suits": self.num_suits,
            "num_cards_per_suit": self.num_cards_per_suit,
            "num_starting_cards": self.num_starting_cards,
            "durak": self.durak.get_id(),
            "winners": [winner.get_id() for winner in self.winners],
            "player_strategies": self.player_strategies,
            "player_depths": self.player_depths
        }

        return game_state


def play(m):
    '''
    Play a game of Durak until there is a winner

    :param m: The model to play the game with
    '''

    while not m.durak:
        print(m)
        m.step()
    print(m)

    return m.get_game_data()


m = DurakModel(verbose=True)
# print("Starting state...")
# print(m)
# print("Play! ")
play(m)
