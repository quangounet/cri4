from extract_midpoint import data
from derivative import *
from perform_splines import perform_spline
from frame_comparison import compare
from trajectory_deviation import traj_dev
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D

plt.ion() #turns on interactive mode
fig1=plt.figure(1)

with open('/home/cuebong/git/cri4/data_5_9_14/C03/C03_C4W_L_bleu_BF_01.csv') as f:
    MPX1=[]
    MPY1=[]
    MPZ1=[]
    data(f,MPX1,MPY1,MPZ1) #Obtains midpoint values for corresponding file
    time1,x1,y1,xvalues1,yvalues1=perform_spline(MPX1,MPY1)

with open('/home/cuebong/git/cri4/data_5_9_14/C03/C03_C4W_L_bleu_BF_02.csv') as f:
    MPX2=[]
    MPY2=[]
    MPZ2=[]
    data(f,MPX2,MPY2,MPZ2) #Obtains midpoint values for corresponding file
    time2,x2,y2,xvalues2,yvalues2=perform_spline(MPX2,MPY2)

with open('/home/cuebong/git/cri4/data_5_9_14/C03/C03_C4W_L_bleu_BF_03.csv') as f:
    MPX3=[]
    MPY3=[]
    MPZ3=[]
    data(f,MPX3,MPY3,MPZ3) #Obtains midpoint values for corresponding file
    time3,x3,y3,xvalues3,yvalues3=perform_spline(MPX3,MPY3)


nf=compare(time1,time2,time3)

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

plt.close(1)
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


time1,vel_x1=deriv_vel(x1)
time1,vel_y1=deriv_vel(y1)
time2,vel_x2=deriv_vel(x2)
time2,vel_y2=deriv_vel(y2)
time3,vel_x3=deriv_vel(x3)
time3,vel_y3=deriv_vel(y3)

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

nf2=compare(time1,time2,time3)

plt.figure(4)

v1=interpolate.UnivariateSpline(time1,vel1,s=0.1)(time1)
v2=interpolate.UnivariateSpline(time2,vel2,s=0.1)(time2)
v3=interpolate.UnivariateSpline(time3,vel3,s=0.1)(time3)
v1line=plt.plot(time1,v1)
v2line=plt.plot(time2,v2)
v3line=plt.plot(time3,v3)
v1values=v1line[0].get_ydata()
v2values=v2line[0].get_ydata()
v3values=v3line[0].get_ydata()

meanVel=[]
velocity1=[]
velocity2=[]
velocity3=[]
sample2=[]

for i in xrange(0,nf2):
    sample2.append(Decimal(i)/nf2)
    velocity1.append(v1values[sample[i]*len(v1)])
    velocity2.append(v2values[sample[i]*len(v2)])
    velocity3.append(v3values[sample[i]*len(v3)])
    meanVel.append(Decimal((velocity1[i]+velocity2[i]+velocity3[i]))/3)

plt.close(4)
fig5=plt.figure(5)
mean_Vtraj=plt.plot(sample2,meanVel)
vtrace1=plt.plot(sample2,velocity1)
vtrace2=plt.plot(sample2,velocity2)
vtrace3=plt.plot(sample2,velocity3)
plt.setp(vtrace1, linestyle='--')
plt.setp(vtrace2, linestyle='--')
plt.setp(vtrace3, linestyle='--')
plt.xlabel('Normalised Time')
plt.ylabel('Velocity (m/s)')
fig5.suptitle('Mean Velocity Profile')


#time1,acc_x1=deriv(vel_x1)
#time1,acc_y1=deriv(vel_y1)
#time2,acc_x2=deriv(vel_x2)
#time2,acc_y2=deriv(vel_y2)
#time3,acc_x3=deriv(vel_x3)
#time3,acc_y3=deriv(vel_y3)

#acc1=resultant_profile(acc_x1,acc_y1)
#acc2=resultant_profile(acc_x2,acc_y2)
#acc3=resultant_profile(acc_x3,acc_y3)

time1,acc1=deriv_accel(v1)
time2,acc2=deriv_accel(v2)
time3,acc3=deriv_accel(v3)

nf3=compare(time1,time2,time3)
plt.figure(1)

a1=interpolate.UnivariateSpline(time1,acc1,s=0.0000001)(time1)
a2=interpolate.UnivariateSpline(time2,acc2,s=0.0000001)(time2)
a3=interpolate.UnivariateSpline(time3,acc3,s=0.0000001)(time3)
a1line=plt.plot(time1,a1)
a2line=plt.plot(time2,a2)
a3line=plt.plot(time3,a3)
a1values=a1line[0].get_ydata()
a2values=a2line[0].get_ydata()
a3values=a3line[0].get_ydata()

meanAcc=[]
Acceleration1=[]
Acceleration2=[]
Acceleration3=[]
sample3=[]

for i in xrange(0,nf3):
    sample3.append(Decimal(i)/nf3)
    Acceleration1.append(a1values[sample[i]*len(a1)])
    Acceleration2.append(a2values[sample[i]*len(a2)])
    Acceleration3.append(a3values[sample[i]*len(a3)])
    meanAcc.append(Decimal((Acceleration1[i]+Acceleration2[i]+Acceleration3[i]))/3)

plt.close(1)
fig7=plt.figure(7)
mean_atraj=plt.plot(sample3,meanAcc)
atrace1=plt.plot(sample3,Acceleration1)
atrace2=plt.plot(sample3,Acceleration2)
atrace3=plt.plot(sample3,Acceleration3)
plt.setp(atrace1, linestyle='--')
plt.setp(atrace2, linestyle='--')
plt.setp(atrace3, linestyle='--')
plt.xlabel('Normalised Time')
plt.ylabel('Acceleration (m/s2)')
fig7.suptitle('Mean Acceleration Profile')

fig8=plt.figure(8)
ax=fig8.add_subplot(111,projection='3d')
plt.rcParams['legend.fontsize']=10
ax.plot(meanX,meanY,sample,'o',markersize=8,color='blue',alpha=0.5)
#Axes3D.scatter(meanX,meanY,sample)
