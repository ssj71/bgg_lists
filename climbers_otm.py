#!/usr/bin/env python3
#spencer jackson

#get top 15 climbers of the month based on beefsack's ranking historical data
import datetime
import numpy as np
import csv
import bgg_get_game_stats as bggstats
import pandas as pd

monthsback = 0
#I considered making this a sliding 12 mo thing. While that definitely highlights solid games, a shorter timespan makes the more dynamic list and highlights some slightly less known games each month. 1 month was a bit squirrelly, so I settled on 3 months.
d = datetime.date.today()
latest = datetime.date(d.year, d.month,1)
for i in range(monthsback):
    d = latest - datetime.timedelta(1) #step back 1 day to get to the prev month
    latest = datetime.date(d.year, d.month,1)
#d = latest - datetime.timedelta(1) #step back 1 day to get to the prev month
#d = latest - datetime.timedelta(365) #step back 365 days to get to the prev year
d = latest - datetime.timedelta(80) #step back 80 days to get 3 months
oldest = datetime.date(d.year, d.month,1)


def getHistorical(date):
    fn = date.strftime("%Y-%m-%d.csv")
    m = pd.read_csv("bgg-ranking-historicals/"+fn).to_numpy()
    return m

#columns of csv
c_id = 0  #id
c_nm = 1  #name
c_yr = 2  #year published
c_rk = 3  #rank
c_av = 4  #average rating
c_gr = 5  #geek rating (bayesian)
c_nv = 6  #number voters

#start with the latest values (we expect it to have the complete list of games)
m = getHistorical(latest)
l = m.shape[0]
d = latest
#peaks is 0gameid, 1gr peak, 2date, 3rank, 4votes, 5gr min, 6date, 7rank, 8votes, 9rating drop (percent), 10rank drop (percent), 11published year
peaks = np.array([m[:,c_id].T, m[:,c_gr].T, np.ones(l)*d.toordinal(), m[:,c_rk].T, m[:,c_nv].T, m[:,c_gr].T, np.ones(l)*d.toordinal(), m[:,c_rk].T, m[:,c_nv].T, np.zeros(l), np.zeros(l), m[:,c_yr].T]).T

#sort by game id
peaks = peaks[peaks[:,0].argsort(),:]
tot = (latest-oldest).days
for n in range(tot):
    #get the next historical data set
    d = latest-datetime.timedelta(n)
    m = getHistorical(d)
    print("\r %.4f%%" %((100*n/tot)),end="")
    #find where the games are in the first set
    idx = np.searchsorted(peaks[:,0],m[:,c_id])
    #we assume that any that aren't currently ranked aren't significant and new editions won't count
    #remove mismatch
    match = (peaks[idx,0] == m[:,c_id]) * (peaks[idx,11] == m[:,c_yr])
    while(sum(match) < m.shape[0]):
        m = m[match,:]
        idx = np.searchsorted(peaks[:,0],m[:,c_id])
        match = peaks[idx,0] == m[:,c_id]

    #find those that have a new higest rank on this date
    fallers = m[:,c_rk] < peaks[idx,3]
    ndx = idx[fallers]
    if(ndx.size):
        peaks[ndx,1] = m[fallers,c_gr] #geek rating
        peaks[ndx,2] = d.toordinal() #date
        peaks[ndx,3] = m[fallers,c_rk] #rank
        peaks[ndx,4] = m[fallers,c_nv] #votes
        test = peaks[ndx,0] != m[fallers,c_id]
        if(sum(test)):
            print("ERROR! fallers mismatch",sum(test))
            print(ndx.size, fallers.size, test.size)
            print(np.where(test),peaks[ndx[test],0], (m[fallers,0])[test], fn)
            exit()

#peaks is 0gameid, 1gr peak, 2date, 3rank, 4votes, 5gr min, 6date, 7rank, 8votes, 9rating drop (percent), 10rank drop (percent), 11published year
    #find those that have a new lowest rank on this date
    risers = m[:,c_rk] > peaks[idx,7]
    ndx = idx[risers]
    if(ndx.size):
        peaks[ndx,5] = m[risers,c_gr] #geek rating
        peaks[ndx,6] = d.toordinal() #date
        peaks[ndx,7] = m[risers,c_rk] #rank
        peaks[ndx,8] = m[risers,c_nv] #votes
        test = peaks[ndx,0] != m[risers,c_id]
        if(sum(test)):
            print("ERROR! risers mismatch",sum(test))
            print(ndx.size, fallers.size, test.size)
            print(np.where(test),peaks[ndx[test],0], (m[fallers,0])[test], fn)
            exit()

print()


#only look at overall risers
risers = peaks[peaks[:,2] > peaks[:,6]]
#remove any that have fewer than 100 votes
risers = risers[risers[:,4]>=100]

#calculate percent change in geek rating
risers[:,9] = (risers[:,1]-risers[:,5])/risers[:,1]
#do the same with rank
risers[:,10] = 100*(risers[:,7]-risers[:,3]) / risers[:,7]
#sort by rise
sordid = risers[risers[:,10].argsort(),:]
#grab the last data set again for titles etc
m = getHistorical(latest)


top = 30
for n in range(top):
    ris = sordid[-n-1,:]
    w = np.where(m[:,c_id] == ris[0])[0]
    sts = m[w][0]
    print()
    print()
#peaks is 0gameid, 1gr peak, 2date, 3rank, 4votes, 5gr min, 6date, 7rank, 8votes, 9rating drop (percent), 10rank drop (percent), 11published year
    print(sts[c_id])
    print(n+1)
    print(sts[c_nm], " (", sts[c_yr], ")", sep="")
    print("peak: ", int(ris[3]), " (%.3f" % ris[1], ", ", int(ris[4]), " votes) ", datetime.date.fromordinal(int(ris[2])).strftime("%d-%b-%y"), sep="" )
    print("lowest: ", int(ris[7]), " ( %.3f" % ris[5], ", ", int(ris[8]), " votes) ", datetime.date.fromordinal(int(ris[6])).strftime("%d-%b-%y"), sep="" )
    print("change: ", int(ris[7]-ris[3]), " %.3f" % ris[10], "%% (%.4f" % (ris[1]-ris[5]),", %.3f" % (100.0*ris[9]), "%, +", int(ris[4]-ris[8]),")" ,sep="")
print("done.")
