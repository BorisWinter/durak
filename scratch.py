import itertools





def calculate_possible_worlds(player0, player1, K_0, K_1):
    #cardList = ["2C", "2D", "3D", "3C", "4D", "4C"] # all possible cards
    cardList = ["2C", "2D", "3D", "3C"] # all possible cards

    # players have access to the hand size of other players
    hand_size_0 = len(player0)
    hand_size_1 = len(player1)

    # remove columns that are knowledge from the previous (and only previous) step
    #K_0 = ["2C0"]
    combination_cards_0 = cardList.copy()
    for card in K_0:
        combination_cards_0.remove(card[0:2])

    #K_1 = ["2D1"]
    combination_cards_1 = cardList.copy()
    for card in K_1:
        combination_cards_1.remove(card[0:2])

    # possible worlds for the known state
    # considered from player 0's perspective:
    print("player 0 considers that player 1 might have ...")
    x = itertools.combinations(combination_cards_0, hand_size_1)
    for p in x:
        print(p)

    # possible worlds for the known state
    # considered from player 1's perspective:
    print("player 1 considers that player 0 might have ...")

    x = itertools.combinations(combination_cards_1, hand_size_0)
    for p in x:
        print(p)

print("t =1")
calculate_possible_worlds(["2C"],["2D"], ["2C"], ["2D"])

print("t =2")

calculate_possible_worlds(["3C"],["2D","2C"], ["3C0"], ["2D1", "2C1"])

print("t =3")

calculate_possible_worlds(["3C"],["2D","2C"], ["3C0", "2D1"], ["2D1", "2C1"])

print("t =4")

calculate_possible_worlds([],["2D","2C"], [], ["2D1", "2C1"])
