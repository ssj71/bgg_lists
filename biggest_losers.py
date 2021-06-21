#!/usr/bin/env python3
#spencer jackson

#games that have gone down in BGG rating the most in beefsack's historical data
import datetime
import numpy as np
import csv

latest = datetime.date(2021,6,18)
oldest = datetime.date(2016, 10, 12)

#start with the latest values (we expect it to have the complete list of games)
d = latest
fn = d.strftime("%Y-%m-%d.csv")
m = np.genfromtxt("bgg-ranking-historicals/"+fn, delimiter=',', skip_header=1, usecols=(0,2,3,4,5,6), comments='therearenocomments')
l = m.shape[0]
#peaks is gameid, gr peak, date, rank, gr min, date, rank,  rating drop (percent), rank drop (percent)
peaks = np.array([m[:,0].T, m[:,4].T, np.ones(l)*d.toordinal(), m[:,2], m[:,4].T, np.ones(l)*d.toordinal(), m[:,2], np.zeros(l), np.zeros(l)]).T
#sort by game id
#peaks.sort(axis=0)
peaks = peaks[peaks[:,0].argsort(),:]
for n in range((latest-oldest).days):
    d = (latest-datetime.timedelta(n))
    fn = d.strftime("%Y-%m-%d.csv")
    m = np.genfromtxt("bgg-ranking-historicals/"+fn, delimiter=',', skip_header=1, usecols=(0,2,3,4,5,6), comments='therearenocomments')
    #we skip the string name so the cols of m are:
    #game id, year, rank, avg, geek rating, no. ratings
    idx = np.searchsorted(peaks[:,0],m[:,0])

    #find those that were higher before
    fallers = m[:,4] > peaks[idx,1]
    (peaks[idx])[fallers,1] = m[fallers,4] #geek rating
    (peaks[idx])[fallers,2] = d.toordinal() #date
    (peaks[idx])[fallers,3] = m[fallers,2] #rank

    #find those that were lower before
    risers = m[:,4] < peaks[idx,1]
    (peaks[idx])[risers,4] = m[risers,4] #geek rating
    (peaks[idx])[risers,5] = d.toordinal() #date
    (peaks[idx])[risers,6] = m[risers,2] #rank

