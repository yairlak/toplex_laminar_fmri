#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 23:00:35 2022

@author: yl254115
"""


import pandas as pd
import numpy as np

np.random.seed(1)

# LOAD LEXIQUE
fn = '../../data/lexique/Lexique383.tsv'
df = pd.read_csv(fn, delimiter='\t')

# CONDITIONS
conditions = ['nbmorph == 1',
              'nblettres == 6',
              "cgram in ['NOM', 'ADJ', 'VER']",
              "nombre == 's'"]

n_freq_low, n_freq_high = 90, 90

# LOG-FREQ PERCENTILE (LOW/HIGH)
df = df.loc[df['freqlivres'] > 3] # keep a ~10K-size vocabulary with top freqlivres
df['log_freqlivres'] = np.log(df['freqlivres'])
log_freqlivres_perc_90 = np.percentile(df['log_freqlivres'], 80)
log_freqlivres_perc_10 = np.percentile(df['log_freqlivres'], 20)

query = ' & '.join(conditions) + f' & (log_freqlivres > {log_freqlivres_perc_90})' 
df_high = df.query(query)
df_high = df_high.sample(n=n_freq_high)

query = ' & '.join(conditions) + f' & (log_freqlivres < {log_freqlivres_perc_10})' 
df_low = df.query(query)
df_low = df_low.sample(n=n_freq_low)

# MERGE DFs and WRITE TO FILE
df = pd.concat([df_low, df_high])
df.to_csv('../../stimuli/stimuli.tsv', sep='\t')
