"""
Accelerometer 3D data visualization
INFO290 Humans, Sensors, Data and Apps Project. UC Berkeley
Author: Vincent van den Goor
"""
import viz
import vizact
import vizcam
import os
import glob
import time
import viztask
import math
import vizshape

datafile = 'walktest.csv'

labels = ["LINEAR ACCELERATION X (m/s²)", "LINEAR ACCELERATION Y (m/s²)", "LINEAR ACCELERATION Z (m/s²)",
          "ORIENTATION Z (azimuth °)",    "ORIENTATION X (pitch °)",      "ORIENTATION Y (roll °)",
          "Time since start in ms "]
labelsIOS = [ "UserAccelerationX", "UserAccelerationY",  "UserAccelerationZ",
              "gyroRotationX",     "gyroRotationY",      "gyroRotationZ",
              "accelerometerTimestamp_sinceReboot"]
labelpos = [-1, -1, -1, -1, -1, -1, -1]         # Label indexing
[accx, accy, accz, acc_M] = [[], [], [], []] 
[posx, posy, posz] = [0,0,5]
[yaw, pitch, roll] = [[],[],[]]
[cpx,  cpy,  cpz ] = [[],[],[]]
alpha = []          # List of alpha values
ts = []             # List of timestamps
dt = 0              # Length of the frame [s]
g = 9.81            # Gravity constant
GAIN = 1            # Multiplication required for different measuring apps
NOISE_AMP = 0.2     # Amplitude windowing threshold
MAX_AMP = 17        # Cut-off amplitude for red color
Z_LOWPASS = 10      # Number of samples for the lowpass-filter
SPHERESIZE = 0.8    # Size of the starting sphere for each datapoint
animspeed = 0.25    # Speed of rotation animation
mill = 0            # Second/milliseconds (app-dependent)
dist = 1.5          # Distance to tail
TAILDECAY = .5      # Speed of decay, default=0.5
tail = []

viz.fov(60)
viz.go()
viz.window.setFullscreen(viz.ON)

# Initialize world
viz.clearcolor( viz.SLATE )
ground = viz.addChild( 'ground.osgb' )
ground.setScale(4,4,4)
# Setup the spheres for the trail of data
sphere = vizshape.addSphere(0.25,10,10)
sphere.visible(viz.OFF)
sphere.alpha(0.9)
sphere.setScale(SPHERESIZE,SPHERESIZE,SPHERESIZE)
# Directional data, currently unused
#cone = vizshape.addCone(0.2,0.3,10)
#cone.alpha(0.4)
#cone.visible(viz.OFF)

## Loads the accelerometer data. Automatically detects Android and IOS versions
def loadcsv():
        global labels, mill, GAIN, MAX_AMP
        path = os.path.dirname(os.path.realpath(__file__))+'\\'
        fileName = path + datafile
        print("\nProcessing: " + fileName)
        trialid = 0
        try:
            with open(fileName, 'r') as f:
                w = []
                for line in f:
                    line = line.rstrip('\n')
                    w = line.split(',')
                    if trialid==0:
                        for a in w:
                            if a == "accelerometerTimestamp_sinceReboot":
                                print 'IOS version detected, changing reference labels'
                                labels = labelsIOS
                                GAIN = 10
                                MAX_AMP = 10
                                mill = 1
                            elif a == "LINEAR ACCELERATION X (m/s²)":
                                print 'Android version detected. Using default reference labels'
                                GAIN = 1
                                MAX_AMP = 17
                                mill = 1000
                                
                        # Check the labels
                        for x in range(0,len(w)):
                            for y in range(0,len(labels)):
                                if w[x].find(labels[y])>-1:
                                    #print w[x]
                                    labelpos[y]=x
                                    #print labelpos
                                    
                    else:
                        # Regular data; only look for data we want to use
                        for x in range(0, len(labelpos)):
                            if not labelpos[x] ==-1:
                                y = w[labelpos[x]]
                                if x == 0:
                                    accx.extend([float(y)*GAIN])
                                elif x ==1:
                                    accy.extend([float(y)*GAIN])
                                elif x ==2:
                                    accz.extend([float(y)*GAIN])
                                elif x ==3:
                                    yaw.extend([float(y)])
                                elif x ==4:
                                    pitch.extend([float(y)])
                                elif x ==5:
                                    roll.extend([float(y)])
                                elif x ==6:
                                    ys = float(y)/mill
                                    ts.extend([ys])
                    cols = len(w)
                    trialid+=1
            f.closed
        except IOError:
            print "Failed to open %s! No idea why though, figure it out yourself." % fileName
        print "Finished checking %i lines of data. Total duration of recording: %f s\n" % (trialid-1, ts[len(ts)-1]-ts[0])

