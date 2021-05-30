import csv
import pymel.core as pm

#Defining variables which will be used as column indices
SECONDS      = 0
PITCH_DEG    = 1
ROLL_DEG     = 2
HEAD_DEG     = 3
X_POS        = 4
Z_POS        = 5
DEPTH        = 6
 
#Defining two variables which will be used as indices where animation starts and ends 
START = 0  #start time in sec
END = 12   #end time in sec

fs = 10 #Sample frequency (in Hz or "samples per second")

#Reading in .csv file (update to reflect your own path)
with open('~data/01_Example_PositionRotationData.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    
    #For loop runs through all rows in data .csv file
    for i, row in enumerate(data):
        if i % 10000 == 0:
            print 'Processing row %s' % (i)
            #Print progress in with data row counter in console to keep track of if/where code gets stuck
                
        #If the row number is between the start and end indices of where we want to animate, run this code.        
        if i >= START*fs and i < END*fs: 
            
            #We will use the function float() to return floating point numbers (with decimals) for data values
            
            time = float(i) / fs - START #Translate .csv data time into animation time
            time = time * 24 #Get from frames to seconds
            
            translateX_value = float(row[X_POS])
            translateZ_value = float(row[Z_POS]) #to fit axis orientations
            depth_value      = float(row[DEPTH])
            
            #Define which object will be transformed according to data (use name as described in "Outliner")
            object = pm.ls('elephantseal')[0] 
            
            #..setKey function sets a keyframe of the given value at the given time.
            object.translateX.setKey(value=translateX_value, time=time)
            object.translateZ.setKey(value=translateZ_value, time=time)
            object.translateY.setKey(value=depth_value, time=time)
            
            pitch_value = -float(row[PITCH_DEG]) 
            head_value  = float(row[HEAD_DEG])
            roll_value  = float(row[ROLL_DEG])
            
            #..setKey function sets a keyframe of the given value at the given time.
            object.rotateX.setKey(value=pitch_value, time=time)
            object.rotateY.setKey(value=head_value, time=time)
            object.rotateZ.setKey(value=roll_value, time=time)

            print 'setting y= %s msw, x= %s, z= %s, rotX= %s, rotY= %s, rotZ = %s for time= %s frames' % (depth_value , translateX_value , translateZ_value , pitch_value , head_value , roll_value , time)