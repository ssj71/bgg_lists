#!/usr/bin/env python3
#spencer jackson

#look at the top games and compare the rating std deviation

import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
from datetime import date
import csv
import pandas as pd
import bgg_get_historicals as bgg_historicals

top = bgg_historicals.get_date(2022,2,10)[:100,bgg_historicals.gameid_col]
stats = bggstats.getStatsSlowly(top)

matplot.scatter(stats[:,bggstats.voters_col].astype(np.int),stats[:,bggstats.stddev_col].astype(np.float))
matplot.gca().set_xscale("log")
matplot.show()

exit()

first = True
topN = np.empty([ntop,2], dtype=bggstats.getGameStatsRowType())
for game in stats:
    rank = float(game[bggstats.weight_col])
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