# Runs the 3D animation of accelerometer data
def runanimation():
    global posx, posy, posz, tail, alpha, yaw, pitch, roll
    global GAIN, SPHERESIZE
    print len(accx)
    [lpx, lpy, lpz] = [[],[],[]]
    # Assume the first time is equal to 1/Fs
    dt = t
    dt2 = dt*dt
    starttime = time.time()
    for i in range(0,len(accx)):
        curtime = float(ts[i])
        timenow = time.time()
        if i > 0:
            dt = curtime-float(ts[i-1])
        [ax, ay, az] = [(accx[i]), (accy[i]), (accz[i])]
        
        # Check for gaps in data, do not move if the threshold is reached
        if dt < 0.5:
            # Calculate the new positions. y-axis is the elevation!
            posx += g*ax*dt*dt
            posz += g*ay*dt*dt
            posy += g*az*dt*dt
            lpx.append(posx)
            lpy.append(posy)
            lpz.append(posz)
            while len(lpx)>Z_LOWPASS:
                lpx.pop(0); lpy.pop(0); lpz.pop(0)
            
            partic = sphere.copy()
            partic.setScale(SPHERESIZE,SPHERESIZE,SPHERESIZE)
            partic.setPosition(avg(lpx),avg(lpy)+1,avg(lpz))
            # Direction cone
            '''
            X = viz.Transform()
            X.makeIdent()
            X.preTrans(posx,posy+1,posz)
            X.setEuler([yaw[i], pitch[i], roll[i]])
            X.preTrans(0,0.4,0)
            cone.setMatrix(X)
            '''
            # Moving average for camera position
            cpx.append(posx); cpy.append(posy); cpz.append(posz)
            while len(cpx) > 15:
                cpx.pop(0); cpy.pop(0); cpz.pop(0)
            cx = 0; cy = 0; cz = 0
            for j in range(0,len(cpx)):
                cx += cpx[j]; cy += cpy[j]; cz += cpz[j]
            cx/=len(cpx); cy/=len(cpy); cz/=len(cpz)
            
            # Calculate resulting camera position and theatrical movement
            camx = cx + dist * math.sin(curtime*animspeed)
            camz = cz + dist * math.cos(curtime*animspeed)
            camy = cy + 2 + 0.5* math.sin(curtime*animspeed*2)
            
            # Fixate view at the moving average
            viz.MainView.lookAt([cx,cy+1,cz])
            vizcam.PivotNavigate([camx,camy,camz],dist,[1.0,1.0],viz.MainView)
            
            # Change color according to the magnitude
            #amplitude = math.sqrt(ax*ax+ay*ay+az*az)
            red = acc_M[i]/MAX_AMP
            green = 1-acc_M[i]/MAX_AMP
            partic.color(red,green,0)
            tail.append(partic.id)
            alpha.append(1)
            
        decaytail(dt)
        yield viz.waitTime(dt)
    while len(tail) >5:
        decaytail(dt)
        yield viz.waitTime(dt)
    print 'All done in: %f seconds.'%(time.time()-starttime)

# Apply the decay to the tail
def decaytail(dt):
    global alpha, tail, TAILDECAY, SPHERESIZE
    for i in range (0,len(tail)-4):
        alpha[i] -= TAILDECAY*dt
        if alpha[i]<=0:
            tail.pop(i)
            alpha.pop(i)
            viz.VizChild(tail[i]).remove()
        else:
            viz.VizChild(tail[i]).alpha(alpha[i])
            viz.VizChild(tail[i]).setScale(SPHERESIZE*alpha[i],SPHERESIZE*alpha[i],SPHERESIZE*alpha[i])

def calc_abs():
    global accx, accy, accz, acc_M, MAX_AMP
    for i in range (0, len(accx)):
        acc_M.append(math.sqrt(accx[i]*accx[i]+accy[i]*accy[i]+accz[i]*accz[i]))
        #print NOISE_AMP, acc_M[i], ' xyz:', accx[i],accy[i],accz[i]
        if acc_M[i] < NOISE_AMP:
            [accx[i], accy[i], accz[i]] = [0,0,0]
            print 'Filtered #%i; amp=%f' % (i, acc_M[i])

# Averaging of a list
def avg(val): return sum(val)/len(val)

# Zooming of the view
def zoom(amount):
    global dist
    dist *= (1+0.05*amount)
    
## Updates the transparancy and size of the elements in the trail
def updateAlpha():
    global tail, alpha
    for i in range (0,len(tail)-5):
        alpha[i] -= 0.1
        viz.VizChild(tail[i]).alpha(alpha[i])

loadcsv()
calc_abs()
endtime = float(ts[len(ts)-1])
t = (float(ts[len(ts)-1])-float(ts[0]))/len(ts)

vizact.onwheeldown(zoom,1)
vizact.onwheelup(zoom,-1)
viztask.schedule(runanimation())