from AttackField import AttackField
from mesa import Agent
from Hand import Hand
from KnowledgeFact import KnowledgeFact, KnowledgeDisjunct
import Moves
import random
from ourKripke import *

class Player(Agent):
    """
    Models a player in the game of Durak
    """

    def __init__(self, unique_id, model, attack_fields, num_players, strategy, knowledge_depth):
        super().__init__(unique_id, model)
        self.id = unique_id
        self.hand = Hand(self.id)
        self.attack_field = attack_fields[self.id]
        self.defence_field = attack_fields[(self.id - 1) % num_players]
        self.strategy = strategy
        self.knowledge_depth = knowledge_depth

    def __repr__(self):
        '''
        Returns the representation of the player.
        '''
        return "\n Player " + str(self.id) + "\n\t Hand : " + str(self.hand) + "\n"


    def get_number_of_cards_in_hand(self):
        '''
        Returns the number of cards in the player's hand
        '''
        return len(self.hand.cards)

    def step(self):
        '''
        '''
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        # print ("Hi, I am player " + str(self.unique_id) +".")

        self.update_knowledge_own_hand()

        self.attack()


    def get_id(self):
        '''
        Returns the id of this player
        '''
        return self.id


    def get_next_player(self):
        '''
        Returns the next player after this one
        '''
        return self.next_player


    def set_next_player(self, player):
        '''
        Sets the next player after this one
        '''
        self.next_player = player


    def get_previous_player(self):
        '''
        Returns the previous player
        '''
        return self.previous_player


    def set_previous_player(self, player):
        '''
        Sets the previous player
        '''
        self.previous_player = player

        
    def get_attack_field(self):
        '''
        Returns the attack field of this player
        '''
        return self.attack_field


    def set_attack_field(self, field):
        '''
        Sets the attack field of this player
        '''
        self.attack_field = field


    def get_defence_field(self):
        '''
        Returns the defence field of this player
        '''
        return self.defence_field


    def set_defence_field(self, field):
        '''
        Sets the defence field of this player
        '''
        self.defence_field = field


    def receive_card(self, card):
        '''
        Adds the specified card to the hand of the player
        '''
        self.hand.add_card(card)

    
    def attack(self):
        '''
        Choose on or more cards and attack with them.
        '''

        # Choose a card to play
        if self.strategy == "random":
            card = random.choice(self.hand.get_cards_in_hand())
        elif self.strategy == "normal":
            #--------- Depth 1 ----------#
            if self.knowledge_depth == 1:
                
                this_player = str(self.get_id())
                defending_player = str(self.get_next_player().get_id())
                # defenders_cards = self.model.kripke_model.player_knows_cards_of_player(this_player, defending_player)
                defenders_cards = []
                # TODO: convert the string cards to actual cards
                highest_defending_card = None
                for c in defenders_cards:
                    if c.get_rank() > highest_defending_card.get_rank():
                        highest_defending_card = c

                if highest_defending_card:
                    winning_card = self.hand.get_lowest_card_that_wins_attack(highest_defending_card)
                    if winning_card:
                        card = winning_card
                    else:
                        card = self.hand.get_lowest_card() # NO = Play your lowest card

                else:
                    # You DONT know one or more cards of the defender
                    if self.get_next_player().get_number_of_cards_in_hand() == 1: # NO = Does the defender only have one card?
                        card = self.hand.get_highest_card() # YES = Play your highest card
                    else:
                        card = self.hand.get_lowest_card() # NO = Play your lowest card


        # Play the card(s)
        if card in self.hand.get_cards_in_hand():
            self.attack_field.add_attack_card(card)
            self.hand.remove_card(card)

        # Update the knowledge of the defender
        # --> REMOVE all worlds where the attacker does not have that card
        kripke_attacker = str(self.get_id())
        kripke_defender = str(self.get_next_player().get_id())
        kripke_card = str(card)
        remove_links(self.model.kripke_model, kripke_defender, Atom(kripke_attacker + kripke_card), self.model.reachable_worlds)


        # Print an attack statement
        if self.model.verbose:
            print("Player " + str(self.id) + " attacked with the " + str(card))


    def defend(self):
        '''
        Choose a card and defend with it.
        '''

        # Choose a card to defend against
        attacking_card = random.choice(self.defence_field.get_attacking_cards())

        # Choose a card to defend with
        if self.strategy == "random":
            defending_card = random.choice(self.hand.get_cards_in_hand())
        elif self.strategy == "normal":
            #--------- Depth 1 ----------#
            if self.knowledge_depth == 1:
                # Can you beat the attacking card?
                winning_card = self.hand.get_lowest_card_that_wins_defence(attacking_card) 
                if winning_card:
                    defending_card = winning_card # YES = Play lowest that beats that card
                else:
                    defending_card = self.hand.get_lowest_card() # NO = Play your lowest card


        # Play the card
        if defending_card in self.hand.get_cards_in_hand():
            self.defence_field.add_defence_card(attacking_card, defending_card)
            self.hand.remove_card(defending_card)

        # Print a defence statement
        if self.model.verbose:
            	print("Player " + str(self.id) + " defended with the " + str(defending_card))

    
    def take_cards_from_deck(self, model, num):
        """
        Take a given number of cards from the deck in the hand.
        """
        for i in range(num):
            if not model.deck.is_empty():
                self.hand.add_card(model.deck.deal())

    def get_cards_that_beat(self, card):
        """
        Returns a list with all cards in the player's hand that can beat the given card
        """

        