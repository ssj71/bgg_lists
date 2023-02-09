#!/usr/bin/env python3
#spencer jackson

#look at all ranked games and compare the rating std deviation

import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
from datetime import date
import csv
import pandas as pd
import bgg_get_historicals as bgg_historicals

votes_required = 300

top = bgg_historicals.get_date(2022,5,31)[:,bgg_historicals.gameid_col]
stats = bggstats.getStatsSlowly(top)

reduced = stats[stats[:,bggstats.voters_col].astype("int") >= votes_required,:]

#matplot.scatter(stats[:,bggstats.voters_col].astype(np.int),stats[:,bggstats.stddev_col].astype(np.float))
#matplot.gca().set_xscale("log")
#matplot.show()

sortd = reduced[reduced[:,bggstats.stddev_col].argsort(),:]
print(reduced.shape, stats.shape)
print("\n\ngames we all agree on:")
for i in range(55):
    game = sortd[i]
    print()
    print()
    print(game[bggstats.gameid_col])
    print(i+1)
    print(game[bggstats.name_col], " (", game[bggstats.year_col], ")", sep="")
    print("Current Rank: %i" % int(game[bggstats.rank_col]))
    print("Average Rating: %.3f" % float(game[bggstats.rating_col]))
    print("Std. Dev.: %.3f" % float(game[bggstats.stddev_col]))
    print("Votes: %i" % int(game[bggstats.voters_col]))

print("\n\n\n\n****************************************************")
print("\n\n\n\ngames we can't agree on:")

revsort = sortd[::-1,:]
for i in range(55):
    game = revsort[i]
    print()
    print()
    print(game[bggstats.gameid_col])
    print(i+1)
    print(game[bggstats.name_col], " (", game[bggstats.year_col], ")", sep="")
    print("Current Rank: %i" % int(game[bggstats.rank_col]))
    print("Average Rating: %.3f" % float(game[bggstats.rating_col]))
    print("Std. Dev.: %.3f" % float(game[bggstats.stddev_col]))
    print("Votes: %i" % int(game[bggstats.voters_col]))

print("done.")

