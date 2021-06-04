from AttackField import AttackField
from mesa import Agent
from Hand import Hand
from KnowledgeFact import KnowledgeFact
import random

class Player(Agent):
    """
    Models a player in the game of Durak
    """

    def __init__(self, unique_id, model, attack_fields, num_players):
        super().__init__(unique_id, model)
        self.id = unique_id
        self.hand = Hand(self.id)
        self.attack_field = attack_fields[self.id]
        self.defence_field = attack_fields[(self.id - 1) % num_players]
        self.private_knowledge = self.initial_knowledge()
        self.common_knowledge = []



    def __repr__(self):
        '''
        Returns the representation of the player.
        '''
        return "\n Player " + str(self.id) + "\n\t Hand : " + str(self.hand) + "\n\t Knowledge : " +\
               str(self.private_knowledge)

    def initial_knowledge(self):
        return []

    def update_knowledge_own_hand(self):
        # step 1: the agent KNOWS its own hand
        self.private_knowledge = [] # knowledge about the current state of hand only
        for card in self.hand.get_cards_in_hand():
            knowledge = KnowledgeFact("K", self.id, card, self.id)
            if knowledge not in self.private_knowledge:
                self.private_knowledge.append(knowledge)



    def get_number_of_cards_in_hand(self):
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

        # Pick one ore more cards TODO: Make it so that multiple cards can be played
        card = random.choice(self.hand.get_cards_in_hand())

        # Play the card(s)
        if card in self.hand.get_cards_in_hand():
            self.attack_field.add_attack_card(card)
            self.hand.remove_card(card)

        # Print an attack statement
        print("Player " + str(self.id) + " attacked with the " + str(card))


    def defend(self):
        '''
        Choose a card and defend with it.
        '''

        # Choose a card to defend against
        attacking_card = random.choice(self.defence_field.get_attacking_cards())

        # Pick a card from your hand to defend with
        defending_card = random.choice(self.hand.get_cards_in_hand())

        # Play the card
        if defending_card in self.hand.get_cards_in_hand():
            self.defence_field.add_defence_card(attacking_card, defending_card)
            self.hand.remove_card(defending_card)

        # Print a defence statement
        print("Player " + str(self.id) + " defended with the " + str(defending_card))

    
    def take_cards_from_deck(self, model, num):
        """
        Take a given number of cards from the deck in the hand.
        """
        for i in range(num):
            if not model.deck.is_empty():
                self.hand.add_card(model.deck.deal())