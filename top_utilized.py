#!/usr/bin/env python3

import bgg_get_game_stats as bggstats
import bgg_most_played as bggmp
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
import datetime

month = datetime.datetime.now().month
year = datetime.datetime.now().year-2000
monthwindow = 6 #window size in months

top = bggtr.getTopRankedGames(5)
mostplayed = bggmp.getTopPlayedGamesTill(year = year, month = month, window = monthwindow, pages = 10) #top played


first = True
stats = bggstats.getStatsSlowly(top)
for rank,gameid in enumerate(top):
    i = np.where( mostplayed[:,bggmp.gameid_col] == gameid )[0]
    if i.size:
        #it was found
        uniqueplays = mostplayed[i,bggmp.uniqueplays_col]
        owned = int(stats[rank,bggstats.owned_col])
        print(rank, stats[rank,bggstats.name_col], mostplayed[i,bggmp.rank_col], uniqueplays/owned)
        if first:
            #results = np.array([[stats]])
            first = False
        else:
            #results = np.vstack((results, np.array([rank+1,i[0]+1])))
            pass
    else:
        #not found
        print("couldn't find #", rank+1, stats[rank,bggstats.name_col], gameid, "in most played");



