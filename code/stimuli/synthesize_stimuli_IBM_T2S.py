#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 23:00:35 2022

@author: yl254115
"""


import pandas as pd
import numpy as np
from gtts import gTTS
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from mutagen.mp3 import MP3


# LOAD STIMULI
df = pd.read_csv('../../stimuli/stimuli.tsv', sep='\t')

# INIT SYNTHESIZER
authenticator = IAMAuthenticator('Y5tueZHZThXVM9io0v7SmRqebq36Dc1_BIohpSOQirki')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)
text_to_speech.set_service_url('https://api.eu-de.text-to-speech.watson.cloud.ibm.com/instances/1a3865b6-ef0f-4fa9-9632-bd91084106cc')
voices = ['fr-FR_NicolasV3Voice', 'fr-FR_ReneeV3Voice']

# INIT DURATION ARRAY
durations = {}
for voice in voices:
    durations[voice] = []

# SYNTHESIZE
for word in df['ortho']:
    for voice in voices:
        fn = f'../../stimuli/audio/{word}_{voice}_IBM.mp3'
        with open(fn,'wb') as audio_file:
            audio_file.write(text_to_speech.synthesize(word,
                                                       voice=voice,
                                                       accept='audio/mp3').get_result().content)    
        # EXTRACT FILE DURATION
        audio = MP3(fn)
        durations[voice].append(audio.info.length)
            
for voice in voices:
    df[f'audio duration_{voice}'] = durations[voice]

# WRITE TO FILE
df.to_csv('../../stimuli/stimuli_with_durations.tsv', sep='\t')
