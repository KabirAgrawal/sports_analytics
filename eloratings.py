#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 22:11:03 2023

@author: kabir
"""


import ratingslib.ratings as rl
import pandas as pd
import datetime
from ratingslib.app_sports.methods import (Predictions, predict_hindsight,
                                           prepare_sport_dataset,
                                           show_list_of_accuracy_results)
from ratingslib.application import SoccerOutcome
from ratingslib.datasets.parameters import (COLUMNS_DICT, DATE_COL, WEEK_PERIOD,
                                            stats)
from ratingslib.datasets.parse import parse_pairs_data
from ratingslib.ratings.methods import rating_systems_to_dict
from ratingslib.utils.enums import ratings
from ratingslib.utils.methods import print_info


DATA_FOLDER = "/home/kabir/Desktop/nrl/"

NRL = pd.read_excel(f"{DATA_FOLDER}nrl.xlsx")
NRL = NRL.iloc[:,:8]

NRL['Home Team'] = NRL['Home Team'].apply(lambda x: x.split(' ')[-1])
NRL['Away Team'] = NRL['Away Team'].apply(lambda x: x.split(' ')[-1])
teams = pd.DataFrame(list(NRL['Home Team'].unique()))
teams.columns = ['Item']

# training data
nrl_train = NRL[NRL.Date <= datetime.datetime(2013, 1, 1)].sort_values(by='Date')
nrl_train.columns = ['date', 'time', 'home', 'away', 'venue', 'hs', 'as', 'playoff']


data = nrl_train[['home', 'away', 'hs', 'as']]
data.columns = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']

filename = f"{DATA_FOLDER}pre_2013.csv"
data.to_csv(filename)

# Columns
outcome = SoccerOutcome()
# prediction methods
pred_methods_list = ['MLE', 'RANK']
data_train, teams_df = parse_pairs_data(data,
                                        outcome=outcome)




# rating systems

ratings_list = [
    rl.Winloss(normalization=False),
    rl.Colley(),
    rl.Massey(data_limit=10),
    rl.Elo(version=ratings.ELOWIN, K=40, ks=400, HA=0,
           starting_point=0),
    rl.Elo(version=ratings.ELOPOINT, K=40, ks=400, HA=0,
           starting_point=0),
    rl.Keener(normalization=False),
    rl.OffenseDefense(tol=0.0001),
    rl.Markov(b=0.85, stats_markov_dict=stats.STATS_MARKOV_EQUAL_DICT),
    rl.AccuRate()
]

# convert list to dictionary
ratings_dict = rating_systems_to_dict(ratings_list)


print_info("HINDSIGHT RESULTS")

for pm in pred_methods_list:
    pred_list = []
    test_Y_list = []
    for rs in ratings_list:
        pred, test_y = predict_hindsight(data_train, rs.rate_from_file(filename), outcome, pm)
        test_Y_list.append(test_y)
        pred_list.append(pred)
    print_info(pm)
    show_list_of_accuracy_results(
        list(ratings_dict.keys()), test_Y_list, pred_list, print_predictions=True)