#!/usr/bin/env python3

#spencer jackson

#a script to create a table calculating the "stoutness" of a list of games on boardgamegeek.com

#a "stout" game is one that is short but heavy. The more tough decisions that can be crammed into a brief play time the better.  This script calculates "stoutness" by the weight divided by the min play length. Both of those statistics are highly variable so the results are very arguable, but it's a decent starting point. It is heavily biased toward sub-hour length games, but I like it that way.

#this script takes several minutes to complete so keep your calm

from bgg_top100 import top1000
import untangle
import time

stride = 10 #number of entries to query at once
delay = 5 #time to wait between server queries
start = 0 #this should always be 0, except if debugging
parse = True #this should always be True, except if debugging

print("rank, name, minlen, weight/minlen, weight/maxlen") #header
top = top1000 #this is the list of game ids
for i in range(start,len(top),stride):
    group = top[i:i+stride]
    url = "https://www.boardgamegeek.com/xmlapi/boardgame/" + ",".join(str (n) for n in group) + "?stats=1"
    xml =  untangle.parse(url)
    if(parse):
        for j in range(stride):
            game = xml.boardgames.boardgame[j]
            name = [name.cdata for name in game.name if name['primary']=='true'][0]
            minlen = float(game.minplaytime.cdata)/60.0
            maxlen = float(game.maxplaytime.cdata)/60.0
            weight = float(game.statistics.ratings.averageweight.cdata)
            rankcategories = game.statistics.ratings.ranks.rank
            if len(rankcategories) > 1:
                rank = int(rankcategories[0]['value'])
            else:
                rank = int(rankcategories['value'])
            print(rank,name, minlen, weight/minlen, weight/maxlen,sep=", ")
    else:
        break
    time.sleep(delay)
