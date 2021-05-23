import csv
import pymel.core as pm

# Defining variables which will be used as column indices
SECONDS = 0
PITCH_DEG = 1
ROLL_DEG = 2
HEAD_DEG = 3
X_POS = 4
Z_POS = 5
DEPTH = 6
GLIDE = 10
STROKE = 12

# Defining two variables which will be used as indices where animation starts and ends
START = 0  # start time in sec
END = 80  # end time in sec

fs = 16  # Sample frequency (in Hz or "samples per second")

# Reading in .csv file (update to reflect your own path)
with open('C:/Users/jmkb9/Documents/GitHub/VisualizingFear/data/Glacier_stroke_analysis.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    headers = next(data)
    print('headers: %s' % headers)

    # For loop runs through all rows in data .csv file
    for i, row in enumerate(data, 1):
        i -= 1 # correct for header row
        
        if i % 10000 == 0:
            print 'Processing row %s' % (i)
            # Print progress in with data row counter in console to keep track of if/where code gets stuck

        # If the row number is between the start and end indices of where we want to animate, run this code.
        if i >= START * fs and i < END * fs:
            # We will use the function float() to return floating point numbers (with decimals) for data values

            clock_time = float(i) / fs - START  # Translate .csv data time into animation time
            time = clock_time * 24 + 1  # Get from seconds to frame
            print('row', i, 'time', clock_time, 'frame', time)

            # translateX_value = float(row[X_POS])
            # translateZ_value = -float(row[Z_POS])  # to fit axis orientations
            # depth_value = float(row[DEPTH])

            # Define which object will be transformed according to data (use name as described in "Outliner")
            object = pm.ls('SWIM_CONTROL')[0]
            
            glide = float(row[GLIDE])
            object.glide.setKey(value=glide, time=time)
            
            swim_stroke = int(row[STROKE])
            if swim_stroke:
                object.swim.setKey(value=0, time=time)
                object.swim.setKey(value=1, time=time - .001)
                pm.keyTangent(object.swim, inTangentType='linear', outTangentType='linear', time=(time - .001, time))


#FIXMEEE
            # ..setKey function sets a keyframe of the given value at the given time.
            object.translateX.setKey(value=translateX_value, time=time)
            object.translateZ.setKey(value=translateZ_value, time=time)
            object.translateY.setKey(value=depth_value, time=time)

            pitch_value = float(row[PITCH_DEG])
            head_value = float(row[HEAD_DEG])
            roll_value = float(row[ROLL_DEG])

            # ..setKey function sets a keyframe of the given value at the given time.
            object.rotateX.setKey(value=pitch_value, time=time)
            object.rotateY.setKey(value=head_value, time=time)
            object.rotateZ.setKey(value=roll_value, time=time)

            print 'setting y= %s msw, x= %s, z= %s, rotX= %s, rotY= %s, rotZ = %s for time= %s frames' % (
                depth_value, translateX_value, translateZ_value, pitch_value, head_value, roll_value, time)

