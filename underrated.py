#!/usr/bin/env python3
#spencer jackson

#look at the top 10 ranked games in different weight "classes"

import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
import regression as reg

top = bggtr.getTopRankedGames(100)
stats = bggstats.getStatsSlowly(top)

#TODO: this method highlights low avg rating games, need to factor in actual rating, not just difference
disparity = stats[:,bggstats.rating_col].astype(np.float)-stats[:,bggstats.geekrating_col].astype(np.float)
nvotes = stats[:,bggstats.voters_col].astype(np.int)
l = stats.shape[0]

#make a linear regression of the disparity per rank
x = 1+np.r_[:l] #x is the ranks
coeff = reg.reg(x,disparity,1)
y = reg.applyPoly(x,coeff)

#tot = np.hstack((stats, np.array([disparity]).T-y))
tot = np.hstack(( np.array([x]]).T, np.array([disparity]).T-y))
slist = np.sort(tot.view('f8,f8'), order=['f1'], axis=0)[::-1]

for i in slist[:25,0]:
    print(stats[i, bggstats.gameid_col], stats[i, bggstats.name_col])
    print("avg rating:", stats[i, bggstats.rating_col], "\ngeek rating:", stats[i, bggstats.geekrating_col])
    print(stats[i, bggstats.voters_col],"\n" stats[i, bggstats.year_col])

matplot.scatter(x, disparity)
matplot.plot(x, y, 'k')

matplot.show()
