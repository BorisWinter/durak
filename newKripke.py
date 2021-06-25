from mlsolver.kripke import World, KripkeStructure
from mlsolver.formula import Implies, Not, And, Or
from ourFormula import Atom
import itertools
from progress.bar import *


#class Kripke:

#    def __init__(self):
#        pass

def worlds_by_names_for_player(ks, player, reachable):
    worlds_to_check = []
    bar = Bar("Finding worlds", max=len(ks.worlds))
    for w in ks.worlds:
        if w.name in reachable[player]:
            worlds_to_check.append(w)
        bar.next()
    bar.finish()
    return worlds_to_check


def false_in_worlds(ks, formula, reachable, player, remove):
    """Returns a list with all worlds of Kripke structure, where formula
     is not satisfiable
    """
    nodes_not_follow_formula = []
    bar = Bar(f'Checking worlds for {formula} being FALSE', max=len(ks.worlds))
    for w in ks.worlds:
        if not formula.semantic(ks, w):
            # if not remove or (remove and w.name in reachable[player]):
            nodes_not_follow_formula.append(w)
    bar.finish()
    return nodes_not_follow_formula


# TODO can we think of any more restrictions?
def illegal_world(state_set, players, start_cards_per_player):
    # Just testing, with 4 cards or less
    if len(state_set) < 5:
        return False

    # Two cards go to the Discard pile at a time, so total count must be even
    if not state_set.count('Discard') % 2 == 0:
        return True

    if state_set.count('Deck') > (len(state_set) - len(players) - start_cards_per_player):
        # print(state_set.count('Deck'))
        return True
    for p in players:
        # one player has all the cards (TODO only removes three states)
        if state_set.count(p) == len(state_set):
            # print("Look,", p, "has all the cards!")
            return True
    return False


def gen_worlds(cards, players, hand_players):
    """
    Generates all possible worlds in the game for the given players and cards.
    """
    # TODO the first is correct, but generates SO MANY WORLDS
    locations = list(itertools.product(players, repeat=len(cards)))
    #locations = list(itertools.combinations_with_replacement(players, len(cards)))
    worlds = []
    bar = Bar('Generating worlds', max=len(locations)/2, suffix='%(percent)d%%')
    for i, state_set in enumerate(locations):
        if not illegal_world(state_set, hand_players, 2):
            # print(i)
            d = {place + cards[j]: True for j, place in enumerate(state_set)}
            w = World(str(i), d)
            # print(i, d)
            worlds.append(w)
            bar.next()
    bar.finish()
    print("Generated", len(worlds), "worlds.")
    return worlds


def gen_empty_kripke(worlds, players):
    relations = {p: set() for p in players}
    reachable = {p: [] for p in players}
    # print(relations)

    ks = KripkeStructure(worlds, relations)
    print("Generated empty model.")
    return ks, reachable


def bad_remove_links(ks, player, statement, reachable):
    """
    Remove all links for the given player to/from all REACHABLE
    worlds in which the given statement is TODO FALSE.
    """
    print("Removing links...")
    worlds_to_check = worlds_by_names_for_player(ks, player, reachable)
    test_model = KripkeStructure(worlds_to_check, ks.relations)
    # print([(w.name, w.assignment) for w in ks.worlds])

    # print(len(reachable[player]))
    worlds_to_remove = false_in_worlds(test_model, statement)
    # print(len(false_in_worlds(test_model, statement)))
    print("\t Number of worlds from/to which to remove relations:", len(worlds_to_remove))
    if len(worlds_to_remove) < 20:
        print("\t Worlds from/to which to remove relations:", worlds_to_remove)

    reachable[player] = [w for w in reachable[player] if w not in worlds_to_remove]
    print("\t Removed links")

    return ks, reachable


def remove_links(ks, player, statement, reachable):
    """
    Remove all links for the given player to/from ALL
    worlds in which the given statement is TODO FALSE.
    """
    #print("Removing links...")
    worlds_where_false = false_in_worlds(ks, statement, reachable, player, True)
    #print("\t Number of worlds from/to which to remove relations (incl. already unreachable):", len(worlds_where_false))
    #if len(worlds_where_false) < 20:
        #print("\t Worlds from/to which to remove relations:", [w.name for w in worlds_where_false])

    worlds_to_remove = []
    for w in worlds_where_false:
        if w in reachable[player]:
            reachable[player].remove(w)
    # reachable[player] = list(set(reachable[player]).difference(set(worlds_where_false)))


    return ks, reachable


def make_statement_cards(all_cards, true_cards, player_name):
    '''

    :param all_cards:
    :param true_cards:
    :param player_name:
    :return:
    '''
    statements = []
    for card in all_cards:
        if card not in true_cards:
            statements.append(Not(Atom(player_name + str(card))))
        else:
            statements.append(Atom(player_name + str(card)))
    big_conj = statements[0]
    for s in statements[1:]:
        big_conj = And(big_conj, s)
    return big_conj


