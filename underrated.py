#!/usr/bin/env python3
#spencer jackson

#find games that could be higher ranked if they just got more ratings

import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
import regression as reg

top = bggtr.getTopRankedGames(100)
stats = bggstats.getStatsSlowly(top)
filterwidth = 46
smoothwidth = 5 #keep this odd

nvotes = stats[:,bggstats.voters_col].astype(np.int)
l = stats.shape[0]

#this could maybe be done with broadcasting but I'd have to look it up
medvotes = np.r_[:l-filterwidth]
for i in range(l-filterwidth):
    medvotes[i] = np.median(nvotes[i:i+filterwidth])

size = l-filterwidth - smoothwidth +1
smoothvotes = np.r_[:size]
#another pass to smooth it further
for i in range(size):
    smoothvotes[i] = np.mean(medvotes[i:i+smoothwidth])


irange = (np.r_[:size]+(filterwidth+smoothwidth-1)/2).astype(int)
medratio = smoothvotes/nvotes[irange]

tot  = np.array([ irange, medratio]).T
slist = tot[tot[:,1].argsort()[::-1]]

for inx,medr in slist[:50,:]:
    i = int(inx) #rank
    print(stats[i, bggstats.gameid_col], stats[i, bggstats.name_col])
    print("rank:",i+1)
    print("avg rating:", stats[i, bggstats.rating_col], "\ngeek rating:", stats[i, bggstats.geekrating_col])
    print("voters:", stats[i, bggstats.voters_col])
    print("%% of median: %.4f%% " % (100.0/medr))
    print("year published:", stats[i, bggstats.year_col], "\n")

matplot.scatter( np.r_[:l], nvotes)
matplot.plot( np.r_[:l-filterwidth]+filterwidth/2, medvotes)
matplot.plot( irange, smoothvotes)
matplot.ylabel('voters')
matplot.xlabel('rank')
matplot.title("Voters per Rank")
matplot.show()
