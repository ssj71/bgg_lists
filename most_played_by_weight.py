#!/usr/bin/env python3
#spencer jackson

#look at how the top played games fall into weight classes

import bgg_get_game_stats as bggstats
import bgg_most_played as bggmp
import numpy as np
import matplotlib.pyplot as matplot

ntop = 10

monthwindow = 12
year = 20
month = 4
unpub = 18291
top = bggmp.getTopPlayedGamesTill( year, month, monthwindow, 10) #top played
top = top[top[:,bggmp.gameid_col]!=unpub,:] #exclude unpublished prototype
idlist = top[:,bggmp.gameid_col]
stats = bggstats.getStatsSlowly(idlist)

#top and stats should be aligned so the id cols match
print(top.shape, stats.shape)

print(type(top[0, bggmp.gameid_col])) #int
print(type(stats[0, bggstats.gameid_col])) #str
for i in range(top.shape[0]):
    #if top[i, bggmp.gameid_col] != stats[i, bggstats.gameid_col]:
    a = int(top[i, bggmp.gameid_col])
    b = int(stats[i, bggstats.gameid_col])
#    if int(top[i, bggmp.gameid_col]) != stats[i, bggstats.gameid_col]:
    if a != b:
        print(i, a, b)
        print(i, int(top[i, bggmp.gameid_col]) , stats[i, bggstats.gameid_col])
        print("oh no! The fetched data doesn't match!")
        exit()


categories = ( 
    "Flyweight [1.0-1.5)",
    "Featherweight [1.5-2.0)",
    "Welterweight [2.0-2.5)",
    "Middleweight [2.5-3.0)",
    "Light-Heavyweight [3.0-3.5)",
    "Cruiserweight [3.5-4.0)",
    "Heavyweight [4.0-4.5)",
    "Super-Heavyweight [4.5-5.0]",
    )

def weight2categoryindex(weight):
    return int(2*(weight-1))

first = True
topN = -np.ones([len(categories),ntop])
idx = -1
for game in stats:
    idx += 1
    weight = float(game[bggstats.weight_col])
    category = weight2categoryindex(weight)
    if topN[category,0] != -1:
        #already found 10 in the category
        continue
    for i in range(ntop-1,-1,-1):
        if topN[category,i] == -1:
            topN[category,i] = idx
            break

cat = 0
for mat in topN:
    i = ntop
    print(categories[cat],"\n") 
    for rank in mat:
        idx = int(rank)
        print(stats[idx, bggstats.gameid_col], stats[idx, bggstats.name_col])
        print("#", i, " in ", categories[cat], sep="")
        print("weight:", stats[idx, bggstats.weight_col])
        print("#", str(idx+1), " most played overall", sep="")
        print("players:", int(top[idx, bggmp.uniqueplays_col]))
        print("\n")
        i -= 1
    cat += 1

print("\nSummary:")
#this summary is harder to read than the ranks
#cat = 0
#for mat in topN:
#    print( categories[cat], "Ratings: ", mat[0][bggstats.rating_col], "-", mat[ntop-1][bggstats.rating_col])
#    cat += 1
#print("")
cat = 0
for mat in topN:
    print( categories[cat].ljust(30,'.'), "Ranks: ", str(int(mat[ntop-1])+1), "-", str(int(mat[0])+1), sep="")
    cat += 1
print("\n")


#matplot.scatter( stats[:,bggstats.weight_col].astype(np.float), top[:,bggmp.uniqueplays_col])#top[:,bggmp.rank_col])
matplot.scatter( stats[:,bggstats.weight_col].astype(np.float), top[:,bggmp.rank_col])
matplot.ylabel('Rank (by Unique Users)')
matplot.xlabel('Weight')
matplot.figure()
matplot.hist(stats[:,bggstats.weight_col].astype(np.float), np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]))
matplot.ylabel('Number of Games in 10K Most Played')
matplot.xlabel('Weight')

matplot.show()