def add_links(ks, player, statement, reachable):
    """
    Add all links for the given player to/from worlds
    in which the given statement is TODO TRUE.
    """
    #print("Adding links...")

    worlds_to_add = false_in_worlds(ks, Not(statement), reachable, player, False)
    #print("\t Number of worlds from/to which to add relations:", len(worlds_to_add))
    #if len(worlds_to_add) < 20:
        #print("\t Worlds from/to which to add relations:", [w.name for w in worlds_to_add])

    new_worlds = []
    for w in worlds_to_add:
        if w not in reachable[player]:
            new_worlds.append(w)
    reachable[player] += new_worlds
    # for w in new_worlds:
    #     reachable[player].append(w)


    # new_world_values = [list(w.assignment.keys()) for w in worlds_to_add]
    #
    # new_worlds = {w.name: w.assignment for w in worlds_to_add}
    # worlds_reachable = {w.name: w.assignment for w in reachable[player]}
    # new_worlds.update(worlds_reachable)
    #
    # print("Hello:", new_worlds)

    # reachable[player] = new_worlds

    return ks, reachable


def knowledge_base(player, reachable):
    print("PLAYER", player.get_id())
    print(player.hand)
    concetting = []
    my_list = []
    for item in player.hand.get_cards_in_hand():
        concetting.append(str(player.get_id())+str(item))

    playerKnowledge = set(concetting)
    number = len(playerKnowledge)
    for w in reachable[str(player.get_id())]:
        print(w)
        if playerKnowledge.issubset(set(list(w.assignment.keys()))) and sum(str(player.get_id()) in s for s in list(w.assignment.keys())) == number:

            my_list.append(set(list(w.assignment.keys())))
        #set(list(w.assignment.keys()))
    #my_list = [set(list(w.assignment.keys())) for w in reachable[str(player.get_id())]]
    for item in my_list:

        print(item)


    #print("worlds in possible words")
    #print(my_list)
    if len(my_list):
        my_set = my_list[0]
        for w in my_list[1:]:
            my_set = my_set.intersection(w)
            print(my_set)
        print("Player " + str(player.get_id()) + " knows:", my_set)

        return my_set
    else:
        return set()


def player_knows_cards_of_player(player, reachable, about_player):
    print("IN HERE")
    all_info = knowledge_base(player, reachable)
    known_cards = []
    for k in all_info:
        print(k)
        if k[0] == about_player:    # now breaks for pure kripke dev
            print(k[1:])
            print(type(k[1:]))
            known_cards.append(str(k[1:]))
    print(f"Player {player.get_id()} knows that player {about_player} has:", known_cards)

    return known_cards


def dev_test():
    # Development sets
    full_numbers = ['2', '3', '4']
    full_suits = ['S', 'C', 'H']
    test_cards = ['2S', '2C', '2H']
    test_players = ['B', 'Deck']
    test_hand_players = ['B']

    k_m, reachable_worlds = gen_empty_kripke(gen_worlds(test_cards, test_players, test_hand_players), test_hand_players)
    print("Reachable:", reachable_worlds)
    print("Full model:", k_m)

    statement = make_statement_cards(test_cards, ['2S', '2C'], 'B')
    print(statement)

    print(k_m.solve(statement))

    # print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    # test_added, reachable_worlds = add_links(k_m, 'B', Atom('B2S'), reachable_worlds)
    # print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    # print(reachable_worlds['B'])
    # test_removed, reachable_worlds = remove_links(k_m, 'B', Atom('Deck2C'), reachable_worlds)
    # print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    # print(reachable_worlds['B'])
    #
    # # knowledge_base('B', reachable_worlds)
    # player_knows_cards_of_player('B', reachable_worlds, 'Deck')

    # REMOVES all worlds in which formula is not True
    # print(test_added.solve(And(Atom('B2S'), Atom('B2C'))))

    # card_move(test_hand_players, 'B', 'B', '2S', k_m, reachable_worlds)


def demo_full():

    full_cards = ['2S', '2C', '2H', '3S', '3C', '3H', '4S', '4C', '4H']
    full_players = ['B', 'M', 'L', 'Deck', 'Discard']
    hand_players = ['B', 'M', 'L']

    all_worlds = gen_worlds(full_cards, full_players, hand_players)
    k_m, reachable_worlds = gen_empty_kripke(all_worlds, hand_players)

    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_added, reachable_worlds = add_links(k_m, 'B', Atom('B2S'), reachable_worlds)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_removed, reachable_worlds_now = remove_links(k_m, 'B', Atom('B2C'), reachable_worlds)
    print("Number of reachable worlds for B (now):", len(reachable_worlds_now['B']))
    #
    # test_again, reachable_worlds = bad_remove_links(k_m, 'B', And(Atom('B2S'), Atom('B3S')), reachable_worlds)
    # print("Number of reachable worlds for B (again):", len(reachable_worlds['B']))
    # knowledge_base('B', reachable_worlds_now)
    player_knows_cards_of_player('B', reachable_worlds_now, 'Deck')


# demo_full()
# dev_test()
#
#
# d_1 = {'1': {'ABC': True, 'ABD': True},
#        '2': {'ABC': True, 'ACD': True}}
# d_2 = {'1': {'ABC': True, 'ABD': True},
#        '3': {'XYZ': True}}
# d_1.update(d_2)
# print(d_1)
#





# print(list(itertools.product('ABCD', repeat=3)))
