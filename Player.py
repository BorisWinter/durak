from AttackField import AttackField
from mesa import Agent
from Hand import Hand
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


    def __repr__(self):
        '''
        Returns the representation of the player.
        '''
        return "Player " + str(self.id) + ": " + str(self.hand)


    def step(self):
        '''
        '''
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        # print ("Hi, I am player " + str(self.unique_id) +".")
        self.attack()


    def receive_card(self, card):
        '''
        Adds the specified card to the hand of the player
        '''
        self.hand.add_card(card)

    
    def attack(self):
        '''
        Choose a card and attack with it.
        '''

        # Pick a card
        card = random.choice(self.hand.get_cards_in_hand())

        # Play the card
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