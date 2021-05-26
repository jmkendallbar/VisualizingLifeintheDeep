"""
LINKING HEART RATE DATA TO SOUND
Created on Tue May 18 10:35:14 2021

@author: Jessica Kendall-Bar
"""
#%%
# import libraries
import os
import pandas as pd
from psychopy import prefs, core, sound

# UPDATE ME
data_path = "C:/Users/jmkb9/Documents/GitHub/VisualizingFear/data"

os.chdir(data_path)
os.getcwd()

# From this website https://mbraintrain.com/how-to-set-up-precise-sound-stimulation-with-psychopy-and-pylsl/
# Change the pref libraty to PTB (psychtoolbox) 
prefs.hardware['audioLib'] = 'PTB'
# Set the latency mode to high precision (3)
prefs.hardware['audioLatencyMode'] = 3

# Load in heartbeat sound
badum = sound.Sound('single_heartbeat.wav') #sound of heart beating
# swish = sound.Sound('01 Tail Noise.wav') #sound of tail swishing back and forth

# Load in heartrate data (with array of interbeat intervals in seconds)
HR_data = pd.read_csv('narwhal_HR.csv', sep=",", header=0, squeeze=True)

# After heartbeat plays, wait interval - duration of heartbeat until next.
HR_data['Wait'] = HR_data['Interval'] - 0.45

# Initializing wait variable with wait durations
wait = HR_data['Wait']
# Fill in first wait time with time until first value (no corresponding interbeat interval)
wait[0] = HR_data.iloc[0]['Seconds']

for i in range(0,len(wait)): # for all values in wait series
    playback_time = core.getTime() # get current time
    curr_time = core.getTime() - playback_time # get elapsed time
    while curr_time < wait[i]: # until it's time to play next heart beat
        curr_time = core.getTime() - playback_time # continue getting elapsed time
        print("Seconds since last heartbeat: %3.5f" %curr_time)
        core.wait(0.05) # wait 50 milliseconds
    badum.play() # play next heartbeat
    core.wait(0.45) # determined by duration of heartbeat
    i += 1 # around and around we go!