[Overview](#overview) - 
[Game](#game) -
[Installation](#installation) - 
[Model](#model) - 

## Overview
Analyzing the Russian card game of Durak using epistemic logic. 

## Game
The gameplay consists of player A attacking their neighbour B with some cards of the same number (for example, 5 of spades and/or 6 of hearts). Player B must defend these by covering each presented card with a card which ``trumps'' that card. 

There is also a so-called trump suit, which trumps other suits. In our example, consider the trump suit to be spades. Then the 5 of hearts could be defended by any card of hearts higher than 5, or any card of spades on hand. However, the 5 of spades can only be defended by a card of spades higher than 5. 

For each presented or covering number, the other players of the game can present more cards of the same number for B to defend. B can defend a maximum of 6 cards in a turn.

If player B manages to defend all presented cards, these and the covering cards are discarded from the game and B can attack its neighbour, C. If player B cannot defend all cards, they have to pick them all up. After each turn, all players with fewer than six cards draw until they have six.

## Installation
To install all required packages (so far only mesa), run:
```
pip3 install -r requirements.txt
```

## Model
To keep the complexity of the implementation as low as possible, the game was reduced to a very simple version with only 3 players (0,1,2), and 3 numbers (2,3,4) for 3 suits (diamonds, hearts, and clubs).

To account for the steps taken as part of each attack, there is a fourth "player", namely the "attack field", between each two players. In other words, when player A attacks B, the attacking card(s) go(es) from A's hand to the attack field between A and B. 

Consists of classes AttackField, Card, Deck, Hand, and Player, and main program ```durak.py```. 