#!/usr/bin/env python3
#spencer jackson

#look at the top 10 ranked games in different weight "classes"

import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
import regression as reg

top = bggtr.getTopRankedGames(5)
stats = bggstats.getStatsSlowly(top)


exit()
# this method undoes the shill filter
ratetio = stats[:,bggstats.rating_col].astype(np.float)/stats[:,bggstats.geekrating_col].astype(np.float) # get it? xD
nvotes = stats[:,bggstats.voters_col].astype(np.int)
l = stats.shape[0]

tot  = np.array([ np.r_[:l] , ratetio.T]).T
slist = tot[tot[:,1].argsort()[::-1]]

for inx in slist[:50,0]:
    i = int(inx)
    print(stats[i, bggstats.gameid_col], stats[i, bggstats.name_col])
    print("avg rating:", stats[i, bggstats.rating_col], "\ngeek rating:", stats[i, bggstats.geekrating_col], "\nratio:",  float(stats[i, bggstats.rating_col])/float(stats[i, bggstats.geekrating_col]) )
    print("voters:", stats[i, bggstats.voters_col], "\nyear published:", stats[i, bggstats.year_col], "\n")

exit()
matplot.scatter(x, disparity)
matplot.plot(x, y, 'k')

matplot.show()
