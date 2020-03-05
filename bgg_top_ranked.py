#!/usr/bin/env python3

#this quickly became poorly named because now it's top 1000
import urllib.request
import re
import copy

page = urllib.request.urlopen("https://boardgamegeek.com/browse/boardgame")

def getNext100TRG(pagen):
    url = "https://boardgamegeek.com/browse/boardgame/page/"+str(pagen)
    page = urllib.request.urlopen(url)
    data = page.read().decode('utf-8')
    top = [int(m.group()) for m in re.finditer('(?<=href="/boardgame/)(\d+)(?=/)',data)]
    return top[0::3]

# grabs number of pages provided (100 entries per page)
def getTopRankedGames( pages = 1 ):
    top = []
    for p in range(1,1+pages):
        top.extend(getNext100TRG(p))
    return top
