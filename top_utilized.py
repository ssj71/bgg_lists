#!/usr/bin/env python3

import bgg_get_game_stats as bggstats
import bgg_most_played as bggmp
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
import datetime
import time

month = datetime.datetime.now().month-1
if month == 0:
    month = 12
year = datetime.datetime.now().year-2000
monthwindow = 6 #window size in months

start = time.time()
print("start",start)

top = bggtr.getTopRankedGames(10)
print("top done",time.time()-start)
mostplayed = bggmp.getTopPlayedGamesTill(year = year, month = month, window = monthwindow, pages = 10) #top played 
print("plays done",time.time()-start)
stats = bggstats.getStatsSlowly(top)

first = True
for rank,gameid in enumerate(top):
    i = np.where( mostplayed[:,bggmp.gameid_col] == gameid )[0]
    if i.size:
        #it was found
        uniqueplays = int(mostplayed[i,bggmp.uniqueplays_col])
        totalplays = int(mostplayed[i,bggmp.plays_col])
        owned = int(stats[rank,bggstats.owned_col])
        idnum = int(stats[rank,bggstats.gameid_col])
        year = int(stats[rank,bggstats.year_col])
        #print(rank, stats[rank,bggstats.name_col], mostplayed[i,bggmp.rank_col], uniqueplays/owned)
        row = np.array([rank, idnum,  mostplayed[i,bggmp.rank_col], uniqueplays,owned, uniqueplays/owned, totalplays, year])
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
print("sorting",time.time()-start)
print("")
results.view('f8,'*8)[::-1].sort( order=['f5'], axis=0)
for i,row in enumerate(results[:,:]):
    print(i+1, int(row[0]), stats[int(row[0]),bggstats.name_col], int(row[1]),"\n")
    print("\n\tPublished:",int(row[7]))
    print("\n\tNo.", int(row[2]+1), "most played game \n\tUnique players:", int(row[3]))
    print("\tOwned:",int(row[4]))
    print("\tTable/Shelf Ratio: %.3f%%"%(row[5]*100))
    print("\n\tAverage times played per player: %.1fx\n\n"%(row[6]/row[3]))


print("script complete",time.time()-start)

