#!/usr/bin/env python3
#spencer jackson

#games that have gone down in BGG rating the most in beefsack's historical data
import datetime
import numpy as np
import csv
import bgg_get_game_stats as bggstats
import pandas as pd

latest = datetime.date(2021, 6, 18)
oldest = datetime.date(2016, 10, 12)
#columns of csv
c_id = 0
c_nm = 1
c_yr = 2
c_rk = 3
c_av = 4
c_gr = 5
c_nv = 6

#start with the latest values (we expect it to have the complete list of games)
d = latest
fn = d.strftime("%Y-%m-%d.csv")
m = pd.read_csv("bgg-ranking-historicals/"+fn).to_numpy()
l = m.shape[0]
#peaks is gameid, gr peak, date, rank, gr min, date, rank,  rating drop (percent), rank drop (percent)
peaks = np.array([m[:,c_id].T, m[:,c_gr].T, np.ones(l)*d.toordinal(), m[:,c_rk], m[:,c_gr].T, np.ones(l)*d.toordinal(), m[:,c_rk], np.zeros(l), np.zeros(l)]).T
#sort by game id
#peaks.sort(axis=0)
peaks = peaks[peaks[:,0].argsort(),:]
tot = 90#(latest-oldest).days
for n in range(tot):
    print("\r ",100*n/tot,end="")
    d = (latest-datetime.timedelta(n))
    fn = d.strftime("%Y-%m-%d.csv")
    #we skip the string name so the cols of m are:
    #game id, year, rank, avg, geek rating, no. ratings
    m = pd.read_csv("bgg-ranking-historicals/"+fn).to_numpy()
    idx = np.searchsorted(peaks[:,0],m[:,c_id])

    #find those that were higher before
    fallers = m[:,c_gr] > peaks[idx,1]
    ndx = idx[fallers]
    peaks[ndx,1] = m[fallers,c_gr] #geek rating
    peaks[ndx,2] = d.toordinal() #date
    peaks[ndx,3] = m[fallers,c_rk] #rank

    #find those that were lower before
    #because we can't make sure this isn't before the peak, we just use the most recent as lowest
    #risers = m[:,c_gr] < peaks[idx,1]
    #ndx = idx[risers]
    #peaks[ndx,4] = m[risers,c_gr] #geek rating
    #peaks[ndx,5] = d.toordinal() #date
    #peaks[ndx,6] = m[risers,c_rk] #rank

print()
#calculate percent change in geek rating
peaks[:,7] = 100*(peaks[:,1]-peaks[:,4])/ peaks[:,1]
#do the same with rank
peaks[:,8] = 100*(peaks[:,3]-peaks[:,6]) / peaks[:,3]
#sort by fall
sordid = peaks[peaks[:,7].argsort(),:]
#find ones that fell rather than climbed
fallers = sordid[:,2] < sordid[:,5]
ids = (sordid[fallers,0])[-110:]
stats = bggstats.getStatsSlowly(ids)
i = 1
for n in range(50):
    w = np.array([])
    while w.size == 0:
        fell = (sordid[fallers])[-i]
        w = np.where(stats[:,bggstats.gameid_col].astype(np.float) == fell[0])[0]
        i += 1
    sts = stats[w][0]
    print()
    print()
    print(i-1)
    print(sts[bggstats.gameid_col], fell[0])
    print(n+1)
    print(sts[bggstats.name_col], " (", sts[bggstats.year_col], ")", sep="")
    print("peak: ", fell[1], " (rank ", int(fell[3]), ") ", datetime.date.fromordinal(int(fell[2])).strftime("%d-%b-%y"), sep="" )
    #print("min: ", fell[4], datetime.date.fromordinal(int(fell[5])).strftime("%d-%b-%y"), "(rank ", fell[6], ")") 
    print("current: ", fell[4]," (rank ", int(fell[6]), ")", sep="") 
    print("change: ", fell[4]-fell[1],",", fell[7],"% (", fell[8], "% rank)")
print("done.")
