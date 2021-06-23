import itertools
from collections import *



def calculate_possible_worlds_for_player(player_id, player_cards, other_player_id, handsize_other, player_knowledge):
    cardList = ["2C", "2D", "3D", "3C"]  # all possible cards
    world_list = []
    relations = []
    cardDict = {}

    for card in cardList:
        cardDict[card] = "D" # default card is in deck

    # players have access to the hand size of other players
    hand_size_0 = len(player_cards)
    hand_size_1 = handsize_other

    combination_cards = cardList.copy()


    for card in player_knowledge:
        cardDict[card[0:2]] = card[-1]
        combination_cards.remove(card[0:2])

        # possible worlds for the known state
        # considered from player 0's perspective:
        #print("player" + player_id + " considers that player 1 might have ...")
        x = itertools.combinations(combination_cards, hand_size_1)
        wl_0 = []
        for p in x:
            # print(p)
            new_world = cardDict.copy()
            q = list(p)
            for w in q:
                new_world[w] = other_player_id
            #print(new_world)
            wl_0.append(str(new_world))
            world_list.append(str(new_world))

        relations = list(itertools.product(wl_0, repeat=2))

    return world_list, relations



'''  

def calculate_possible_worlds(player0, player1, K_0, K_1):
    #cardList = ["2C", "2D", "3D", "3C", "4D", "4C"] # all possible cards
    cardList = ["2C", "2D", "3D", "3C"] # all possible cards
    world_list = []
    cardDict0 = {}
    cardDict1 = {}

    for card in cardList:
        cardDict0[card] = "D" # default card is in deck
        cardDict1[card] = "D" # default card is in deck


    # players have access to the hand size of other players
    hand_size_0 = len(player0)
    hand_size_1 = len(player1)

    # remove columns that are knowledge from the previous (and only previous) step
    #K_0 = ["2C0"]

    combination_cards_0 = cardList.copy()
    for card in K_0:
        if card[-1] == "0":
            cardDict0[card[0:2]] = "0"
        else:
            cardDict0[card[0:2]] = "1"

        combination_cards_0.remove(card[0:2])


    #K_1 = ["2D1"]
    combination_cards_1 = cardList.copy()
    for card in K_1:
        if card[-1] == "1":
            cardDict1[card[0:2]] = "1"
        else:
            cardDict1[card[0:2]] = "0"
        combination_cards_1.remove(card[0:2])

    # possible worlds for the known state
    # considered from player 0's perspective:
    print("player 0 considers that player 1 might have ...")
    x = itertools.combinations(combination_cards_0, hand_size_1)
    wl_0 = []
    for p in x:
        #print(p)
        new_world = cardDict0.copy()
        q = list(p)
        for w in q:
            new_world[w] = "1"
        print(new_world)
        wl_0.append(new_world.items())
        world_list.append(new_world.items())

    relations_0 = itertools.product(wl_0, repeat=2)



    # possible worlds for the known state
    # considered from player 1's perspective:
    print("player 1 considers that player 0 might have ...")

    x = itertools.combinations(combination_cards_1, hand_size_0)
    wl_1 = []
    for p in x:
        #print(p)
        #print(list(p))
        q = list(p)
        new_world = cardDict1.copy()
        for w in q:
            new_world[w] = "0"
        print(new_world)
        wl_1.append(new_world.items())
        world_list.append(new_world.items())

    relations_1 = itertools.product(wl_1, repeat=2)

    for relation in relations_0:
        print("RELATION", relation)

    return world_list
'''

print("t =1")
# player 0 has 2C,
# player 1 has 2D,
# no attacks yet, so no-one knows anything
# the rest of the cards are in the deck.


worlds0, relations0 = calculate_possible_worlds_for_player("0", ["2C"], "1", 1,["2C0"])
worlds1, relations1 = calculate_possible_worlds_for_player("1", ["2D"], "0", 1,["2D1"])

print("worlds considered possible by player 0: ")
for world in worlds0:
    print("\t" +world)

print("relations on those worlds ")
for rel in relations0:
    print(rel)

print("worlds considered possible by player 1: ")
for world in worlds1:
    print("\t" + world)

print("relations on those worlds ")
for rel in relations1:
    print(rel)





'''
wl = calculate_possible_worlds(["2C"],["2D"], ["2C0"], ["2D1"])
print(wl)
print("t =2")

calculate_possible_worlds(["3C"],["2D","2C"], ["3C0"], ["2D1", "2C1"])

print("t =3")

calculate_possible_worlds(["3C"],["2D","2C"], ["3C0", "2D1"], ["2D1", "2C1"])

print("t =4")

calculate_possible_worlds([],["2D","2C"], [], ["2D1", "2C1"])




print("t =1")
wl = calculate_possible_worlds(["2C"],["2D"], ["2C0"], ["2D1"])
print(wl)
print("t =2")

calculate_possible_worlds(["3C"],["2D","2C"], ["3C0"], ["2D1", "2C1"])

print("t =3")

calculate_possible_worlds(["3C"],["2D","2C"], ["3C0", "2D1"], ["2D1", "2C1"])

print("t =4")

calculate_possible_worlds([],["2D","2C"], [], ["2D1", "2C1"])
'''