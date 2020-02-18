#!/usr/bin/env python3

#this snags the play data from bgg by date range
import urllib.request
import re
import copy
import datetime
import calendar
import numpy as np

starty = 2019
startm = 12

rangem = 12 #months
pagen = 1

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

start = datetime.date(starty,startm,1)
stardate = start.strftime("%Y-%m-%d")
endate = (add_months(start,rangem) - datetime.timedelta(1)).strftime("%Y-%m-%d")

#
page = urllib.request.urlopen("https://boardgamegeek.com/plays/bygame/subtype/boardgame/start/" + stardate + "/end/" + endate + "/page/" + str(pagen) + "?sortby=distinctusers")

#print(page.read())
data = page.read().decode('utf-8')
p = 0
for i in range(3):
    p = data.find("<table ",p+1) #the data we want is in the 3rd table
n = data.find("</table>",p)
rawtable = data[p:n]
#print(rawtable)

items = [int(m.group()) for m in re.finditer('(?<=href="/boardgame/)(\d+)(?=/)',rawtable)]
#TODO: I can't quite get this regex to pick up all the special characters in the titles, I can use the xml api at some point
#titles = [m.group() for m in re.finditer('(?<="   >)([\u00BF-\u1FFF\u2C00-\uD7FF\w:\-\s]+)(?=</a>)',data)]
plays = [int(m.group()) for m in re.finditer('(?<=<td>\n)(\s+\d+\s+)(?=</td>)',rawtable)]
players = [int(m.group()) for m in re.finditer('(?<=">)(\d+\s+)(?=</td>)',rawtable)]
print(len(items),len(plays),len(players))
exit()
#top100 = top[0::3]
#topstring = [m.group() for m in re.finditer('(?:href="/boardgame/)(\d+)(?:/)',data)]
#for i in range(0,10):
#    print(top[i],topstring[3*i])

top1000 = top100

for p in range(2,11):
    url = "https://boardgamegeek.com/browse/boardgame/page/"+str(p)
    page = urllib.request.urlopen(url)
    data = page.read().decode('utf-8')
    top = [int(m.group()) for m in re.finditer('(?<=href="/boardgame/)(\d+)(?=/)',data)]
    top1000.extend(top[0::3])
