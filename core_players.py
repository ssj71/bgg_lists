#spencer jackson

#figure out how many unique players played in both halves of the past 12 months relative to the number of copies owned

import bgg_most_played as bggmp
import numpy as np

gameid_col = 0
rank0_col = 1 #rank in period for most unique plays
rank1_col = 2 #rank in period for most unique plays
rank2_col = 3 #rank in period for most unique plays
uniqueplays0_col = 4
uniqueplays1_col = 5
uniqueplays2_col = 6

def combinePeriods(top):
    (nperiods, ngames, col) = top.shape
    gamelist = top[0,:,bggmp.gameid_col]
    avgrank = np.zeros([ngames,1])
    trends = np.ones([ngames,nperiods])*(ngames+1)
    for period_index, period in enumerate(top):
        for game in period:
            gameid = game[gameid_col]
            rank = game[rank_col]
            i = np.where( gamelist == gameid )[0]
            if(i.size):
                #update game
                avgrank[i] += rank
                trends[i,period_index] = rank
            else:
                #append
                gamelist = np.append(gamelist, gameid)
                avgrank = np.append(avgrank, rank+period_index*(ngames+1))
                trends = np.append(trends, np.ones([1,nperiods])*(ngames+1), axis=0)
                trends[-1,-1] = rank
    out = np.vstack((gamelist,avgrank,trends.T)).T
    return out#out.view('f8,'*out.shape[1]).sort( order=['f0'], axis=0)

def findGame(gameid, annual, first, second):
    i = np.where(annual[:,bggmp.gameid_col] == gameid)[0]
    if(i.size):
        a = annual[i,:]
    else:
       return np.array([])
    i = np.where(first[:,bggmp.gameid_col] == gameid)[0]
    if(i.size):
        f = first[i,:]
    else:
       return np.array([])
    i = np.where(second[:,bggmp.gameid_col] == gameid)[0]
    if(i.size):
        s = second[i,:]
    else:
       return np.array([])
    return np.vstack([a,f,s])

def getCore(gameids, year = 0, month = 0):
    #if no year/month given use current
    if year == 0:
        year = datetime.datetime.now().year-2000
    if month == 0:
        month = datetime.datetime.now().month-1
    if month == 0:
        year -= 1
        month = 12
    if month > 6:
        prevmonth = month-6
        prevyear = year
    else:
        prevmonth = month + 6
        prevyear = year-1

    firsthalf = bggmp.getTopPlayedGamesTill(prevyear, prevmonth, 6, 10)
    secondhalf = bggmp.getTopPlayedGamesTill(year, month, 6, 10)
    annual = bggmp.getTopPlayedGamesTill(year, month, 12, 10)

    #ToDo get stats slowly for owned info

    #now need to flatten into unique players, and rank by period
    for game in gameids:
        playstats = findGame(game, annual, firsthalf, secondhalf)
        totplayers = playstats[0,bggmp.uniqueplays_col]
        firstplayers = playstats[0,bggmp.uniqueplays_col]
        coreplayers = totplayers - firstplayers
        print(game, 
