from extract_midpoint import data
from derivative import deriv
from perform_splines import perform_spline
from trajectory_deviation import traj_dev
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

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


TD1=traj_dev(X_axis1,Y_axis1,meanX,meanY)
TD2=traj_dev(X_axis2,Y_axis2,meanX,meanY)
TD3=traj_dev(X_axis3,Y_axis3,meanX,meanY)


time1,vel_x1=deriv(x1)
time1,vel_y1=deriv(y1)
time2,vel_x2=deriv(x2)
time2,vel_y2=deriv(y2)
time3,vel_x3=deriv(x3)
time3,vel_y3=deriv(y3)

def resultant_profile(x,y):
    val=[]
    for i in xrange(0,len(x)):
        x_term=x[i]*x[i]
        y_term=y[i]*y[i]
        a=(x_term+y_term)**0.5
        val.append(a)

    return val

vel1=resultant_profile(vel_x1,vel_y1)
vel2=resultant_profile(vel_x2,vel_y2)
vel3=resultant_profile(vel_x3,vel_y3)

plt.figure(4)
plt.plot(time1,vel1,time2,vel2,time3,vel3)

time1,acc_x1=deriv(vel_x1)
time1,acc_y1=deriv(vel_y1)
time2,acc_x2=deriv(vel_x2)
time2,acc_y2=deriv(vel_y2)
time3,acc_x3=deriv(vel_x3)
time3,acc_y3=deriv(vel_y3)

plt.figure(5)
plt.plot(time1,acc_x1,time1,acc_y1,time2,acc_x2,time2,acc_y2,time3,acc_x3,time3,acc_y3)
