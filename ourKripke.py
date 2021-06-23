from mlsolver.kripke import World, KripkeStructure
from mlsolver.formula import *
import itertools
from progress.bar import *


# TODO can we think of any more restrictions?
def illegal_world(state_set, players, start_cards_per_player):
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
    # TODO the first is correct, but generates SO MANY WORLDS that everything crashes when trying to add full relations.
    # locations = list(itertools.product(players, repeat=len(cards)))
    locations = list(itertools.combinations_with_replacement(players, len(cards)))
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


# Given all worlds, generates a fully connected Kripke model.
def gen_kripke(worlds, players):
    # print("Generating relations, itertools takes a while")  # TODO explore generating dynamically, i.e. from 0 up
    w = list(itertools.product(worlds, repeat=2))
    print("Number of relations:", len(w))
    full_edges = set()
    bar = Bar('Adding relations', max=len(w), suffix='%(percent)d%%')
    for (w1, w2) in w:
        full_edges.update({(w1.name, w2.name)})
        bar.next()
    bar.finish()
    relations = {p: full_edges for p in players}
    reachable = {p: [world.name for world in worlds] for p in players}
    # print(relations)

    ks = KripkeStructure(worlds, relations)
    print("Generated model. ")
    # print(ks.relations)
    return ks, reachable


# Remove all links for the given player to and/or from
# worlds in which the given statement is false.
def remove_links(ks, player, statement, reachable):
    print("Removing links...")
    worlds_to_remove = ks.nodes_not_follow_formula(statement)
    print("\t Number of worlds from/to which to remove relations:", len(worlds_to_remove))
    if len(worlds_to_remove) < 20:
        print("\t Worlds from/to which to remove relations:", worlds_to_remove)

    relations = ks.relations[player]  # Passed by ref, ie changes to 'relations' affect the model relations!
    print("\t Original number of relations:", len(relations))
    links_to_remove = []
    for (w1, w2) in relations:
        if w1 in worlds_to_remove or w2 in worlds_to_remove:
            links_to_remove.append((w1, w2))  # Necessary because Python sets are annoying
    print("\t Number of relations to remove:", len(links_to_remove))
    relations -= set(links_to_remove)

    print("\t Updated number of relations:", len(relations))
    if len(relations) < 50:
        print("\t Updated relations as sorted list: ", sorted(relations))  # Used for development

    reachable[player] = [w for w in reachable[player] if w not in worlds_to_remove]

    return ks, reachable


# Add all links for the given player to and/or from
# worlds in which the given statement is true.
# TODO only add when not already in there
def add_links(ks, player, statement, reachable):
    print("Adding links...")

    worlds_to_add = ks.nodes_not_follow_formula(statement)
    print("\t Number of worlds from/to which to add relations:", len(worlds_to_add))
    if len(worlds_to_add) < 20:
        print("\t Worlds from/to which to add relations:", worlds_to_add)

    other_worlds = reachable[player]
    if len(other_worlds) < 50:
        print("\t Other worlds", other_worlds)

    new_reachable = list(set(other_worlds+worlds_to_add))
    links_to_add = list(itertools.product(new_reachable, repeat=2))
    # Above also includes reflexivity in other_worlds, but that is solved by using sets

    print("\t Number of relations to add (incl. already there):", len(links_to_add))
    if len(links_to_add) < 20:
        print("\t Relations to add (incl. already there):", links_to_add)
    ks.relations[player].update(set(links_to_add))
    relations = ks.relations[player]

    print("\t Updated number of relations:", len(relations))
    if len(relations) < 50:
        print("\t Updated relations as sorted list: ", sorted(relations))  # Used for development

    reachable[player] = list(set(reachable[player]+worlds_to_add))

    return ks, reachable


def card_move(all_players, from_player, to_player, card, ks, reachable):
    for p in all_players:
        fuller_model, reachable = add_links(ks, p, Atom(to_player + card), reachable)
        final_model, reachable = remove_links(fuller_model, p, Atom(from_player + card), reachable)


def dev_test():
    # Development sets
    full_numbers = ['2', '3', '4']
    full_suits = ['S', 'C', 'H']
    test_cards = ['2S', '2C']
    test_players = ['B', 'Deck']
    test_hand_players = ['B']

    k_m, reachable_worlds = gen_kripke(gen_worlds(test_cards, test_players, test_hand_players), test_hand_players)
    print("Reachable:", reachable_worlds)
    print("Full model:", k_m)
    test_removed, reachable_worlds = remove_links(k_m, 'B', And(Not(Atom('B2C')), Atom('B2S')), reachable_worlds)
    test_added, reachable_worlds = add_links(test_removed, 'B', And(Not(Atom('B2C')), Atom('B2S')), reachable_worlds)

    # card_move(test_hand_players, 'B', 'B', '2S', k_m, reachable_worlds)


def demo_full():
    full_cards = ['2S', '2C', '2H', '3S', '3C', '3H', '4S', '4C', '4H']
    full_players = ['B', 'M', 'L', 'Deck', 'Discard']
    hand_players = ['B', 'M', 'L']

    all_worlds = gen_worlds(full_cards, full_players, hand_players)
    k_m, reachable_worlds = gen_kripke(all_worlds, hand_players)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_removed, reachable_worlds = remove_links(k_m, 'B', Atom('B2S'), reachable_worlds)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))
    test_added, reachable_worlds = add_links(test_removed, 'B', Atom('B2S'), reachable_worlds)
    print("Number of reachable worlds for B:", len(reachable_worlds['B']))


demo_full()
# dev_test()

# print(list(itertools.product('ABCD', repeat=3)))
