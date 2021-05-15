#%%
# USING PSYCHOPY
import pyaudio
import wave
import sys
import os
import wavio
import time
from datetime import datetime
from psychopy import prefs
import pandas as pd
import numpy as np
import psychtoolbox as ptb

data_path = "G:\Shared drives\Elephant Seal Animation for Gitte\ESeal_Animation\data"
output_path = "G:\Shared drives\Elephant Seal Animation for Gitte\ESeal_Animation"

os.chdir(data_path)
os.getcwd()

test = pd.read_csv('HR_data_for_Python.csv', sep=",", header=1, squeeze=True)
wait = pd.read_csv('HR_wait_for_Python.csv', sep=",", header=0, squeeze=True)


# From this website https://mbraintrain.com/how-to-set-up-precise-sound-stimulation-with-psychopy-and-pylsl/
from psychopy import prefs
#change the pref libraty to PTB and set the latency mode to high precision
prefs.hardware['audioLib'] = 'PTB'
prefs.hardware['audioLatencyMode'] = 3

#import other necessary libraries
from psychopy import core, event, sound

seconds=pd.read_csv('HR_subset_for_Reaper.csv', sep=',',header=None, squeeze=True)
badum = sound.Sound('single_heartbeat.wav')

for i in range(0,len(wait)):
    playback_time = core.getTime()
    curr_time = core.getTime() - playback_time # get elapsed time
    while curr_time < wait[i]:
        curr_time = core.getTime() - playback_time # get elapsed time
        print("DEBUG: Initial wait %3.5f" %curr_time)
        core.wait(0.05) #wait 50 milliseconds
    # if test[i] == 1:   
    badum.play()
    core.wait(0.45) #Determined by shortest interbeat interval
    #print("First Badum at %f" %(datetime.now()))
    i += 1