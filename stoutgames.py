#!/usr/bin/env python3

#spencer jackson

#a script to create a table calculating the "stoutness" of a list of games on boardgamegeek.com

#a "stout" game is one that is short but heavy. The more tough decisions that can be crammed into a brief play time the better.  This script calculates "stoutness" by the weight divided by the min play length. Both of those statistics are highly variable so the results are very arguable, but it's a decent starting point. It is heavily biased toward sub-hour length games, but I like it that way.

#this script takes around 20 minutes to complete so keep your calm

import bgg_top_ranked as bggtr
import untangle
import time

top2500 = bggtr.getTopRankedGames(25)
stride = 10 #number of entries to query at once
delay = 4 #time (sec) to wait between server queries
start = 0 #this should always be 0, except if debugging
parse = True #this should always be True, except if debugging


##
# @brief  get xml from bgg
#
# @param ids list of game ids
#
# @return  untangle xml object
def getGameXML(ids):
    url = "https://www.boardgamegeek.com/xmlapi2/thing?id=" + ",".join(str (n) for n in ids) + "&stats=1"
    url = "https://www.boardgamegeek.com/xmlapi/boardgame/" + ",".join(str (n) for n in group) + "?stats=1"
    xml =  untangle.parse(url)
    return xml

top = top2500[0:100] #this is the list of game ids
print("rank","name", "minlen", "maxlen", "weight", "maxstout", "minstout", "stout", "string", sep=", ") #header
for i in range(start,len(top),stride):
    group = top[i:i+stride]
    #url = "https://www.boardgamegeek.com/xmlapi/boardgame/" + ",".join(str (n) for n in group) + "?stats=1"

    xml = getGameXML(group) #untangle.parse(url)
    if(parse):
        for j in range(stride):
            game = xml.boardgames.boardgame[j]
            name = [name.cdata for name in game.name if name['primary']=='true'][0]
            minlen = float(game.minplaytime.cdata)/60.0
            maxlen = float(game.maxplaytime.cdata)/60.0
            if maxlen <= 0:
                if minlen<=0:
                    continue #unpublished prototype shows up here
                maxlen = minlen
            if minlen <= 0:
                minlen = maxlen
            midlen = (maxlen + minlen)/2.0
            weight = float(game.statistics.ratings.averageweight.cdata)-1.0
            rankcategories = game.statistics.ratings.ranks.rank
            if len(rankcategories) > 1:
                rank = int(rankcategories[0]['value'])
            else:
                rank = int(rankcategories['value'])
            stats = f"Weight: {weight+1.0:.3f} Length: {midlen:.3f} hr (±{midlen-minlen:.3f}) Stout Score: {weight/midlen:.4f}"
            print(rank,name, minlen, maxlen, weight+1.0,sep=", ",end=", ")
            print(weight/minlen, weight/maxlen, weight/midlen, stats, sep=", ")
    else:
        break
    time.sleep(delay)
