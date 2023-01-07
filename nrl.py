#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 09:44:54 2023

@author: kabir
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_rows(df, rows=0, position = None, rounds = None):
    
    if position != None:
        df = df[df.position == position]
        
    if rounds != None:
        df = df[df['round'].isin(rounds)]
    
    baseline_data = pd.DataFrame()
    for y in list(df.year.unique()):
        try:
            tdf = df[df.year == y]
            if rows != 'all':
                baseline_data = pd.concat([baseline_data, tdf.iloc[rows,:].T], axis=1)
            else:
                baseline_data = pd.concat([baseline_data, tdf.iloc[:,:].T], axis=1)
        except:
            pass
        
        
    baseline_data = baseline_data.T
    baseline_data.index = np.arange(baseline_data.shape[0])
    return baseline_data

def filter_data(data, query, min_matches, max_gap):
    X = data.query(query)    
    df = pd.DataFrame()

    # Employ filters
    for p in list(X.playerId.unique()):
        S = X[X.playerId == p]
                
        games = S.shape[0]
        
        if games > 1:
            max_diff = np.amax(np.asarray(S['round'].diff().dropna()))
        else:
            max_diff = 30
        
        
        if games >= min_matches and max_diff <= max_gap:
            df = pd.concat([df, S])
    return df


def surface(data, query, xlabel, ylabel, min_matches = 10, max_gap = 3, show=True):
    df = filter_data(data, query, min_matches, max_gap)
    
    df = df[['fullname', 'playerId', xlabel, ylabel]]
    
    df[xlabel] = df[xlabel].astype("int")

    x = df[xlabel]
    z = df[ylabel]
    
    ymap = {}
    P = list(df.playerId.unique())
    y = np.linspace(0, 20, len(P))
    
    for i, p in enumerate(P):
        ymap[p] = y[i]
    
    
    
    df['ycoord'] = df['playerId'].apply(lambda p: ymap[p])
    y = df['ycoord']
    
    fig = plt.figure(figsize=(15, 15)) 
    ax = plt.axes(projection='3d')
    ax.scatter3D(x, y, z, c=y, cmap='Greens')
    
    # Show the graph
    if show == True:
        plt.show()
    else:
        plt.close()