from mlsolver.kripke import World, KripkeStructure
from mlsolver.model import add_symmetric_edges, add_reflexive_edges
from mlsolver.formula import *
import itertools


# Generates all possible worlds in the game for the given players and cards.
def gen_worlds(cards, players):
    l = list(itertools.combinations_with_replacement(players, 9))
    worlds = []
    for i, state_set in enumerate(l):
        d = {place + cards[j]: True for j, place in enumerate(state_set)}
        w = World(str(i), d)
        # print(i, d)
        worlds.append(w)
    # print(len(worlds))
    return worlds


# Given all worlds, generates a Kripke model.
# TODO alter to allow specification of relations?
def gen_kripke(worlds, players):
    full_edges = set((x, x + 1) for x in range(0, len(worlds)))  # one way
    full_edges.update({(0, len(worlds)), (len(worlds), 0)})  # last and first

    # Update with symmetric and reflexive edges. If needed, refer to
    # mlsolver.model for functions that do this for entire set of relations.
    full_edges.update(set((x, x - 1) for x in range(1, len(worlds) + 1)))  # symmetric
    full_edges.update(set((x, x) for x in range(0, len(worlds) + 1)))  # reflexive

    full_edges = sorted(full_edges)
    relations = {p: full_edges for p in players}
    # print(relations)

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


full_numbers = ['2', '3', '4']
full_suits = ['S', 'C', 'H']
full_cards = ['2S', '2C', '2H', '3S', '3C', '3H', '4S', '4C', '4H']
full_players = ['B', 'M', 'L', 'Deck', 'Discard']
test_players = ['Hand', 'Deck', 'Discard']
hand_players = ['B', 'M', 'L']

# gen_kripke(gen_worlds(full_cards, full_players), hand_players)
demo()