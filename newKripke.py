from mlsolver.kripke import World, KripkeStructure
from mlsolver.formula import Implies, Not, And, Or
from ourFormula import Atom
import itertools
from progress.bar import *


#class Kripke:

#    def __init__(self):
#        pass

def false_in_worlds(model, formula):
    """Returns a list with all worlds of Kripke structure, where formula
     is not satisfiable
    """
    nodes_not_follow_formula = []
    bar = Bar('Checking worlds', max=len(model.worlds), suffix='%(percent)d%%')
    for w in model.worlds:
        if not formula.semantic(model, w):
            nodes_not_follow_formula.append(w.name)
        bar.next()
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


# Generates all possible worlds in the game for the given players and cards.
def gen_worlds(cards, players, hand_players):
    # TODO the first is correct, but generates SO MANY WORLDS
    locations = list(itertools.product(players, repeat=len(cards)))
    # locations = list(itertools.combinations_with_replacement(players, len(cards)))
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


# Remove all links for the given player to and/or from
# worlds in which the given statement is false.
def remove_links(ks, player, statement, reachable):
    print("Removing links...")
    worlds_to_remove = false_in_worlds(Not(statement))
    print("\t Number of worlds from/to which to remove relations:", len(worlds_to_remove))
    if len(worlds_to_remove) < 20:
        print("\t Worlds from/to which to remove relations:", worlds_to_remove)

    reachable[player] = [w for w in reachable[player] if w not in worlds_to_remove]

    return ks, reachable


# Add all links for the given player to and/or from
# worlds in which the given statement is true.
def add_links(ks, player, statement, reachable):
    print("Adding links...")

    worlds_to_add = false_in_worlds(Not(statement))
    print("\t Number of worlds from/to which to add relations:", len(worlds_to_add))
    if len(worlds_to_add) < 20:
        print("\t Worlds from/to which to add relations:", worlds_to_add)

    reachable[player] = list(set(reachable[player]+worlds_to_add))

    return ks, reachable


def dev_test():
    # Development sets
    full_numbers = ['2', '3', '4']
    full_suits = ['S', 'C', 'H']
    test_cards = ['2S', '2C']
    test_players = ['B', 'Deck']
    test_hand_players = ['B']

    k_m, reachable_worlds = gen_empty_kripke(gen_worlds(test_cards, test_players, test_hand_players), test_hand_players)
    print("Reachable:", reachable_worlds)
    print("Full model:", k_m)

    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_added, reachable_worlds = add_links(k_m, 'B', Atom('B2S'), reachable_worlds)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_removed, reachable_worlds = remove_links(k_m, 'B', Atom('B2S'), reachable_worlds)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))

    # REMOVES all worlds in which formula is not True
    # print(test_added.solve(And(Atom('B2S'), Atom('B2C'))))

    # card_move(test_hand_players, 'B', 'B', '2S', k_m, reachable_worlds)


def demo_full():
    full_cards = ['2S', '2C', '2H', '3S', '3C', '3H', '4S', '4C', '4H']
    full_players = ['B', 'M', 'L', 'Deck', 'Discard']
    hand_players = ['B', 'M', 'L']

    all_worlds = gen_worlds(full_cards, full_players, hand_players)
    k_m, reachable_worlds = gen_empty_kripke(all_worlds, hand_players)

    print(len(false_in_worlds(k_m, Not(And(Atom('B2S'), Atom('B2C'))))))

    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    # test_added, reachable_worlds = add_links(k_m, 'B', Atom('B2S'), reachable_worlds)
    # print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    # test_removed, reachable_worlds = remove_links(k_m, 'B', Atom('B2S'), reachable_worlds)
    # print("Number of reachable worlds for B:", len(reachable_worlds['B']))


demo_full()
# dev_test()

# print(list(itertools.product('ABCD', repeat=3)))
