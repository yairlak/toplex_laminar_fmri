#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 23:00:35 2022

@author: yl254115
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gtts import gTTS
from mutagen.mp3 import MP3

# LOAD LEXIQUE
fn = '../../data/lexique/Lexique383.tsv'
df = pd.read_csv(fn, delimiter='\t')

# CONDITIONS
conditions = ['nbmorph == 1',
              'nblettres == 6',
              "cgram == 'NOM'",
              "nombre == 's'"]


# LOG-FREQ PERCENTILE (LOW/HIGH)
df = df.loc[df['freqlivres'] > 6] # keep a ~10K-size vocabulary with top freqlivres
df['log_freqlivres'] = np.log(df['freqlivres'])
log_freqlivres_perc_90 = np.percentile(df['log_freqlivres'], 90)
log_freqlivres_perc_10 = np.percentile(df['log_freqlivres'], 10)


# QUERY DF HIGH FREQ
df_high = df.loc[df['log_freqlivres']>log_freqlivres_perc_90]
df_high = df_high.query(' & '.join(conditions))

durations = []
for word in df_high['ortho']:
    tts = gTTS(word, lang='fr')
    fn = f'../../stimuli/audio/{word}.mp3'
    tts.save(fn)
    audio = MP3(fn)
    durations.append(audio.info.length)

df_high['audio duration'] = durations
df_high.to_csv('../../stimuli/high_freq.tsv', sep='\t')

print('HIGH FREQ')
print(sorted(df_high['ortho'].values))
print(f'High-freq: {np.mean(durations):1.2f} +- {np.std(durations):1.2f}')

# QUERY DF LOW FREQ
df_low = df.loc[df['log_freqlivres']<log_freqlivres_perc_10]
df_low = df_low.query(' & '.join(conditions))

durations = []
for word in df_low['ortho']:
    tts = gTTS(word, lang='fr')
    fn = f'../../stimuli/audio/{word}.mp3'
    tts.save(fn)
    audio = MP3(fn)
    durations.append(audio.info.length)
    
df_low['audio duration'] = durations
df_low.to_csv('../../stimuli/low_freq.tsv', sep='\t')

print('LOW FREQ')
print(sorted(df_low['ortho'].values))
print(f'Low-freq: {np.mean(durations):1.2f} +- {np.std(durations):1.2f}')


