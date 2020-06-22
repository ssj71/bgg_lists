#!/usr/bin/env python3

#spencer jackson

import untangle
import time
import numpy as np


stride = 50 #number of entries to query at once
delay = 2 #time (sec) to wait between server queries


rank_col   = 0
name_col   = 1
gameid_col = 2
minlen_col = 3
maxlen_col = 4
weight_col = 5
owned_col  = 6
year_col   = 7
rating_col = 8

num_col = 9

##
# @brief  get xml from bgg
#
# @param ids list of game ids
#
# @return  untangle xml object
def getGameXML2(ids):
    url = "https://www.boardgamegeek.com/xmlapi2/thing?id=" + ",".join(str (int(n)) for n in ids) + "&stats=1"
    xml =  untangle.parse(url)
    return xml

##
# @brief  get stats from bgg xml
#
# @param items untangle object from bgg with a collecton of boardgame entries
#
# @return numpy array with boardgame data
def getGameStats(items):
    first = True
    for game in items.items.item:
        name = [name['value'] for name in game.name if name['type']=='primary'][0]
        idnum = int(game['id'])
        minlen = int(game.minplaytime['value'])
        maxlen = int(game.maxplaytime['value'])
        if maxlen <= 0:
            if minlen<=0:
                continue #unpublished prototype shows up here
            maxlen = minlen
        if minlen <= 0:
            minlen = maxlen
        weight = float(game.statistics.ratings.averageweight['value'])
        rankcategories = game.statistics.ratings.ranks.rank
        rank = [int(rank['value']) for rank in game.statistics.ratings.ranks.rank if rank['id']=='1'][0]
        rating = float(game.statistics.ratings.average['value'])
        if len(rankcategories) > 1:
            rank = int(rankcategories[0]['value'])
        else:
            rank = int(rankcategories['value'])
        owned = game.statistics.ratings.owned['value']
        year = int(game.yearpublished['value'])
        row = np.array([rank,name,idnum,minlen,maxlen,weight,owned,year,rating])
        if(first):
           out = np.array([row,]) 
        else:
            out = np.vstack([out,row])
        first = False
    return out
    
def getGameStatsRowType():
    return 'i4, object, i4, i4, i4, f4, i4, i4, f4'


def getGameStatsHeader():
    return ("rank", "name", "id", "minlen", "maxlen", "weight", "owned", "year", "rating")

def getStatsSlowly(ids):
    first = True
    print("getting stats",end=" ")
    for i in range(0,len(ids),stride):
        block = ids[i:i+stride]
        stats = getGameStats(getGameXML2(block))
        if first:
            out = stats
            first = False
        else:
            out = np.vstack((out,stats))
        print(len(block),end=" ", flush=True)
        time.sleep(delay)
    print("done", flush=True)
    return out


#some game ids for testing
ids = [167791,204583,178900,1.48228e+05,1.69786e+05,1.73346e+05, 6.84480e+04,2.30802e+05,2.09685e+05,1.63412e+05,8.22000e+02,1.74430e+05, 1.99561e+05,3.00000e+00,5.00000e+00,2.44992e+05,2.33867e+05,2.44521e+05, 2.36457e+05,2.54640e+05,2.66192e+05,2.86096e+05]

#print(getGameStatsHeader(), "\n", getGameStats(getGameXML2(ids[0:4])))
