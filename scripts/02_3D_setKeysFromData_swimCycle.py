import csv
import pymel.core as pm

#Defining variables which will be used as column indices

SECONDS = 0
DEPTH = 1
STROKE_RATE = 2
GLIDE = 3
PITCH_DEG = 4
ROLL_DEG = 5
STROKE = 6
 
#Defining two variables which will be used as indices where animation starts and ends 
START = 0  #start time in sec
END = 12240   #end time in sec

fs = 16 #Sample frequency (in Hz or "samples per second")

#Reading in .csv file (update to reflect your own path)
with open('~data/02_Example_StrokeRateData.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    #For loop runs through all rows in data .csv file
    for i, row in enumerate(data):
        
        if i % 1 == 0:
            
            #print('Processing row %s' % (i)) #Print progress in with data row counter in console to keep track of if/where code gets stuck
            
            #If the row number is between the start and end indices of where we want to animate, run this code.        
            if i >= START*fs and i < END*fs: 
            
            #We will use the function float() to return floating point numbers (with decimals) for data values
                time = float(i) / fs - START #Translate .csv data time into animation time
                time = time * fs #Get from frames to seconds
             
                depth_value = -float(row[DEPTH])
             
                #Define which object will be transformed according to data (use name as described in "Outliner")
                object = pm.ls('ESEAL_PLACER')[0] 
             
                #..setKey function sets a keyframe of the given value at the given time.
                object.translateX.setKey(value=2*(-time/fs), time=time) # Moving forward at 1m/s
                object.translateY.setKey(value=2*depth_value, time=time)
             
                pitch_value = float(row[PITCH_DEG]) 
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
                
                print('setting swim = %s, glide = %s, y= %s units, pitch= %s, roll = %s for time= %s frames' % (swim_stroke, glide, depth_value , pitch_value , roll_value , time))
                

