from mlsolver.kripke import World, KripkeStructure
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


# Quick demo of how the mlsolver library works.
def demo():
    worlds = [
        World('1', {'p': True, 'q': True}),
        World('2', {'p': True, 'q': False}),
        World('3', {'p': False, 'q': True})
    ]

    relations = {('1', '2'), ('2', '1'), ('1', '3'), ('3', '3')}
    print(type(relations))
    ks = KripkeStructure(worlds, relations)
    # print(ks.worlds)
    # print(ks.relations)
    print(ks)


full_numbers = ['2', '3', '4']
full_suits = ['S', 'C', 'H']
full_cards = ['2S', '2C', '2H', '3S', '3C', '3H', '4S', '4C', '4H']
full_players = ['B', 'M', 'L', 'Deck', 'Discard']
test_players = ['Hand', 'Deck', 'Discard']
hand_players = ['B', 'M', 'L']

gen_kripke(gen_worlds(full_cards, full_players), hand_players)
