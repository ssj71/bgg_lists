#!/usr/bin/env python3

import bgg_get_game_stats as bggstats
import bgg_most_played as bggmp
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
import datetime
import time

month = datetime.datetime.now().month
year = datetime.datetime.now().year-2000
monthwindow = 6 #window size in months

top = bggtr.getTopRankedGames(5)
print("top done",time.time())
mostplayed = bggmp.getTopPlayedGamesTill(year = year, month = month, window = monthwindow, pages = 10) #top played 
print("plays done",time.time())
stats = bggstats.getStatsSlowly(top)

first = True
for rank,gameid in enumerate(top):
    i = np.where( mostplayed[:,bggmp.gameid_col] == gameid )[0]
    if i.size:
        #it was found
        uniqueplays = int(mostplayed[i,bggmp.uniqueplays_col])
        owned = int(stats[rank,bggstats.owned_col])
        idnum = int(stats[rank,bggstats.gameid_col])
        #print(rank, stats[rank,bggstats.name_col], mostplayed[i,bggmp.rank_col], uniqueplays/owned)
        row = np.array([rank, idnum,  mostplayed[i,bggmp.rank_col], uniqueplays,owned, uniqueplays/owned])
        if first:
            results = np.array([row])
            names = [stats[rank,bggstats.name_col],] 
            first = False
        else:
            results = np.vstack((results, row))
            names.append(stats[rank,bggstats.name_col]) 
    else:
        #not found
        #print("couldn't find #", rank+1, stats[rank,bggstats.name_col], gameid, "in most played");
        pass

#save results?
#load last month results
print("sorting",time.time())
print("")
results.view('f8,'*6)[::-1].sort( order=['f4'], axis=0)
for i,row in enumerate(results):
    print(i, int(row[0]), names[i], int(row[1]))
    print("\tno.", int(row[2]+1), "most played game (", int(row[3]), " unique users )\n")
    print("\tOwned:",int(row[4]),"\n")
    print("\tTable/Shelf Ratio:",row[5]*100,"%\n\n")


