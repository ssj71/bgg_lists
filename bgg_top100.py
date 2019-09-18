#!/usr/bin/env python3

import urllib.request
import re
import copy

page = urllib.request.urlopen("https://boardgamegeek.com/browse/boardgame")

#print(page.read())
data = page.read().decode('utf-8')
top = [int(m.group()) for m in re.finditer('(?<=href="/boardgame/)(\d+)(?=/)',data)]
top = top[0::3]
#topstring = [m.group() for m in re.finditer('(?:href="/boardgame/)(\d+)(?:/)',data)]
#for i in range(0,10):
#    print(top[i],topstring[3*i])

