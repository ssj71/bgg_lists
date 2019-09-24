#!/usr/bin/env python3

#this quickly became poorly named because now it's top 1000
import urllib.request
import re
import copy

page = urllib.request.urlopen("https://boardgamegeek.com/browse/boardgame")

#print(page.read())
#data = page.read().decode('utf-8')
#top = [int(m.group()) for m in re.finditer('(?<=href="/boardgame/)(\d+)(?=/)',data)]
#top100 = top[0::3]
#topstring = [m.group() for m in re.finditer('(?:href="/boardgame/)(\d+)(?:/)',data)]
#for i in range(0,10):
#    print(top[i],topstring[3*i])

top2500 = []

for p in range(1,26):
    url = "https://boardgamegeek.com/browse/boardgame/page/"+str(p)
    page = urllib.request.urlopen(url)
    data = page.read().decode('utf-8')
    top = [int(m.group()) for m in re.finditer('(?<=href="/boardgame/)(\d+)(?=/)',data)]
    top2500.extend(top[0::3])

top100 = top2500[0:100]
top1000 = top2500[0:1000]
