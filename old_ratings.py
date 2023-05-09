#!/usr/bin/env python3
#spencer jackson

#look at top 100 ranked games and re-order them by average rating when excluding anything within 2 years of release!

#it would be nice if we could adjust the geek rating but that algorithm is secret.
# we might just scale the gr proportionally to how the average changed
import bgg_get_game_stats as bggstats
import bgg_top_ranked as bggtr
import numpy as np
import matplotlib.pyplot as matplot
import datetime
import dateutil.parser as dparse
import csv
import pandas as pd
import bgg_get_historicals as bgg_historicals
import math as m
import untangle
import time
import urllib.parse
import re

rgame_col = 0
ruser_col = 1
rating_col = 2
rdate_col = 3

ntop = 100
cutoff = 24 #months

allname = "top_100_all_raters_23_2"

try:
    allgames = np.load(allname+'.npy')
    stats = np.load(allname+"stats.npy").astype('U100')
    startat = np.count_nonzero(stats[:,bggstats.gameid_col])
    if startat == ntop:
        #TODO: if the last game gets messed up we won't get this right
        skip = True
    else:
        skip = False
except:
    allgames = np.zeros((0),'i4, U100, f4, i4') #when each game is done the resulting matrix will get appended to this array
    stats = np.zeros((ntop,14),dtype='U100')
    skip = False
    startat = 0

top = bgg_historicals.get_date(2023,2,24)[:ntop,bgg_historicals.gameid_col]

#instead use XML API 2

if not skip:
    #two steps
    print("getting all ratings for games")
    for g, gid in enumerate(top[startat:],startat):
        #first get all raters for a game
        url =  "https://boardgamegeek.com/xmlapi2/thing?id="+str(gid)+"&ratingcomments=1&stats=1"
        xml = untangle.parse(url)
        game = xml.items.item
        stats[g,:] = bggstats.getGameStats(xml)[0]

        nrat = int(game.comments['totalitems'])
        ratings = np.zeros(nrat+100,'i4, U100, f4, i4')
        pages = m.ceil(nrat/100) #pages 100 raters per page
        print("game", g, gid, stats[g,bggstats.name_col], nrat, flush=True)
        i = 0
        for user in game.comments.comment:
            ratings[i][rgame_col] = gid # or game['id']
            ratings[i][ruser_col] = user['username']
            ratings[i][rating_col] = float(user['rating'])
            #don't have the date yet
            i+=1

        #now repeat until there are no more pages with comments
        p = 2
        url =  "https://boardgamegeek.com/xmlapi2/thing?id=" + str(gid) + "&ratingcomments=1&page=" + str(p)
        xml = untangle.parse(url)
        game = xml.items.item
        while hasattr(game.comments,'comment'):
            print(p,end=',',flush=True)
            for user in game.comments.comment:
                #TODO: check that there wasn't an overlap from a new rating being insterted and getting repeated users
                ratings[i][rgame_col] = gid # or game['id']
                ratings[i][ruser_col] = user['username']
                ratings[i][rating_col] = float(user['rating'])
                #don't have the date yet
                i+=1
            time.sleep(2)
            p += 1
            url =  "https://boardgamegeek.com/xmlapi2/thing?id=" + str(gid) + "&ratingcomments=1&page=" + str(p)
            xml = untangle.parse(url)
            game = xml.items.item

        #because we don't know how many ratings all the games will have all together yet
        #we must stack. Since this will only be done 100x it's hopefully ok
        allgames = np.hstack((allgames,ratings[:i]))
        time.sleep(10)
        print()

        np.save(allname,allgames)
        np.save(allname+"stats",stats)
    exit()



