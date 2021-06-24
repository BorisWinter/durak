from mlsolver.kripke import World, KripkeStructure
from mlsolver.formula import Implies, Not, And, Or
from ourFormula import Atom
import itertools
from progress.bar import *


def false_in_worlds(worlds, formula, reachable, player, remove):
    """Returns a list with all worlds of Kripke structure, where formula
     is not satisfiable
    """
    nodes_not_follow_formula = set()
    bar = Bar(f'Checking worlds for {formula} being FALSE', max=len(worlds))
    for w in worlds:
        if not formula.semantic(worlds, w):
            print("Here:", w)
            # if not remove or (remove and w.name in reachable[player]):
            nodes_not_follow_formula |= w
    bar.finish()
    print(type(nodes_not_follow_formula))
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
    # locations = list(itertools.combinations_with_replacement(players, len(cards)))
    worlds = set()
    bar = Bar('Generating worlds', max=len(locations)/2, suffix='%(percent)d%%')
    for i, state_set in enumerate(locations):
        if not illegal_world(state_set, hand_players, 2):
            # print(i)
            w = {place + cards[j] for j, place in enumerate(state_set)}
            worlds.add(w)
            bar.next()
    bar.finish()
    print("Generated", len(worlds), "worlds.")
    print(worlds)
    return worlds


def gen_empty_kripke(players):
    reachable = {p: set() for p in players}
    print("Generated empty model.")
    return reachable


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
    print("Removing links...")
    worlds_to_remove = false_in_worlds(ks, statement, reachable, player, True)
    print("\t Number of worlds from/to which to remove relations (incl. already unreachable):", len(worlds_to_remove))
    if len(worlds_to_remove) < 20:
        print("\t Worlds from/to which to remove relations:", [w.name for w in worlds_to_remove])
    reachable[player] = list(set(reachable[player]).difference(set(worlds_to_remove)))

    return ks, reachable


def add_links(all_worlds, player, statement, reachable):
    """
    Add all links for the given player to/from worlds
    in which the given statement is TODO TRUE.
    """
    print("Adding links...")

    # worlds_to_add = {w for w in all_worlds if statement not in w}
    # print(worlds_to_add)

    worlds_to_add = false_in_worlds(all_worlds, Not(statement), reachable, player, False)
    print("\t Number of worlds from/to which to add relations:", len(worlds_to_add))
    if len(worlds_to_add) < 20:
        print("\t Worlds from/to which to add relations:", worlds_to_add)

    # new_world_values = [list(w.assignment.keys()) for w in worlds_to_add]

    # new_worlds = {w.name: w.assignment for w in worlds_to_add}
    # worlds_reachable = {w.name: w.assignment for w in reachable[player]}
    # new_worlds.update(worlds_reachable)
    # print(reachable[player])

    # print("Hello:", new_worlds)
    print(type(reachable[player]))
    print(reachable[player])
    print(worlds_to_add)

    reachable[player] = reachable[player].update(worlds_to_add)

    return reachable


def dev_test():
    # Development sets
    full_numbers = ['2', '3', '4']
    full_suits = ['S', 'C', 'H']
    test_cards = ['2S', '2C']
    test_players = ['B', 'Deck']
    test_hand_players = ['B']

    all_worlds = gen_worlds(test_cards, test_players, test_hand_players)
    reachable_worlds = gen_empty_kripke(test_hand_players)
    print("Reachable:", reachable_worlds)
    print("All worlds:", all_worlds)

    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_added, reachable_worlds = add_links(all_worlds, 'B', Atom('B2S'), reachable_worlds)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    print(reachable_worlds['B'])
    test_removed, reachable_worlds = remove_links(k_m, 'B', Atom('Deck2C'), reachable_worlds)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    print(reachable_worlds['B'])

    # REMOVES all worlds in which formula is not True
    # print(test_added.solve(And(Atom('B2S'), Atom('B2C'))))

    # card_move(test_hand_players, 'B', 'B', '2S', k_m, reachable_worlds)


def demo_full():

    full_cards = ['2S', '2C', '2H', '3S', '3C', '3H', '4S', '4C', '4H']
    full_players = ['B', 'M', 'L', 'Deck', 'Discard']
    hand_players = ['B', 'M', 'L']

    all_worlds = gen_worlds(full_cards, full_players, hand_players)
    k_m, reachable_worlds = gen_empty_kripke(hand_players)

    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_added, reachable_worlds = add_links(k_m, 'B', Atom('B2S'), reachable_worlds)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_removed, reachable_worlds_now = remove_links(k_m, 'B', Atom('B2C'), reachable_worlds)
    print("Number of reachable worlds for B (now):", len(reachable_worlds_now['B']))
    #
    # test_again, reachable_worlds = bad_remove_links(k_m, 'B', And(Atom('B2S'), Atom('B3S')), reachable_worlds)
    # print("Number of reachable worlds for B (again):", len(reachable_worlds['B']))



# demo_full()
dev_test()


d_1 = {'1': {'ABC': True, 'ABD': True},
       '2': {'ABC': True, 'ACD': True}}
d_2 = {'1': {'ABC': True, 'ABD': True},
       '3': {'XYZ': True}}
d_1.update(d_2)
print(d_1)




# print(list(itertools.product('ABCD', repeat=3)))
