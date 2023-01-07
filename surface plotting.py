#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 19:27:36 2023

@author: kabir
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nrl import *


DATA_FOLDER = "/home/kabir/Desktop/nrl/"

# Load data
player_stats = pd.read_csv(f"{DATA_FOLDER}match_player_stats.csv")
players = pd.read_csv(f"{DATA_FOLDER}players.csv")

player_stats = player_stats[['match_id', 'playerId', 'minutesPlayed', 'fantasyPointsTotal']]
players['fullname'] = players['firstName'] + ' ' + players['lastName']
players = players[['match_id', 'fullname', 'playerId', 'teamID', 'number', 'position']]

# join tables
data = pd.merge(player_stats, players, on=['match_id', 'playerId']).drop_duplicates()

data['year'] = data['match_id'].apply(lambda x: int(str(x)[:4]))
data['round'] = data['match_id'].apply(lambda x: int(str(x)[7:9]))

data = data[data['round'] <= 26]

# Analysis
query = 'year==2014 and position=="Fullback"'
xlabel='round'
ylabel = 'fantasyPointsTotal'
surface(data, query, xlabel, ylabel)
considered_df = filter_data(data, query, min_matches=10, max_gap=3)

    


    
    
    
    
    