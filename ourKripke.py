from mlsolver.kripke import World, KripkeStructure
import itertools


# Generates initial Kripke structure in the game.
def gen_worlds(cards, players):
    l = list(itertools.combinations_with_replacement(players, 9))
    worlds = []
    for i, state_set in enumerate(l):
        d = {place+cards[j]: True for j, place in enumerate(state_set)}
        w = World(str(i), d)
        # print(i, d)
        worlds.append(w)

    # Add all reflexive edges
    relations = set((x, x+1) for x in range(0, len(worlds)))
    relations.update(set((x, x-1) for x in range(1, len(worlds)+1)))
    relations.update()
    relations.update({(0, len(worlds)), (len(worlds), 0)})
    # print(sorted(relations))
    ks = KripkeStructure(worlds, relations)
    # print(ks)

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

gen_worlds(full_cards, test_players)
# demo()