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

    page = urllib.request.urlopen("https://boardgamegeek.com/plays/bygame/subtype/boardgame/start/" + stardate + "/end/" + endate + "/page/" + str(pagen) + "?sortby=distinctusers")

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
