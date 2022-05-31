#!/usr/bin/env python3

#spencer jackson

import time
import datetime
import csv

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def openFile(y,m,d)
    name =  datetime.date(y,m,d).strftime(%Y-%m-%d) + ".csv"
    path = "bgg-ranking-historicals/"
    f = open(name) as csvfile

    

def openFiles(starty, startm, rangem)
    start = datetime.date(starty,startm,1)
    stardate = start.strftime("%Y-%m-%d")
    endate = (add_months(start,rangem) - datetime.timedelta(1)).strftime("%Y-%m-%d")


