#!/usr/bin/env python3
#spencer jackson

#look at how the top played games is correlated (or not) with the top ranked games

import bgg_get_game_stats as bggstats
import bgg_most_played as bggmp
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot

monthwindow = 1 #number of months (1,3,6) to look at for the most played (by unique users)
month = 12 #month (1-12) to consider

t6m = bggmp.loadyear(19,monthwindow) #top played

#plan b iterate over top100 to see where they rank in most played
top = bggtr.getTopRankedGames(5)
first = True
for rank,gameid in enumerate(top):
    i = np.where( t6m[month-1,:,bggmp.gameid_col] == gameid )[0]
    if i.size:
        #it was found
        print("#",rank+1,"=",i[0]+1,"most played", gameid)
        if first:
            results = np.array([[rank+1,i[0]+1]])
            first = False
        else:
            results = np.vstack((results, np.array([rank+1,i[0]+1])))
    else:
        #not found
        print("couldn't find #", rank+1, gameid);
    

print(results.shape)
matplot.scatter(results[:,0],results[:,1])
matplot.show()
