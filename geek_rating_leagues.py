#!/usr/bin/env python3
#spencer jackson

#look at the top 100 ranked games to visualize the "gaps" between different ratings

import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
import bgg_get_historicals as bgh

#plot the top ranked games by geekrating to see the natural groupings and gaps

#top = bggtr.getTopRankedGames(1)
#print(top)
#stats = bggstats.getStatsSlowly(top)
stats = bgh.get_date(2022,5,31)


#for row in stats[0:100,:]:
#    print("%s %s"% (row[bgh.rank_col], row[bgh.name_col]))
print(stats.shape)
matplot.scatter(np.arange(1,101),stats[:100,bgh.geekrating_col].astype(np.float))
matplot.ylabel('geek rating')
matplot.xlabel('game')
matplot.title("top ranked games by geek rating (31 May '22)")
for x,y in zip(np.arange(1,101),stats[:100,bgh.geekrating_col].astype(np.float)):
    matplot.text(x,y+.01,stats[x-1,bgh.name_col],rotation="vertical",color="red", fontsize=10)
matplot.show()
