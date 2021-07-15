#!/usr/bin/env python3
#spencer jackson

#games that have gone down in BGG rating the most in beefsack's historical data
import datetime
import numpy as np
import csv
import bgg_get_game_stats as bggstats
import pandas as pd

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

#start with the latest values (we expect it to have the complete list of games)
d = latest
fn = d.strftime("%Y-%m-%d.csv")
m = pd.read_csv("bgg-ranking-historicals/"+fn).to_numpy()
l = m.shape[0]
#peaks is gameid, gr peak, date, rank, votes, gr min, date, rank,  rating drop (percent), rank drop (percent), published year
peaks = np.array([m[:,c_id].T, m[:,c_gr].T, np.ones(l)*d.toordinal(), m[:,c_rk].T, m[:,c_nv].T, m[:,c_gr].T, np.ones(l)*d.toordinal(), m[:,c_rk].T, np.zeros(l), np.zeros(l), m[:,c_yr].T]).T
#sort by game id
#peaks.sort(axis=0)
peaks = peaks[peaks[:,0].argsort(),:]
tot = (latest-oldest).days
for n in range(tot):
    d = (latest-datetime.timedelta(n))
    fn = d.strftime("%Y-%m-%d.csv")
    print("\r %s %.4f%%" %(fn, (100*n/tot)),end="")

    #get the next historical data set
    m = pd.read_csv("bgg-ranking-historicals/"+fn).to_numpy()
    #find where the games are in the first set
    idx = np.searchsorted(peaks[:,0],m[:,c_id])
    #we assume that any that aren't currently ranked aren't significant and new editions won't count
    #remove mismatch TODO make this faster
    match = (peaks[idx,0] == m[:,c_id]) * (peaks[idx,10] == m[:,c_yr])
    while(sum(match) < m.shape[0]):
        #print("\n", fn, "has ", m.shape[0] - sum(match), "extra\n")
        m = m[match,:]
        idx = np.searchsorted(peaks[:,0],m[:,c_id])
        match = peaks[idx,0] == m[:,c_id]

    #find those that were higher before
    fallers = m[:,c_gr] > peaks[idx,1]
    ndx = idx[fallers]
    if(ndx.size):
        peaks[ndx,1] = m[fallers,c_gr] #geek rating
        peaks[ndx,2] = d.toordinal() #date
        peaks[ndx,3] = m[fallers,c_rk] #rank
        peaks[ndx,4] = m[fallers,c_nv] #votes
        #track monopoly specifically
        #mon = np.where(m[fallers,c_id] == 1406)[0]
        #if(mon.size):
        #    print()
        #    print(peaks[ndx[mon[0]]], (m[fallers])[mon[0]], d.toordinal(), fn)
        #    print()
        #print("\n",peaks[ndx[-1]],"\n",fn, d.toordinal(), "\n", (m[fallers])[-1], "\n")
        test = peaks[ndx,0] != m[fallers,c_id]
        if(sum(test)):
            print("ERROR! mismatch",sum(test))
            print(ndx.size, fallers.size, test.size)
            print(np.where(test),peaks[ndx[test],0], (m[fallers,0])[test], fn)
            #print("\n",peaks[ndx,0], m[fallers,0])
            exit()

    #find those that were lower before
    #because we can't make sure this isn't before the peak, we just use the most recent as lowest
    #risers = m[:,c_gr] < peaks[idx,1]
    #ndx = idx[risers]
    #peaks[ndx,4] = m[risers,c_gr] #geek rating
    #peaks[ndx,5] = d.toordinal() #date
    #peaks[ndx,6] = m[risers,c_rk] #rank

print()
#calculate percent change in geek rating
peaks[:,8] = (peaks[:,5]-peaks[:,1])
#do the same with rank
peaks[:,9] = 100*(peaks[:,7]-peaks[:,3]) / peaks[:,3]
#sort by fall
sordid = peaks[peaks[:,8].argsort(),:]
#find ones that fell rather than climbed
fallers = sordid[:,2] < sordid[:,6]
#grab the last data set again
fn = latest.strftime("%Y-%m-%d.csv")
m = pd.read_csv("bgg-ranking-historicals/"+fn).to_numpy()

top = 50
for n in range(top):
    fell = (sordid[fallers])[top-n-1]
    w = np.where(m[:,c_id] == fell[0])[0]
    sts = m[w][0]
    print()
    print()
    print(sts[c_id])
    print(top-n)
    print(sts[c_nm], " (", sts[c_yr], ")", sep="")
    print("peak: %.3f" % fell[1], " (rank ", int(fell[3]), ", ", int(fell[4]), " votes) ", datetime.date.fromordinal((fell[2])).strftime("%d-%b-%y"), sep="" )
    #print("min: ", fell[4], datetime.date.fromordinal(int(fell[5])).strftime("%d-%b-%y"), "(rank ", fell[6], ")") 
    print("current: %.3f" % fell[5]," (rank ", int(fell[7]), ", ", int(sts[c_nv]), " votes)", sep="")
    #print("change:  %.4f" % (fell[5]-fell[1]),", %.4f" % fell[8], "%% (%.3f" % fell[9], "% rank)",sep="")
    print("change:  %.4f" % (fell[8]),", %.3f" % (100.0*fell[8]/fell[1]), "%% (%.3f" % fell[9], "% rank)",sep="")
print("done.")
