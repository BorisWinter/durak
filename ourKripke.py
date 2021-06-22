from mlsolver.kripke import World, KripkeStructure
from mlsolver.model import add_symmetric_edges, add_reflexive_edges
from mlsolver.formula import *
import itertools


# Generates all possible worlds in the game for the given players and cards.
def gen_worlds(cards, players):
    l = list(itertools.combinations_with_replacement(players, len(cards)))
    worlds = []
    for i, state_set in enumerate(l):
        d = {place + cards[j]: True for j, place in enumerate(state_set)}
        w = World(str(i), d)
        # print(i, d)
        worlds.append(w)
    print("Generated", len(worlds), "worlds.")
    return worlds


# Given all worlds, generates a Kripke model.
# TODO used for development
def gen_kripke(worlds, players):
    full_edges = set((x, x + 1) for x in range(0, len(worlds)))  # one way
    full_edges.update({(0, len(worlds)), (len(worlds), 0)})  # last and first

    # Update with symmetric and reflexive edges. If needed, refer to
    # mlsolver.model for functions that do this for entire set of relations.
    full_edges.update(set((x, x - 1) for x in range(1, len(worlds) + 1)))  # symmetric
    full_edges.update(set((x, x) for x in range(0, len(worlds) + 1)))  # reflexive

    # full_edges = sorted(full_edges)
    relations = {p: full_edges for p in players}
    # print(relations)

    ks = KripkeStructure(worlds, relations)
    # print(ks.relations)
    return ks


# Given all worlds, generates a Kripke model.
# TODO if this version is used, the line "if str(w1) ... in to_remove" should be changed
def gen_str_kripke(worlds, players):
    full_edges = set((str(x), str(x + 1)) for x in range(0, len(worlds)))  # one way
    full_edges.update({('0', str(len(worlds))), (str(len(worlds)), '0')})  # last and first

    # Update with symmetric and reflexive edges. If needed, refer to
    # mlsolver.model for functions that do this for entire set of relations.
    full_edges.update(set((str(x), str(x - 1)) for x in range(1, len(worlds) + 1)))  # symmetric
    full_edges.update(set((str(x), str(x)) for x in range(0, len(worlds) + 1)))  # reflexive

    # full_edges = set(sorted(full_edges))
    relations = {p: full_edges for p in players}

    ks = KripkeStructure(worlds, relations)
    # print(ks.relations)
    return ks


# Quick demo of how the mlsolver library works, doubles as scratch code.
def demo():
    worlds = [
        World('1', {'p': True, 'q': True}),
        World('2', {'p': True, 'q': False}),
        World('3', {'p': False, 'q': True})
    ]
    relations = {'A': {('1', '2'), ('2', '1'), ('1', '3'), ('3', '1'), ('1', '1'), ('2', '2'), ('3', '3')},
                 'B': {('1', '3'), ('3', '1'), ('1', '1'), ('3', '3')}}
    ks = KripkeStructure(worlds, relations)
    print(ks)

    ## In this model, all worlds with "neg p" are removed,
    ## and so are all edges to and from those worlds.
    # print("---------------Box--------------")
    # print(ks.solve(Atom('p')))
    # print(ks.solve(Box_a('A', Atom('p'))))
    # print(ks.solve(Box_a('B', Atom('p'))))

    ## Some more tests
    # print("---------------Diamond--------------")
    # print(ks.solve(Diamond_a('A', Atom('p'))))
    # print(ks.solve(Diamond_a('B', Atom('p'))))

    ## A cleaner but slower way of writing these
    # formula = Diamond_a('2', Atom('p'))
    # new_ks = ks.solve(formula)
    # print(new_ks)

    # This only shows the list of worlds in which the
    # formula does not work, TODO might be useful.
    print(ks.nodes_not_follow_formula(Atom('p')))


# Remove all links for the given player to and/or from
# worlds in which the given statement is false.
def remove_link(ks, player, statement):
    to_remove = ks.nodes_not_follow_formula(Atom(statement))
    if len(to_remove) > 40:
        print("Number of worlds from/to which to remove relations:", len(to_remove))
    else:
        print("Worlds from/to which to remove relations:", to_remove)

    relations = ks.relations.get(player)  # Passed by ref, ie changes to 'relations' affect the model relations!
    print("Original number of worlds:", len(relations))
    links_to_remove = []
    for (w1, w2) in relations:
        if str(w1) in to_remove or str(w2) in to_remove:
            links_to_remove.append((w1, w2))  # Necessary because Python sets are annoying
    print("Number of relations to remove:", len(links_to_remove))
    relations -= set(links_to_remove)

    if len(relations) > 40:
        print("Updated number of relations:", len(relations))
    else:
        print("Updated relations: ", sorted(relations))  # This is a list, not a set! Used for development

    if relations != ks.relations.get(player):
        raise PassByRefError("Model is not updated properly")

    return ks


full_cards = ['2S', '2C', '2H', '3S', '3C', '3H', '4S', '4C', '4H']
full_players = ['B', 'M', 'L', 'Deck', 'Discard']
hand_players = ['B', 'M', 'L']


# Development sets
full_numbers = ['2', '3', '4']
full_suits = ['S', 'C', 'H']
test_cards = ['2S', '2C', '2H']
test_players = ['Hand', 'Deck', 'Discard']


k_m = gen_kripke(gen_worlds(full_cards, full_players), hand_players)
test_removed = remove_link(k_m, 'B', 'B2S')

# demo()
# k_m = gen_kripke(gen_worlds(test_cards, full_players), hand_players)
