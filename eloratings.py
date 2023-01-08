#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 22:11:03 2023

@author: kabir
"""


import ratingslib.ratings as rl
import pandas as pd
import numpy as np
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



# Get data
DATA_FOLDER = "/home/kabir/Desktop/nrl/"
filename = f"{DATA_FOLDER}formatted_match_results.csv"
data = pd.read_csv(filename)


# Columns
outcome = SoccerOutcome()

# prediction methods
pred_methods_list = ['MLE', 'RANK']
data_train, teams_df = parse_pairs_data(data,
                                        outcome=outcome)

R = lambda K, ks, HA: rl.Elo(version=ratings.ELOPOINT, K=K, ks=ks, HA=HA, starting_point=0)

K = 1
ks = 50
HA = 150





