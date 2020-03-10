#!/usr/bin/env python3

import bgg_get_game_stats as bggstats
import bgg_most_played as bggmp
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot

month = 12 #month (1-12) to consider
monthwindow = 6 #window size in months

t6m = bggmp.loadyear(19,monthwindow) #top played
top = bggtr.getTopRankedGames(1)
mostplayed = t6m[month-1,:,:]


first = True
for rank,gameid in enumerate(top):
    i = np.where( mostplayed[:,bggmp.gameid_col] == gameid )[0]
    if i.size:
        #it was found
        uniqueplays = mostplayed[i,bggmp.uniqueplays_col]
        stats = bggstats.getGameStats(bggstats.getGameXML2((gameid,)))[0]
        owned = int(stats[bggstats.owned_col])
        print(rank, stats[bggstats.name_col], uniqueplays/owned)
        if first:
            #results = np.array([[stats]])
            first = False
        else:
            #results = np.vstack((results, np.array([rank+1,i[0]+1])))
            pass
    else:
        #not found
        print("couldn't find #", rank+1, gameid, "in most played");



