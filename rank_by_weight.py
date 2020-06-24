#!/usr/bin/env python3
#spencer jackson

#look at the top 10 ranked games in different weight "classes"

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
    if first:
        results = np.array([[weight,rating]])
        first = False
    else:
        results = np.vstack((results, np.array([weight,rating])))
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
        print(game[bggstats.gameid_col], game[bggstats.name_col])
        print("#", i, " in ", categories[cat], sep="")
        print("weight:", game[bggstats.weight_col])
        print("\n")
        i -= 1
    cat += 1

print("\nSummary:")
#this summary is harder to read than the ranks
#cat = 0
#for mat in topN:
#    print( categories[cat], "Ratings: ", mat[0][bggstats.rating_col], "-", mat[ntop-1][bggstats.rating_col])
#    cat += 1
#print("")
cat = 0
for mat in topN:
    print( categories[cat].ljust(30,'.'), "Ranks: ", mat[ntop-1][bggstats.rank_col], "-", mat[0][bggstats.rank_col], sep="")
    cat += 1
print("\n")


matplot.scatter(results[:,0],results[:,1])
matplot.show()
