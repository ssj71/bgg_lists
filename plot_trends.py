#!/usr/bin/env python3

#this snags the play data from bgg by date range
import urllib.request
import re
import copy
import calendar
import numpy as np
import bgg_most_played as bggmp
import matplotlib.pyplot as matplot

def plot2YearTrends(year = 19, window = 1, top = 10):
    tm = bggmp.loadyear(year,window);
    tm = np.append(tm,bggmp.loadyear(year+1,window),axis=0)

    trends  = bggmp.ranktrends(tm);
    matplot.plot( bggmp.topNtrends(trends,top)[:,2:].T )
    matplot.ylabel('rank')
    matplot.xlabel('month')
    matplot.title(str(top)+" most played games ranked by number of unique users each "+ str(window) +" months 20"+str(year)+"-20"+str(year+1))
    matplot.axis([0, trends.shape[1]-3, -.5, top+10])
    matplot.gca().invert_yaxis()
 
def compareWindows(year = 19):
    matplot.figure(0)
    plot2YearTrends(year, 1, 10)
    matplot.figure(1)
    plot2YearTrends(year, 3, 10)
    matplot.figure(2)
    plot2YearTrends(year, 6, 10)

    matplot.show()

def plotNYearTrend(gameid, startyear = 19, N = 2, window = 1):
    tm = bggmp.loadyear(startyear,window);
    for i in range(1,N):
        tm2 = bggmp.loadyear(startyear+i,window)
        tm = np.append(tm,tm2,axis=0)

    trends  = bggmp.ranktrends(tm);
    i = np.where(trends[:,0] == gameid)[0];
    if(i.size):
        matplot.plot( trends[i,2:].T+1 )
        matplot.ylabel('rank')
        matplot.xlabel('month')
    else:
        print("game not found!")

#compareWindows(18)
#plot2YearTrends(18,1,50)
games = np.array( [
    [265736,"Tiny Towns"],
    [197376,"Charterstone"],
    [174430, "Gloomhaven"],
    [148228, "Splendor"],
    [68448,  "7 Wonders"],
    [180263, "7th Continent"],
    [150376, "Dead of Winter"],
    [147020, "Star Realms"],
    [172, "For Sale"],
    [13, "Catan"],
    [28143, "Race FT Galaxy"],
    [285774, "Marvel Champs"],
    [478, "Citadels"],
    [16992, "Tsuro"],
    ])
strt = 10
yrs = 10
for row in games:
    plotNYearTrend(int(row[0]),strt,yrs)
matplot.legend(games[:,1])
#matplot.axis(matplot.axis()[:2]+(-.5, 270))
matplot.gca().set_yscale("log")
matplot.gca().invert_yaxis()

#do again with a 12 month window
matplot.figure()
for row in games:
    plotNYearTrend(int(row[0]),strt,yrs,12)
matplot.legend(games[:,1])
#matplot.axis(matplot.axis()[:2]+(-.5, 270))
matplot.gca().set_yscale("log")
matplot.gca().invert_yaxis()

matplot.show()
