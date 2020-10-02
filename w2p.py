#!/usr/bin/env python3
#spencer jackson

#look at the top ranked games for different lengths and player counts

import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot

ntop = 5 # number to include in each category
nplayers = 8 # max number of players to look at
times = np.array([15,30,45,60,90])

def playlength(mintime, maxtime, playermin, playermax):
    if playermax != playermin:
        per = (maxtime - mintime)/(playermax - playermin)
    else:
        per = 0.0
    base = mintime - playermin*per
    return (base, per)

top = bggtr.getTopRankedGames(20)
print(len(top))
stats = bggstats.getStatsSlowly(top)
#playtimes = np.zeros([len(times),nplayers]

first = True
topN = np.empty([nplayers,len(times),ntop], dtype=bggstats.getGameStatsRowType())
for game in stats:
    playmin = float(game[bggstats.minlen_col])
    playmax = float(game[bggstats.maxlen_col])
    playermin = int(game[bggstats.minplayer_col])
    playermax = int(game[bggstats.maxplayer_col])

    (base, per) = playlength( playmin, playmax, playermin, playermax )
    #print(playmin, playmax, playermin, playermax)
    #print(base,per,"\n")
    if(playermax > nplayers):
        playermax = nplayers;

    for players in range(playermin-1, playermax):
        for t in range(len(times)):
            if base+per*players+per <= times[t]:
                if topN[players,t,-1][2] == 0:
                    #still slots in the category
                    for i in range(ntop):
                        if topN[players,t,i][2] == 0:
                            for j in range(len(game)):
                                topN[players,t,i][j] = game[j]
                            break
                break #don't put this game in any other time categories

#print out results
for n in range(nplayers):
    for t in range(len(times)):
        for r in range(ntop):
            game = topN[n,t,r]

            playmin = float(game[bggstats.minlen_col])
            playmax = float(game[bggstats.maxlen_col])
            playermin = int(game[bggstats.minplayer_col])
            playermax = int(game[bggstats.maxplayer_col])

            (base, per) = playlength( playmin, playmax, playermin, playermax )

            print(game[bggstats.gameid_col], game[bggstats.name_col])
            print("#", str(r+1), " - ", str(n+1)," player game", sep="")
            print("     %i minutes or less\n     (%.2f expected)\n" %( times[t],  (base+per+per*n)))
