[Overview](#overview) - 
[Installation](#installation) - 
[Game](#game) -
[Model](#model)

## Overview
Analyzing the Russian card game of Durak using epistemic logic. 

Practically, this main game consists of classes AttackField, Card, Deck, DiscardPile, Hand, and Player, and the main program ```durak.py```. The logical aspects of the game are represented in classes Inference and KnowledgeFact.

## Installation and run
To install all required packages, run:
```
pip install -r requirements.txt
```
To run the game:
```
python durak.py
```

## Model
To keep the complexity of the implementation as low as possible, the game was reduced to a very simple version with only 3 players (0,1,2), and 3 numbers (2,3,4) for 3 suits (diamonds, hearts, and clubs). Moreover, the non-attacking players can not present additional cards to an already defending player, and each attack is done with only one card, even if multiple cards are possible. 

To account for the steps taken as part of each attack, there is a special location for cards to be in, namely the "attack field", between each two players. In other words, when player A attacks B, the attacking cards go from A's hand to the attack field between A and B. 

### Knowledge and strategy
The knowledge in the game is represented as a list of statements, one for each agent and one for common knowledge. These lists are updated after each move. The knowledge that is gained in the game concerns the cards in the hands of the players, as well as the cards in the deck and the discard pile. Some of these cards are known for sure, while others are of the form "Player 1 knows that Player 2 has a subset of the following cards". 

Note that we plan on implementing the rule that it is common knowledge how many cards each player has, how many are in the deck, and how many in the discard pile. In real life, the game goes too fast to keep track of this implicitly; an interesting experiment might be to "toggle" this knowledge on or off.

Another function we are still working on implementing is the inference of knowledge, which is an important step in implementing actual strategies. So far, the players do not have strategies; the card used to attack is chosen at random, and a defending card is chosen from the viable options if there are any. Real-life strategy in Durak is based both on choosing such cards based on the progression of the game (i.e. the size of the deck; a high card should not be used to attack in an early round), and on choosing such cards based on what the player knows about the cards of the defender. 

Lastly, another aspect that we aim to experiment with is that where one player has higher-order knowledge, i.e. that at the beginning of the game, one player knows what some other player's knowledge is. 
