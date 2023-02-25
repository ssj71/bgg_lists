#!/usr/bin/env python3
#spencer jackson

#look at top 100 ranked games and re-order them by average rating when excluding anything within 2 years of release!

#it would be nice if we could adjust the geek rating but that algorithm is secret.
# we might just scale the gr proportionally to how the average changed
import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
from datetime import date
import dateutil.parser as dparse
import csv
import pandas as pd
import bgg_get_historicals as bgg_historicals
import math as m
import untangle
import time
import urllib.request
import re

rgame_col = 0
ruser_col = 1
rating_col = 2
rdate_col = 3

ntop = 100

allname = "top_100_all_raters_23_2"

try:
    allgames = np.load(allname)
    stats = np.load(allname+"_stats")
    skip = True
except:
    allgames = np.zeros((0),'i4, U100, f4, i4') #when each game is done the resulting matrix will get appended to this array
    stats = np.zeros((ntop,14),dtype='S')
    skip = False

top = bgg_historicals.get_date(2023,2,24)[:ntop,bgg_historicals.gameid_col]

#instead use XML API 2

if not skip:
    #two steps
    for g, gid in enumerate(top):
        #first get all raters for a game
        url =  "https://boardgamegeek.com/xmlapi2/thing?id="+str(gid)+"&ratingcomments=1&stats=1"
        xml = untangle.parse(url)
        game = xml.items.item
        stats[g,:] = bggstats.getGameStats(xml)[0]

        ratings = np.zeros(int(game.comments['totalitems'])+100,'i4, U100, f4, i4')
        pages = m.ceil(len(ratings)/100) #pages 100 raters per page
        print("game", g, gid, len(ratings), flush=True)
        i = 0
        for user in game.comments.comment:
            ratings[i][rgame_col] = gid # or game['id']
            ratings[i][ruser_col] = user['username']
            ratings[i][rating_col] = float(user['rating'])
            #don't have the date yet
            i+=1

        #now repeat for the rest of the pages
        for p in range(2,pages+1):
            url =  "https://boardgamegeek.com/xmlapi2/thing?id=" + str(gid) + "&ratingcomments=1&page=" + str(p)
            xml = untangle.parse(url)
            game = xml.items.item
            print(p,end=',',flush=True)
            for user in game.comments.comment:
                #may need to check if the rating is valid (could just be comment without rating)?
                ratings[i][rgame_col] = gid # or game['id']
                ratings[i][ruser_col] = user['username']
                ratings[i][rating_col] = float(user['rating'])
                #don't have the date yet
                i+=1
            time.sleep(2)

        #because we don't know how many ratings all the games will have all together yet
        #we must stack. Since this will only be done 100x it's hopefully ok
        allgames = np.hstack((allgames,ratings[:i]))
        time.sleep(10)
        print()

    np.save(allname,allgames)
    np.save(allname+"stats",stats)
    exit()
        

#now get all the pages of raters from here https://boardgamegeek.com/xmlapi2/thing?id=174430&ratingcomments=1&page=2 etc

url = "https://www.boardgamegeek.com/xmlapi2/thing?id=" + ",".join(str (int(n)) for n in top) + "&stats=1"
xml =  untangle.parse(url)

stats = bggstats.getStatsSlowly(top)

reduced = stats[stats[:,bggstats.voters_col].astype("int") >= votes_required,:]

#the only way to do this is to get all the pages of ratings on the item (game) then get each user's
#collection data
# for example https://boardgamegeek.com/xmlapi2/collection?&id=174430,161936,291457,167791&stats=1&username=Terraformer

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

