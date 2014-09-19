from splines_function import Splines
from splines_function import splinesToPlot
from extract_midpoint import data
from normalize import normalize
from collections import defaultdict
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def perform_spline(MPX,MPY,MPZ):
    time=range(0,len(MPX))
    xinterp=interpolate.UnivariateSpline(time,MPX,s=0.000001)(time)
    yinterp=interpolate.UnivariateSpline(time,MPY,s=0.000001)(time)
    xline=plt.plot(time,xinterp)
    yline=plt.plot(time,yinterp)
    xvalues=xline[0].get_ydata()
    yvalues=yline[0].get_ydata()

    return time,xinterp,yinterp,xvalues,yvalues

plt.ion() #turns on interactive mode
fig1=plt.figure(1)

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_01.csv') as f:
    MPX1=[]
    MPY1=[]
    MPZ1=[]
    data(f,MPX1,MPY1,MPZ1) #Obtains midpoint values for corresponding file
    time1,x1,y1,xvalues1,yvalues1=perform_spline(MPX1,MPY1,MPZ1)

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_02.csv') as f:
    MPX2=[]
    MPY2=[]
    MPZ2=[]
    data(f,MPX2,MPY2,MPZ2) #Obtains midpoint values for corresponding file
    time2,x2,y2,xvalues2,yvalues2=perform_spline(MPX2,MPY2,MPZ2)

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_03.csv') as f:
    MPX3=[]
    MPY3=[]
    MPZ3=[]
    data(f,MPX3,MPY3,MPZ3) #Obtains midpoint values for corresponding file
    time3,x3,y3,xvalues3,yvalues3=perform_spline(MPX3,MPY3,MPZ3)


if len(time1)<len(time2) and len(time1)<len(time3):
    nf=len(time1)
elif len(time2)<len(time1) and len(time2)<len(time1):
    nf=len(time2)
else:
    nf=len(time3)

meanX=[]
meanY=[]
X_axis1=[]
Y_axis1=[]
X_axis2=[]
Y_axis2=[]
X_axis3=[]
Y_axis3=[]
sample=[]

for i in xrange(0,nf):
    sample.append(Decimal(i)/nf)
    X_axis1.append(xvalues1[sample[i]*len(x1)])
    Y_axis1.append(yvalues1[sample[i]*len(y1)])
    X_axis2.append(xvalues2[sample[i]*len(x2)])
    Y_axis2.append(yvalues2[sample[i]*len(y2)])
    X_axis3.append(xvalues3[sample[i]*len(x3)])
    Y_axis3.append(yvalues3[sample[i]*len(y3)])
    meanX.append(Decimal((X_axis1[i]+X_axis2[i]+X_axis3[i]))/3)
    meanY.append(Decimal((Y_axis1[i]+Y_axis2[i]+Y_axis3[i]))/3)


print(nf)    
fig1.suptitle('Midpoint Trajectories')
plt.xlabel('Time')
plt.ylabel('X/Y Axis')


fig2=plt.figure(2)
mean_traject=plt.plot(meanX,meanY)
traj1=plt.plot(MPX1,MPY1)
traj2=plt.plot(MPX2,MPY2)
traj3=plt.plot(MPX3,MPY3)
plt.setp(traj1, linestyle='--')
plt.setp(traj2, linestyle='--')
plt.setp(traj3, linestyle='--')
plt.axis('equal')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
fig2.suptitle('Mean Trajectory')


fig3=plt.figure(3)
plt.plot(sample, X_axis1, sample, X_axis2, sample, X_axis3)
plt.plot(sample, Y_axis1, sample, Y_axis2, sample, Y_axis3)
fig3.suptitle('Normalised Trajectories')
plt.xlabel('Normalised Time')
plt.ylabel('X/Y Axis')
plt.show


def traj_dev(Xtraj,Ytraj,Xmean,Ymean):
    sum=0
    for i in xrange(0,len(Xmean)):
        x_term=Decimal(Xtraj[i])-Xmean[i]
        y_term=Decimal(Ytraj[i])-Ymean[i]
        x_sq=x_term*x_term
        y_sq=y_term*y_term
        sum=Decimal(sum)+x_sq+y_sq
    TD=Decimal(sum/len(Xmean)).sqrt()

    return TD

TD1=traj_dev(X_axis1,Y_axis1,meanX,meanY)
TD2=traj_dev(X_axis2,Y_axis2,meanX,meanY)
TD3=traj_dev(X_axis3,Y_axis3,meanX,meanY)
print(TD1,TD2,TD3)

timeN=range(0,len(x1))
timeN=np.array(timeN, dtype=np.float32).transpose()
X_axis=np.array(x1, dtype=np.float32).transpose()
time=np.gradient(timeN)[0]
velocity1=np.gradient(X_axis,time)
plt.figure(4)
plt.plot(timeN,velocity1)

timeO=range(0,len(MPX1))
timeO=np.array(timeO,dtype=np.float32).transpose()
MPX1=np.array(MPX1,dtype=np.float32).transpose()
frames=np.gradient(timeO)[0]
velocityO=np.gradient(MPX1,frames)
plt.plot(timeO, velocityO)

accel1=np.gradient(velocity1,time)
plt.figure(5)
plt.plot(timeN,accel1)

accelO=np.gradient(velocityO,frames)
plt.plot(timeO,accelO)
