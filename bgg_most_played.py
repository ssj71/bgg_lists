#!/usr/bin/env python3

#this snags the play data from bgg by date range
import urllib.request
import re
import copy
import datetime
import calendar
import numpy as np

#column ids
rank_col = 0 #rank in period for most unique plays
gameid_col = 1
plays_col = 2
uniqueplays_col = 3

defaultPages = 5 #number of pages to scrape (100 games per)

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


def getNext100TPG(starty, startm, rangem, pagen):
    start = datetime.date(starty,startm,1)
    stardate = start.strftime("%Y-%m-%d")
    endate = (add_months(start,rangem) - datetime.timedelta(1)).strftime("%Y-%m-%d")

    url = "https://boardgamegeek.com/plays/bygame/subtype/boardgame/start/" + stardate + "/end/" + endate + "/page/" + str(pagen) + "?sortby=distinctusers"
    page = urllib.request.urlopen(url)

    #print(url)
    #print(page.read())
    data = page.read().decode('utf-8')
    p = 0
    for i in range(3):
        p = data.find("<table ",p+1) #the data we want is in the 3rd table
    n = data.find("</table>",p)
    rawtable = data[p:n]
    #print(rawtable)

    items = [int(m.group()) for m in re.finditer('((?<=href="/boardgame/)|(?<=href="/boardgameexpansion/))\d+(?=/)',rawtable)]
    #TODO: I can't quite get this regex to pick up all the special characters in the titles, I can use the xml api at some point do get the title
    #titles = [m.group() for m in re.finditer('(?<="   >)([\u00BF-\u1FFF\u2C00-\uD7FF\w:\-\s]+)(?=</a>)',data)]
    plays = [int(m.group()) for m in re.finditer('(?<=<td>\n)(\s+\d+\s+)(?=</td>)',rawtable)]
    players = [int(m.group()) for m in re.finditer('(?<=">)(\d+\s+)(?=</td>)',rawtable)]
    #print(len(items),len(plays),len(players))
    
    return (items, plays, players)

def getTopPlayedGames( startyear = 2019, startmonth = 1, timerangemonths = 12, pages = 1 ):
    games = np.array([[],[],[],[]]).T #rank, game, plays, players
    for i in range(pages):
        (g, p, pr) = getNext100TPG(startyear, startmonth, timerangemonths, i+1)
        if len(g) != len(p) or len(g) != len(pr):
            print("error scraping page", i, "for", startmonth, startyear, len(g),len(p),len(pr))
        tmp = np.array([np.r_[:100]+i*100,g,p,pr])
        games = np.vstack((games,tmp.T))
    return games


def getTopPlayedGamesTill( year = 2019, month = 12, window = 1, pages = 1 ):
    if(window > month):
        year -= 1;
        month = 14 - window + month
    else:
        start = month - window + 1
    a = getTopPlayedGames( startyear = year, startmonth = start, timerangemonths = window , pages = pages )
    return a

#grab a year of data with sliding window of configurable number of months
#windows reach backward in time (so Jan with three month is Nov+ Dec+ Jan)
def loadyear(year = 19, window = 1):
    title = "t"+str(window)+"m"+str(year)
    try:
       data = np.load( title+".npy" )
    except IOError:
        print("could't find "+str(year)+" "+str(window)+ " data")
        first = True
        for m in range(1,13): #sliding window
            print(m)
            a = getTopPlayedGamesTill( year = 2000+year, month = m, timerangemonths = window , pages = defaultPages )
            if first:
                data = np.array([a,])
                first = False
            else:
                data = np.append(data,np.array([a]),axis=0)
        #don't save if the year isn't over
        if year != datetime.datetime.now().year-2000:
            np.save(title,data)
    return data

#the following functions help manipulate the data for analysis

#takes a 3d matrix from load_year and
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
            gameid = game[gameid_col]
            rank = game[rank_col]
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

#takes a matrix from ranktrends and
#returns a pruned matrix with game trends that reached rank N or higher
def topNtrends(trends, n):
    a = trends[np.any(trends < n, axis=1),:]
    print("top", n, a.shape)
    return trends[np.any(trends < n, axis=1), :]
