#!/usr/bin/env python3

#this snags the play data from bgg by date range
import urllib.request
import re
import copy
import calendar
import numpy as np
import bgg_most_played as bgg

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