#now we have a table of all voters, now we must get each user's collection data to see when they last updated their rating
# for example https://boardgamegeek.com/xmlapi2/collection?&id=174430,161936,291457,167791&stats=1&username=Terraformer
print("getting individual collections")
for rater in allgames:
    if not rater[rdate_col]:
        username = rater[ruser_col]
        idx = (allgames['f1']==username).nonzero()[0]
        usersgames = allgames[allgames['f1']==username]
        ids = usersgames['f0']
        url = "https://boardgamegeek.com/xmlapi2/collection?&id="+",".join(str(n) for n in ids) +"&username="+urllib.parse.quote(username)
        #these are just some debugging messages
        #print(rater)
        #print(username)
        #print(len(ids))
        #print(url)
        #print(len(ids))
        #print(usersgames)
        #exit()
        xml = untangle.parse(url)
        retry = 1
        done = False
        while not done:
            time.sleep(retry*3)
            xml = untangle.parse(url)
            if hasattr(xml,'errors'):
                print()
                print(idx[usersgames['f0'] == rater[rgame_col]][0], rater)
                print(xml.errors.error.message.cdata)
                print('https://boardgamegeek.com/collection/user/'+username+'?subtype=boardgame&ff=1')
                print()
                done = True
            elif retry == 2:
                np.save(allname,allgames)
                print('.',end='',flush=True)
            elif retry == 10:
                print("something wrong with", idx[usersgames['f0'] == rater[rgame_col]][0],'?')
                print(url)
                #exit()
            elif retry > 2:
                print('.',end='',flush=True)
            retry += 1
            if hasattr(xml,'items'):
                if hasattr(xml.items,'item'):
                    #get rating dates and store (as sec from epoch)
                    for game in xml.items.item:
                        #print(game.status['lastmodified'], end=', ')
                        d = int(dparse.parse(game.status['lastmodified']).timestamp())
                        i = idx[usersgames['f0'] == int(game['objectid'])]
                        for j in i:
                            allgames[j][rdate_col] = d
                    #double check the line we're currently on
                    i = idx[usersgames['f0'] == rater[rgame_col]][0]
                    print(i, end=',', flush=True)
                    #print()
                    if not allgames[i][rdate_col]:
                        #somehow we didn't get the date we're looking for
                        #could be they removed their rating OR they rated another version e.g. El Grande Big Box
                        print(" got issues")
                        print(url)
                        print(stats[stats[:,bggstats.gameid_col] == str(allgames[i][0]),bggstats.name_col])
                        print('https://boardgamegeek.com/collection/user/'+username+'?subtype=boardgame&ff=1')
                        #exit()
                    if not i%10:
                        np.save(allname,allgames)
                        time.sleep(10)
                    else:
                        time.sleep(1)
                    done = True
                else:
                    #user removed their only rating
                    print("\nuser removed rating: ", idx[usersgames['f0'] == rater[rgame_col]][0])
                    done = True
    #else we already got them from a different game
    #go to next user
print("all done!")

#make a scatter plot of the ratings by date after publication
if False:
    nplot = 10
    for line in stats[:nplot]:
        game = int(line[bggstats.gameid_col])
        today = datetime.datetime(2023,4,1).timestamp()
        year = datetime.datetime(int(line[bggstats.year_col]),1,1).timestamp()
        secsamonth = 60*60*24*365.25/12
        ratings = allgames[allgames['f0'] == game]
        rsrt = ratings[ratings['f3'].argsort()]
        start = rsrt[100]['f3'] #everything relative to the date of the 100th rating
        rsrt['f3'] = (rsrt['f3']-start)/secsamonth
        avgs = np.zeros(m.ceil(max(rsrt['f3'])))
        b4time = (rsrt['f3']<0).nonzero()[0]
        if len(b4time):
            eom = b4time[-1]
            avgs[0] = np.mean(rsrt[:eom]['f2'])
        else:
            avgs[0] = 5.5
        for mo in range(1,len(avgs)):
            neom = (rsrt['f3']<=mo).nonzero()[0][-1]
            if eom != neom:
                avgs[mo] = np.mean(rsrt[eom:neom]['f2'])
            else:
                avgs[mo] = avgs[mo-1]
            eom = neom

        #matplot.scatter(rsrt['f3'],rsrt['f2'])
        matplot.plot(avgs)

    matplot.legend(stats[:nplot,bggstats.name_col])
    matplot.ylabel('rating')
    matplot.xlabel('months')
    matplot.title('average rating per month after 100 ratings')
    matplot.show()

