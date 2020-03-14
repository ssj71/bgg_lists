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

#compareWindows(18)
plot2YearTrends(18,1,50)
matplot.show()
