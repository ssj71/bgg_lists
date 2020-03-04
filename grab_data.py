#!/usr/bin/env python3

#this snags the play data from bgg by date range
import urllib.request
import re
import copy
import calendar
import numpy as np
import bgg_most_played as bgg
import matplotlib.pyplot as matplot

#takes a 3d matrix from bgg_most_played and
#returns a 2d matrix with averaged rank, and summed play stats
def flatten(mat):
    groups = mat.shape[0]
    rows = mat.shape[1]
    out = np.array(mat[0]) #start with the first submatrix
    for g in range(1,groups):
        for r in range(rows):
            game = mat[g,r,1]
            i = np.where( out[:,1] == game )[0]
            if(i.size):
                #game is already in the matrix
                i = i[0]
                for c in (0, 2, 3):
                    out[i,c] += mat[g,r,c]
            else:
                #append row to matrix
                out = np.vstack([out,mat[g,r]])
    #average the rankings
    out[:,0] /= groups
    return out

#takes a 3d matrix from bgg_most_played and
#returns a matrix of games rank per time period for plotting
def ranktrends(top):
    (nperiods, ngames, col) = top.shape
    gamelist = top[0,:,1]
    avgrank = np.zeros([ngames,1])
    trends = np.ones([ngames,nperiods])*(ngames+1)
    for period_index, period in enumerate(top):
        for game in period:
            gameid = game[bgg.gameid_col]
            rank = game[bgg.rank_col]
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

def topNtrends(trends, n):
    a = trends[np.any(trends < n, axis=1),:]
    print(a.shape)
    return trends[np.any(trends < n, axis=1), :]

def loadyear(year = 19, window = 1):
    title = "t"+str(window)+"m"+str(year)
    try:
       data = np.load( title+".npy" )
    except IOError:
        print("could't find "+str(year)+" "+str(window)+ " data")
        a = bgg.getTopPlayedGames( startyear = 2000+year, startmonth = 1, timerangemonths = window , pages = 5 )
        data = np.array([a,])
        for m in range(1+window,13,window):
            print(m)
            a = bgg.getTopPlayedGames( startyear = 2000+year, startmonth = m, timerangemonths = window , pages = 5 )
            data = np.append(data,np.array([a]),axis=0)
        np.save(title,data)
    return data

if False:
    try:
       t12m = np.load( "t12m.npy" )
    except IOError:
        print("could't find 12m data")
        a = bgg.getTopPlayedGames( startmonth = 1, timerangemonths = 12 , pages = 5 )
        t12m = np.array([a])
        np.save( "t12m", t12m )

    try:
       t6m = np.load( "t6m.npy" )
    except IOError:
        print("could't find 6m data")
        a = bgg.getTopPlayedGames( startmonth = 1, timerangemonths = 6 , pages = 5 )
        b = bgg.getTopPlayedGames( startmonth = 7, timerangemonths = 6 , pages = 5 )
        t6m = np.array([a,b])
        np.save( "t6m", t6m )

    try:
       t3m = np.load( "t3m.npy" )
    except IOError:
        print("could't find 3m data")
        a = bgg.getTopPlayedGames( startmonth = 1, timerangemonths = 3 , pages = 5 )
        b = bgg.getTopPlayedGames( startmonth = 4, timerangemonths = 3 , pages = 5 )
        c = bgg.getTopPlayedGames( startmonth = 7, timerangemonths = 3 , pages = 5 )
        d = bgg.getTopPlayedGames( startmonth = 10, timerangemonths = 3 , pages = 5 )
        t3m = np.array([a,b,c,d])
        np.save( "t3m", t3m )

    try:
       t1m = np.load( "t1m.npy" )
    except IOError:
        print("could't find 1m data")
        a = bgg.getTopPlayedGames( startmonth = 1, timerangemonths = 1 , pages = 5 )
        b = bgg.getTopPlayedGames( startmonth = 2, timerangemonths = 1 , pages = 5 )
        c = bgg.getTopPlayedGames( startmonth = 3, timerangemonths = 1 , pages = 5 )
        d = bgg.getTopPlayedGames( startmonth = 4, timerangemonths = 1 , pages = 5 )
        e = bgg.getTopPlayedGames( startmonth = 5, timerangemonths = 1 , pages = 5 )
        f = bgg.getTopPlayedGames( startmonth = 6, timerangemonths = 1 , pages = 5 )
        g = bgg.getTopPlayedGames( startmonth = 7, timerangemonths = 1 , pages = 5 )
        h = bgg.getTopPlayedGames( startmonth = 8, timerangemonths = 1 , pages = 5 )
        i = bgg.getTopPlayedGames( startmonth = 9, timerangemonths = 1 , pages = 5 )
        j = bgg.getTopPlayedGames( startmonth = 10, timerangemonths = 1 , pages = 5 )
        k = bgg.getTopPlayedGames( startmonth = 11, timerangemonths = 1 , pages = 5 )
        l = bgg.getTopPlayedGames( startmonth = 12, timerangemonths = 1 , pages = 5 )
        t1m = np.array([a,b,c,d,e,f,g,h,i,j,k,l])
        np.save( "t1m", t1m )
 
t1m = loadyear(year = 19, window = 1);

print(t1m.shape)
t1mflattened = flatten(t1m)
t1mflattened.view('f8,f8,f8,f8')[::-1].sort( order=['f3'], axis=0)
#print(t1mflattened.shape)
#print(t12m[:,:10,:], "\n\n" , t1mflattened[:10,:])

trends  = ranktrends(t1m);
#print(trends[:10,:])
print(trends.shape)

#matplot.plot( np.r_[:12], trends[0,2:])
#matplot.plot( trends[:10,2:].T)
matplot.plot( topNtrends(trends,10)[:,2:].T )
matplot.ylabel('rank')
matplot.xlabel('month')
matplot.title("most played games")
matplot.axis([0, 11, -.5, 25])
matplot.gca().invert_yaxis()
matplot.show()
