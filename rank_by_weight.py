#!/usr/bin/env python3
#spencer jackson

#look at how the top played games is correlated (or not) with the top ranked games

import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot

ntop = 10

top = bggtr.getTopRankedGames(20)
print(len(top))
stats = bggstats.getStatsSlowly(top)
categories = ( 
    "Flyweight [1.0-1.5)",
    "Featherweight [1.5-2.0)",
    "Welterweight [2.0-2.5)",
    "Middleweight [2.5-3.0)",
    "Light-Heavyweight [3.0-3.5)",
    "Cruiserweight [3.5-4.0)",
    "Heavyweight [4.0-4.5)",
    "Super-Heavyweight [4.5-5.0]",
    )

def weight2categoryindex(weight):
    return int(2*(weight-1))

first = True
topN = np.empty([len(categories),ntop], dtype=bggstats.getGameStatsRowType())
for game in stats:
    weight = float(game[bggstats.weight_col])
    rating = float(game[bggstats.rating_col])
    category = weight2categoryindex(weight)
    if topN[category,0][2] != 0:
        #already found 10 in the category
        continue
    for i in range(ntop-1,-1,-1):
        if topN[category,i][2] == 0:
            for j in range(len(game)):
                topN[category,i][j] = game[j]
            break

cat = 0
for mat in topN:
    i = ntop
    print(categories[cat],"\n") 
    for game in mat:
        print(game[bggstats.gameid_col], game[bggstats.name_col], "\n")
        print("#", i, " in ", categories[cat], sep="")
        print("weight:", game[bggstats.weight_col])
        print("\n")
        i -= 1
    cat += 1



    

#matplot.scatter(results[:,0],results[:,1])
#matplot.show()
