# -*- coding: utf-8 -*-
"""
LINKING HEART RATE DATA TO SOUND
Created on Tue May 18 10:35:14 2021

@author: Jessica Kendall-Bar
"""
#%%
# USING PSYCHOPY
import os
import pandas as pd
from psychopy import prefs, core, sound

data_path = "C:/Users/jmkb9/Documents/GitHub/VisualizingFear/data"
output_path = "C:/Users/jmkb9/Documents/GitHub/VisualizingFear/data"

os.chdir(data_path)
os.getcwd()

# From this website https://mbraintrain.com/how-to-set-up-precise-sound-stimulation-with-psychopy-and-pylsl/
#change the pref libraty to PTB and set the latency mode to high precision (3)
prefs.hardware['audioLib'] = 'PTB'
prefs.hardware['audioLatencyMode'] = 3

#import other necessary libraries

badum = sound.Sound('single_heartbeat.wav')
HR_data = pd.read_csv('narwhal_HR.csv', sep=",", header=0, squeeze=True)
HR_data['Wait'] = HR_data['Interval'] - 0.30
HR_data.iloc[0]['Wait'] = HR_data.iloc[0]['Seconds']
wait = pd.read_csv('HR_wait_for_Python.csv', sep=",", header=0, squeeze=True)

for i in range(0,len(wait)):
    playback_time = core.getTime()
    curr_time = core.getTime() - playback_time # get elapsed time
    while curr_time < wait[i]:
        curr_time = core.getTime() - playback_time # get elapsed time
        print("Seconds since last heartbeat: %3.5f" %curr_time)
        core.wait(0.05) #wait 50 milliseconds  
    badum.play()
    core.wait(0.45) #Determined by shortest interbeat interval (duration of heartbeat)
    i += 1