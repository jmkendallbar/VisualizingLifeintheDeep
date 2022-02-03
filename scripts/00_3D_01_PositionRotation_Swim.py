import csv
import pymel.core as pm #Importing pymel (see documentation here: 
# https://help.autodesk.com/cloudhelp/2015/ENU/Maya-Tech-Docs/PyMel/index.html
import maya.cmds as cmds #Importing maya commands

pm.window(title='PositionRotation_Swim Demo',width=300)
pm.columnLayout(adjustableColumn=True)
pm.showWindow()

#Defining variables which will be used as column indices

SECONDS = 0
ECG = 1
PITCH_DEG = 2
ROLL_DEG = 3
HEAD_DEG = 4
GYRZ = 5
GLIDE = 6
DEPTH = 7
HR = 8
STROKE_RATE = 9
EVENTS = 10
HEART = 11
STROKE = 12
 
#Defining two variables which will be used as indices where animation starts and ends 
START = 0  #start time in sec
END = 3084   #end time in sec

fs = 10 # Higher-res sample frequency (in Hz or "samples per second")
fps = 24

#Reading in .csv file (update to reflect your own path)
with open('G:/My Drive/Visualization/Data/02_HypoactiveHeidi_SleepDive.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data) # skips first row of the CSV file (with header)
    #For loop runs through all rows in data .csv file
    for i, row in enumerate(data):
        
        if i % 1 == 0:
            
            #print('Processing row %s' % (i)) #Print progress in with data row counter in console to keep track of if/where code gets stuck
            
            #If the row number is between the start and end indices of where we want to animate, run this code.        
            if i >= START*fs and i < END*fs: 
            
            #We will use the function float() to return floating point numbers (with decimals) for data values
                secs = float(i) / fs - START #Translate .csv data time into animation time
                time = secs * fps #Get from frames to seconds
             
                depth_value = -float(row[DEPTH])
                head_value = float(row[HEAD_DEG])+180
             
                #Define which object will be transformed according to data (use name as described in "Outliner")
                object = pm.ls('ESEAL_PLACER')[0] 
             
                #..setKey function sets a keyframe of the given value at the given time.
                object.rotateY.setKey(value=head_value, time=time) # rotate ESEAL_PLACER according to heading
                object.translateY.setKey(value=2*depth_value, time=time) # Moving vertically according to depth
             
                pitch_value = -float(row[PITCH_DEG]) 
                roll_value  = -float(row[ROLL_DEG])
                
                object = pm.ls('ESEAL_PIVOT')[0]
                
                object.rotateZ.setKey(value=pitch_value, time=time)
                object.rotateX.setKey(value=roll_value, time=time)
                
                object = pm.ls('SWIM_CONTROL')[0]
                
                glide = float(row[GLIDE])
                object.glide.setKey(value=glide, time=time)
                
                swim_stroke = int(row[STROKE])
                if swim_stroke:
                    object.swim.setKey(value=0, time=time)
                    object.swim.setKey(value=1, time=time - .001)
                    pm.keyTangent(object.swim, inTangentType='linear', outTangentType='linear', time=(time - .001, time))
                
                print('setting swim = %s, glide = %s, y= %s units, pitch= %s, roll = %s for time= %s sec' % (swim_stroke, glide, depth_value , pitch_value , roll_value , secs))
#     0            1            2       3          4          5           6       7      8         9           10                   11             12       13    14     15        16  17  18  19    20      21      22                  
# Sleep.Code	Sleep.Num	Seconds	  R.Time	Resp.Code	Resp.Num	Date	Time	Hour	Seal.ID	Simple.Sleep.Code	Simple.Sleep.Num	timebins	DN	pitch	roll	heading	x	y	z	Depth	speed	ODBA

low_fs = 5 #Lower resolution sampling frequency
            
XPOS = 17 # Lat displacement in m
YPOS = 18 # Long displacement in m
ZPOS = 19 # Depth

#Reading in .csv file (update to reflect your own path)
with open('Z:/Dissertation Sleep/Sleep_Analysis/Data/test33_HypoactiveHeidi_08_animation_track_5Hz_JKB.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data) # skips first row of the CSV file (with header)
    #For loop runs through all rows in data .csv file
    for j, row in enumerate(data):
        
        if j % 1 == 0:
            
            #If the row number is between the start and end indices of where we want to animate, run this code.        
            if j >= START*low_fs and j < END*low_fs: 
            
            #We will use the function float() to return floating point numbers (with decimals) for data values
                secs2 = float(j) / low_fs - START #Translate .csv data time into animation time
                time = secs2 * fps #Get from frames to seconds
             
                XPOS_value = -float(row[XPOS])
                YPOS_value = float(row[YPOS])
             
                #Define which object will be transformed according to data (use name as described in "Outliner")
                object = pm.ls('ESEAL_PLACER')[0] 
             
                #..setKey function sets a keyframe of the given value at the given time.
                object.translateX.setKey(value=XPOS_value, time=time) # Moving forward at 1m/s
                object.translateZ.setKey(value=YPOS_value, time=time) # Moving vertically according to depth
                
                print('setting translateX = %s, translateZ = %s for time= %s sec' % (XPOS_value, YPOS_value, secs2))
