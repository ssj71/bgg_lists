#!/usr/bin/env python3
#spencer jackson

#checking how the average and median average rating of the games in the top 1000 have changed over time
import datetime
import numpy as np
import csv
import bgg_get_game_stats as bggstats
import pandas as pd
import matplotlib.pyplot as matplot

latest = datetime.date(2021, 7, 10)
oldest = datetime.date(2016, 10, 12)

#columns of csv
c_id = 0  #id
c_nm = 1  #name
c_yr = 2  #year published
c_rk = 3  #rank
c_av = 4  #average rating
c_gr = 5  #geek rating (bayesian)
c_nv = 6  #number voters

l = (latest-oldest).days

means = np.zeros(l)
meds = np.zeros(l)

for n in range(l):
    d = (oldest+datetime.timedelta(n))
    fn = d.strftime("%Y-%m-%d.csv")
    print("\r %s %.4f%%" %(fn, (100*n/l)),end="")
    m = pd.read_csv("bgg-ranking-historicals/"+fn).to_numpy()
    
    means[n] = np.mean(m[:1000,c_av])
    meds[n] = np.median(m[:1000,c_av])
    

matplot.plot( means )
matplot.plot( meds )

matplot.ylabel('average ratings')
matplot.xlabel('time (days)')

matplot.title("Change in top 1000 games' average rating statistics since %s" % oldest.strftime("%Y-%m-%d"))
matplot.legend(("average","median"))
matplot.show()
