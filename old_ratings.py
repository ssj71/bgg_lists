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
import urllib.parse
import re

rgame_col = 0
ruser_col = 1
rating_col = 2
rdate_col = 3

ntop = 100

allname = "top_100_all_raters_23_2"

try:
    allgames = np.load(allname+'.npy')
    stats = np.load(allname+"stats.npy").astype('U100')
    startat = np.count_nonzero(stats[:,bggstats.gameid_col])
    if startat == ntop:
        #TODO: if the last game gets messed up we won't get this right
        skip = True
    else:
        skip = False
except:
    allgames = np.zeros((0),'i4, U100, f4, i4') #when each game is done the resulting matrix will get appended to this array
    stats = np.zeros((ntop,14),dtype='U100')
    skip = False
    startat = 0

top = bgg_historicals.get_date(2023,2,24)[:ntop,bgg_historicals.gameid_col]

#instead use XML API 2

if not skip:
    #two steps
    print("getting all ratings for games")
    for g, gid in enumerate(top[startat:],startat):
        #first get all raters for a game
        url =  "https://boardgamegeek.com/xmlapi2/thing?id="+str(gid)+"&ratingcomments=1&stats=1"
        xml = untangle.parse(url)
        game = xml.items.item
        stats[g,:] = bggstats.getGameStats(xml)[0]

        nrat = int(game.comments['totalitems'])
        ratings = np.zeros(nrat+100,'i4, U100, f4, i4')
        pages = m.ceil(nrat/100) #pages 100 raters per page
        print("game", g, gid, stats[g,bggstats.name_col], nrat, flush=True)
        i = 0
        for user in game.comments.comment:
            ratings[i][rgame_col] = gid # or game['id']
            ratings[i][ruser_col] = user['username']
            ratings[i][rating_col] = float(user['rating'])
            #don't have the date yet
            i+=1

        #now repeat until there are no more pages with comments
        p = 2
        url =  "https://boardgamegeek.com/xmlapi2/thing?id=" + str(gid) + "&ratingcomments=1&page=" + str(p)
        xml = untangle.parse(url)
        game = xml.items.item
        while hasattr(game.comments,'comment'):
            print(p,end=',',flush=True)
            for user in game.comments.comment:
                #TODO: check that there wasn't an overlap from a new rating being insterted and getting repeated users
                ratings[i][rgame_col] = gid # or game['id']
                ratings[i][ruser_col] = user['username']
                ratings[i][rating_col] = float(user['rating'])
                #don't have the date yet
                i+=1
            time.sleep(2)
            p += 1
            url =  "https://boardgamegeek.com/xmlapi2/thing?id=" + str(gid) + "&ratingcomments=1&page=" + str(p)
            xml = untangle.parse(url)
            game = xml.items.item

        #because we don't know how many ratings all the games will have all together yet
        #we must stack. Since this will only be done 100x it's hopefully ok
        allgames = np.hstack((allgames,ratings[:i]))
        time.sleep(10)
        print()

        np.save(allname,allgames)
        np.save(allname+"stats",stats)
    exit()



#now we have a table of all voters, now we must get each user's collection data to see when they last updated their rating
# for example https://boardgamegeek.com/xmlapi2/collection?&id=174430,161936,291457,167791&stats=1&username=Terraformer
print("getting individual collections")
for rater in allgames:
    if not rater[rdate_col]:
        username = rater[ruser_col]
        idx = (allgames['f1']==username).nonzero()[0]
        usersgames = allgames[allgames['f1']==username]
        ids = usersgames['f0']
        url = "https://boardgamegeek.com/xmlapi2/collection?&id="+",".join(str(n) for n in ids) +"&username="+urllib.parse.quote(username)
        #these are just some debugging messages
        #print(rater)
        #print(username)
        #print(len(ids))
        #print(url)
        #print(len(ids))
        #print(usersgames)
        #exit()
        xml = untangle.parse(url)
        retry = 1
        while not hasattr(xml,'items'):
            time.sleep(retry*3)
            xml = untangle.parse(url)
            if retry == 2:
                np.save(allname,allgames)
                print('.',end='',flush=True)
            elif retry == 10:
                print("something wrong")
                print(url)
                exit()
            elif retry > 2:
                print('.',end='',flush=True)
            retry += 1

        #get rating dates and store (as sec from epoch)
        for game in xml.items.item:
            #print(game.status['lastmodified'], end=', ')
            d = int(dparse.parse(game.status['lastmodified']).timestamp())
            i = idx[usersgames['f0'] == int(game['objectid'])]
            for j in i:
                allgames[j][rdate_col] = d
        #double check the line we're currently on
        i = idx[usersgames['f0'] == rater[rgame_col]][0]
        print(i, end=',', flush=True)
        #print()
        if not allgames[i][rdate_col]:
            #somehow we didn't get the date we're looking for
            print("got issues")
            exit()
        np.save(allname,allgames)
        if not i%10:
            time.sleep(10)
    #else we already got them from a different game
    #go to next user
print("all done!")
exit()

#OLD STUFF
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

