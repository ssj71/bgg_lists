#!/usr/bin/env python3
#spencer jackson

#get a csv from the historicals and return it as a numpy array (note types are all strings!)

import numpy as np
from datetime import date
import csv
import pandas as pd

#columns of csv
gameid_col = 0  #id
name_col = 1  #name
year_col = 2  #year published
rank_col = 3  #rank
rating_col = 4  #average rating
geekrating_col = 5  #geek rating (bayesian)
voters_col = 6  #number voters

def get_date(y, m, d):
    return pd.read_csv("bgg-ranking-historicals/"+date(y, m, d).strftime("%Y-%m-%d.csv")).to_numpy()
