#!/usr/bin/env python3

#spencer jackson

import untangle
import time
import numpy as np

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
def getGameXML2(ids):
    url = "https://www.boardgamegeek.com/xmlapi2/thing?id=" + ",".join(str (n) for n in ids) + "&stats=1"
    xml =  untangle.parse(url)
    return xml

##
# @brief  get stats from bgg xml
#
# @param items untangle object from bgg with a collecton of boardgame entries
#
# @return numpy array with boardgame data
def getGameStats(items):
    for game in items:
        name = [name.cdata for name in game.name if name['type']=='primary']
        game.id.cdata
        minlen = game.minplaytime.cdata
        maxlen = game.maxplaytime.cdata
        if maxlen <= 0:
            if minlen<=0:
                continue #unpublished prototype shows up here
            maxlen = minlen
        if minlen <= 0:
            minlen = maxlen
        weight = float(game.statistics.ratings.averageweight.cdata)
        rankcategories = game.statistics.ratings.ranks.rank
        if len(rankcategories) > 1:
            rank = int(rankcategories[0]['value'])
        else:
            rank = int(rankcategories['value'])
    

def getGameStatsHeader():
    return ("rank", "name", "id", "minlen", "maxlen", "weight", "owned")

#some game ids for testing
ids = [1.67791e+05,2.04583e+05,1.78900e+05,1.48228e+05,1.69786e+05,1.73346e+05, 6.84480e+04,2.30802e+05,2.09685e+05,1.63412e+05,8.22000e+02,1.74430e+05, 1.99561e+05,3.00000e+00,5.00000e+00,2.44992e+05,2.33867e+05,2.44521e+05, 2.36457e+05,2.54640e+05,2.66192e+05,2.86096e+05]

exit()

top = top2500[0:100] #this is the list of game ids

print("rank","name", "minlen", "maxlen", "weight", "maxstout", "minstout", "stout", "string", sep=", ") #header
for i in range(start,len(top),stride):
    group = top[i:i+stride]
    #url = "https://www.boardgamegeek.com/xmlapi/boardgame/" + ",".join(str (n) for n in group) + "?stats=1"

    xml = getGameXML2(group) #untangle.parse(url)
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
