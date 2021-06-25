# Imports
import pandas as pd
import durak
from AttackField import AttackField
from mesa import Model
from CustomStagedActivation import CustomStagedActivation
from Player import Player
from Deck import Deck
from DiscardPile import DiscardPile
import random
from newKripke import *
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import copy

"""
Percentage of losses per player
"""

num_runs = 20
data = {}

for game_index in range(num_runs):
    print("=================== GAME " + str(game_index) + " STARTED ===================")
    model = durak.DurakModel(
            verbose = False, 
            num_suits = 2, 
            num_cards_per_suit = 3,
            num_starting_cards = 1,
            num_players = 2,
            player_strategies = ["normal", "random", "random"],
            player_depths = [1,1,1],
            multiple_runs = True
            )
    data["game" + str(game_index)] = durak.play(model)
    #  = model.play(num_runs, verbose= False, player_strategies=player_strategies, player_depths=player_depths)


df = pd.DataFrame.from_dict(data, orient="index")
df.to_csv("d1_normal-d1_random.csv")

# df = pd.read_csv("d1_normal-d1_random-d1_random.csv")
# df.head()

fig, ax = plt.subplots()
durak_percentages = [x/len(df)*100 for x in list(Counter(df["durak"]).values())]
players = sorted(list(df.durak.unique()))

g = sns.barplot(x=players, y=durak_percentages, dodge=False)
g.set_xlabel("Player", fontsize=18)
g.set_xticklabels(["Player " + str(x) for x in players])

g.set_ylabel("Percentage of losses", fontsize=18)

ax=g
#annotate axis = seaborn axis
for p in ax.patches:
    ax.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=14, color='black', xytext=(0, 20),
                textcoords='offset points')
_ = g.set_ylim(0, 100) #To make space for the annotations

plt.savefig('test.png')