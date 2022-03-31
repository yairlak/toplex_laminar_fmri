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
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from mutagen.mp3 import MP3


authenticator = IAMAuthenticator('Y5tueZHZThXVM9io0v7SmRqebq36Dc1_BIohpSOQirki')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('https://api.eu-de.text-to-speech.watson.cloud.ibm.com/instances/1a3865b6-ef0f-4fa9-9632-bd91084106cc')

voices = ['fr-FR_NicolasV3Voice', 'fr-FR_ReneeV3Voice']

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
    for voice in voices:
        fn = f'../../stimuli/audio/{word}_{voice}_IBM.mp3'
        with open(fn,'wb') as audio_file:
            audio_file.write(text_to_speech.synthesize(word,
                                                       voice=voice,
                                                       accept='audio/mp3').get_result().content)
    
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
    
    for voice in voices:
        fn = f'../../stimuli/audio/{word}_IBM.mp3'
        with open(fn,'wb') as audio_file:
            audio_file.write(text_to_speech.synthesize(word,
                                                       voice=voice,
                                                       accept='audio/mp3').get_result().content)
    audio = MP3(fn)
    durations.append(audio.info.length)
    
df_low['audio duration'] = durations
df_low.to_csv('../../stimuli/low_freq.tsv', sep='\t')

print('LOW FREQ')
print(sorted(df_low['ortho'].values))
print(f'Low-freq: {np.mean(durations):1.2f} +- {np.std(durations):1.2f}')


