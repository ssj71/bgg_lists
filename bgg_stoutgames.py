#!/usr/bin/env python3

#spencer jackson

#a script to create a table ranking a list of games on boardgamegeek.com by "stoutness"

#a "stout" game is one that is short but heavy. The more tough decisions that can be crammed into a brief play time the better.  This script calculates "stoutness" by the weight divided by the min play length. Both of those statistics are highly variable so the results are very arguable, but it's a decent starting point.

from bgg_top100 import top
import untangle
import time

size = 10
delay = 5


for i in range(0,100,size):
    group = top[i:i+size]
    url = "https://www.boardgamegeek.com/xmlapi/boardgame/" + ",".join(str (n) for n in group) + "?stats=1"
    xml =  untangle.parse(url)
    for j in range(size):
        game = xml.boardgames.boardgame[j]
        name = [name.cdata for name in game.name if name['primary']=='true'][0]
        minlen = float(game.minplaytime.cdata)/60.0
        maxlen = float(game.maxplaytime.cdata)/60.0
        weight = float(game.statistics.ratings.averageweight.cdata)
        rank = int(game.statistics.ratings.ranks.rank[0]['value'])
        print(rank,name, minlen, weight/minlen, weight/maxlen,sep=", ")

    time.sleep(delay)

        

