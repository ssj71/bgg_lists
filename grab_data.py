#!/usr/bin/env python3

#this snags the play data from bgg by date range
import urllib.request
import re
import copy
import calendar
import numpy as np
import bgg_most_played as bggmp
import matplotlib.pyplot as matplot

 
def compareWindows(year = 11):
    t1m = bggmp.loadyear(year,1);
    t1m = np.append(t1m,bggmp.loadyear(year+1,1),axis=0)

    t1mflattened = bggmp.flatten(t1m)
    t1mflattened.view('f8,f8,f8,f8')[::-1].sort( order=['f3'], axis=0)

    trends  = bggmp.ranktrends(t1m);
    matplot.figure(0)
    matplot.plot( bggmp.topNtrends(trends,10)[:,2:].T )
    matplot.ylabel('rank')
    matplot.xlabel('month')
    matplot.title("most played games ranked by number of unique users each month")
    matplot.axis([0, trends.shape[1]-3, -.5, 20])
    matplot.gca().invert_yaxis()


    t3m = bggmp.loadyear(year,3);
    t3m = np.append(t3m,bggmp.loadyear(year+1,3),axis=0)

    trends3  = bggmp.ranktrends(t3m);
    matplot.figure(1)
    matplot.plot( bggmp.topNtrends(trends3,10)[:,2:].T )
    matplot.ylabel('rank')
    matplot.xlabel('month')
    matplot.title("most played games ranked by number of unique users each quarter")
    matplot.axis([0, trends3.shape[1]-3, -.5, 20])
    matplot.gca().invert_yaxis()

    t6m = bggmp.loadyear(year,6);
    t6m = np.append(t6m,bggmp.loadyear(year+1,6),axis=0)

    trends6  = bggmp.ranktrends(t6m);
    matplot.figure(2)
    matplot.plot( bggmp.topNtrends(trends6,10)[:,2:].T )
    matplot.ylabel('rank')
    matplot.xlabel('month')
    matplot.title("most played games ranked by number of unique users semi-anually")
    matplot.axis([0, trends6.shape[1]-3, -.5, 20])
    matplot.gca().invert_yaxis()

    matplot.show()

compareWindows(18)

