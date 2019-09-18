#!/usr/bin/env python3

import urllib.request
import re

page = urllib.request.urlopen("https://boardgamegeek.com/browse/boardgame")

top = [int(m.group()) for m in re.finditer('(?<=href="/boardgame/)(\d+)(?=/)',page.read().decode('utf-8'))]

print(top)