#store game ids, average, adjusted, votes, rm votes and new GR
gidcol = 0
avgcol = 1
adjcol = 2
votcol = 3
nvtcol = 4
ngrcol = 5
i = 0
store = np.zeros([len(stats),6])
for line in stats:
    game = int(line[bggstats.gameid_col])
    today = datetime.datetime(2023,4,20).timestamp()
    year = datetime.datetime(int(line[bggstats.year_col]),1,1).timestamp()
    secsamonth = 60*60*24*365.25/12
    ratings = allgames[allgames['f0'] == game]
    rsrt = ratings[ratings['f3'].argsort()]
    #convert everything to months relative to the date of the 100th rating
    start = rsrt[100]['f3']
    rsrt['f3'] = (rsrt['f3']-start)/secsamonth

    if max(rsrt['f3']) >= cutoff:
        avg = np.mean(rsrt['f2'])
        adjavg = np.mean(rsrt[rsrt['f3']>=cutoff]['f2'])

        store[i,gidcol] = game
        store[i,avgcol] = avg
        store[i,adjcol] = adjavg
        store[i,votcol] = len(rsrt)
        store[i,nvtcol] = np.count_nonzero(rsrt['f3']>=cutoff)
        store[i,ngrcol] = float(line[bggstats.geekrating_col])*adjavg/avg
        i += 1

#sort
stort = store[store[:,ngrcol].argsort()]
i = 1
print(stort.shape)
for stuff in stort[-1:-16:-1]: #stort[-52:-1:,:]:
    if stuff[0]:
        line = stats[stats[:,bggstats.gameid_col]==str(int(stuff[gidcol]))][0]
        print()
        print()
        print(line[bggstats.gameid_col])
        dif = int(line[bggstats.rank_col]) - i
        s = "(+"+str(dif)+")" if dif > 0 else "("+str(dif)+")"
        print(line[bggstats.name_col], " (", line[bggstats.year_col], ")", sep="")
        print("Adjusted Stats:")
        print("  Rank:",i,s)
        print("  GeekRating: %.3f" % stuff[ngrcol])
        print("  Avg. Rating: %.3f (%.3f%%)" % (stuff[adjcol], 100.0*(stuff[adjcol]/stuff[avgcol]-1.0)))
        print("  Votes: %i (%i)" % (stuff[nvtcol], stuff[nvtcol]-stuff[votcol]))
        print()
        print("Original Stats:")
        print("  Rank: %i" % int(line[bggstats.rank_col]))
        print("  GeekRating: %.3f" % float(line[bggstats.geekrating_col]))
        print("  Avg. Rating: %.3f" % stuff[avgcol])
        print("  Votes: %i" % stuff[votcol])
        i += 1


print("\nThose that didn't make it:")

for stuff in stort[:50]:
    if stuff[gidcol]:
        line = stats[stats[:,bggstats.gameid_col]==str(int(stuff[gidcol]))][0]
        #if int(line[bggstats.rank_col])<=50:
        print(line[bggstats.rank_col], line[bggstats.name_col], " (%s, %.3f)" % (line[bggstats.year_col], 100.0*(stuff[adjcol]/stuff[avgcol]-1.0)))
            #print("  Votes: %i (%i)" % (stuff[nvtcol], stuff[nvtcol]-stuff[votcol]))

print("\n too new")
for line in stats:
    if float(line[bggstats.gameid_col]) in stort[:,gidcol]:
        pass
    else:
        print(line[bggstats.rank_col],line[bggstats.name_col], line[bggstats.year_col])


print("done.")

