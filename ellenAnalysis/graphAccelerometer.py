import pandas as pd
from matplotlib.pyplot import *
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D 
import csv
import matplotlib.pyplot as plt


variables = []

loggingTime = []
loggingSample = []

accelerometerAccelerationX = []
accelerometerAccelerationY = []
accelerometerAccelerationZ = []

i = 0


#Matrix operations
def square(list):
    return [i ** 2 for i in list]

def squareRoot(list):
    return [i ** .5 for i in list]

def add(list1, list2, list3):
    return [x + y  + z for x, y, z in zip(list1, list2, list3)]



#Open csv file
with open('2015-10-05_21-20-50.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for row in spamreader:
		#if the row is after the first row
		if i > 0:

			loggingSample.append(float(row [loggingSampleind]))
			time = (row[loggingTimeind]).split(':')

			#Convert minutes to seconds and add the seconds for 2 different time formats
			if len(time) > 2:
				seconds = float(time[1]) * 60 + float(time[2]) 
			else:
				seconds = float(time[0]) * 60 + float(time[1]) 

			#Make arrays of loggingTime and the user motion
			loggingTime.append(seconds)
			accelerometerAccelerationX.append(float(row [motionUserAccelerationXind]))
			accelerometerAccelerationY.append(float(row [motionUserAccelerationYind]))
			accelerometerAccelerationZ.append(float(row [motionUserAccelerationZind]))

		#if the row is the first row, make an array of the parameters
		else:
			for j in row:
				variables.append(j)

			#Then find the index of the values we care about
			motionUserAccelerationXind = variables.index('motionUserAccelerationX')
			motionUserAccelerationYind = variables.index('motionUserAccelerationY')
			motionUserAccelerationZind = variables.index('motionUserAccelerationZ')
			loggingSampleind = variables.index('loggingSample')
			loggingTimeind = variables.index('loggingTime')

		i = 1


#Calculate magnitude of acceleration vector
accelerationMagnitude = squareRoot(add(square(accelerometerAccelerationX),  square(accelerometerAccelerationY), square(accelerometerAccelerationZ)))


#Store data in data frame. I don't understand this stuff very well
data = {'accelerationMagnitude' : pd.Series(accelerationMagnitude, index=loggingTime)}
df = pd.DataFrame(data)
df=df.astype(float)

#Set up the plot
fig, axes = plt.subplots(nrows=3, ncols=1)
for i, c in enumerate(df.columns):
    df[c].plot(kind='line', ax=axes[i], figsize=(24, 24), title=c)
#plt.savefig('EU1.png', bbox_inches='tight')


plt.show()


