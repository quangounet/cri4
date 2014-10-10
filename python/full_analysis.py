from extract_midpoint import data
from derivative import *
from perform_splines import perform_spline
from frame_comparison import compare
from trajectory_deviation import traj_dev
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
import matplotlib.pyplot as plt
import numpy as np
from numpy import *
from scipy import interpolate
from matplotlib.patches import Ellipse
from pylab import *

plt.ion() #turns on interactive mode
fig1=plt.figure(1)
#________________P01___________________#
with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C1N_S_vert_VF_01.csv') as f:
    MPX11=[]
    MPY11=[]
    MPZ11=[]
    data(f,MPX11,MPY11,MPZ11) #Obtains midpoint values for corresponding file
    time11,x11,y11,xvalues11,yvalues11=perform_spline(MPX11,MPY11)

with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C1N_S_vert_VF_02.csv') as f:
    MPX12=[]
    MPY12=[]
    MPZ12=[]
    data(f,MPX12,MPY12,MPZ12) #Obtains midpoint values for corresponding file
    time12,x12,y12,xvalues12,yvalues12=perform_spline(MPX12,MPY12)

with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C1N_S_vert_VF_03.csv') as f:
    MPX13=[]
    MPY13=[]
    MPZ13=[]
    data(f,MPX13,MPY13,MPZ13) #Obtains midpoint values for corresponding file
    time13,x13,y13,xvalues13,yvalues13=perform_spline(MPX13,MPY13)

nf11=compare(time11,time12,time13)

meanX1=[]
meanY1=[]
X_axis11=[]
Y_axis11=[]
X_axis12=[]
Y_axis12=[]
X_axis13=[]
Y_axis13=[]
sample11=[]

for i in xrange(0,nf11):
    sample11.append(Decimal(i)/nf11)
    X_axis11.append(xvalues11[sample11[i]*len(x11)])
    Y_axis11.append(yvalues11[sample11[i]*len(y11)])
    X_axis12.append(xvalues12[sample11[i]*len(x12)])
    Y_axis12.append(yvalues12[sample11[i]*len(y12)])
    X_axis13.append(xvalues13[sample11[i]*len(x13)])
    Y_axis13.append(yvalues13[sample11[i]*len(y13)])
    meanX1.append(Decimal((X_axis11[i]+X_axis12[i]+X_axis13[i]))/3)
    meanY1.append(Decimal((Y_axis11[i]+Y_axis12[i]+Y_axis13[i]))/3)

#________________P02_____________________#
with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C4E_R_rouge_VF_01.csv') as f:
    MPX21=[]
    MPY21=[]
    MPZ21=[]
    data(f,MPX21,MPY21,MPZ21) #Obtains midpoint values for corresponding file
    time21,x21,y21,xvalues21,yvalues21=perform_spline(MPX21,MPY21)

with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C4E_R_rouge_VF_02.csv') as f:
    MPX22=[]
    MPY22=[]
    MPZ22=[]
    data(f,MPX22,MPY22,MPZ22) #Obtains midpoint values for corresponding file
    time22,x22,y22,xvalues22,yvalues22=perform_spline(MPX22,MPY22)

with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C4E_R_rouge_VF_03.csv') as f:
    MPX23=[]
    MPY23=[]
    MPZ23=[]
    data(f,MPX23,MPY23,MPZ23) #Obtains midpoint values for corresponding file
    time23,x23,y23,xvalues23,yvalues23=perform_spline(MPX23,MPY23)

nf21=compare(time21,time22,time23)

meanX2=[]
meanY2=[]
X_axis21=[]
Y_axis21=[]
X_axis22=[]
Y_axis22=[]
X_axis23=[]
Y_axis23=[]
sample21=[]

for i in xrange(0,nf21):
    sample21.append(Decimal(i)/nf21)
    X_axis21.append(xvalues21[sample21[i]*len(x21)])
    Y_axis21.append(yvalues21[sample21[i]*len(y21)])
    X_axis22.append(xvalues22[sample21[i]*len(x22)])
    Y_axis22.append(yvalues22[sample21[i]*len(y22)])
    X_axis23.append(xvalues23[sample21[i]*len(x23)])
    Y_axis23.append(yvalues23[sample21[i]*len(y23)])
    meanX2.append(Decimal((X_axis21[i]+X_axis22[i]+X_axis23[i]))/3)
    meanY2.append(Decimal((Y_axis21[i]+Y_axis22[i]+Y_axis23[i]))/3)


#______________________P03__________________#
with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C4W_L_bleu_VF_01.csv') as f:
    MPX31=[]
    MPY31=[]
    MPZ31=[]
    data(f,MPX31,MPY31,MPZ31) #Obtains midpoint values for corresponding file
    time31,x31,y31,xvalues31,yvalues31=perform_spline(MPX31,MPY31)

with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C4W_L_bleu_VF_02.csv') as f:
    MPX32=[]
    MPY32=[]
    MPZ32=[]
    data(f,MPX32,MPY32,MPZ32) #Obtains midpoint values for corresponding file
    time32,x32,y32,xvalues32,yvalues32=perform_spline(MPX32,MPY32)

with open('/home/cuebong/git/cri4/data_8_10_14/C07/C07_C4W_L_bleu_VF_03.csv') as f:
    MPX33=[]
    MPY33=[]
    MPZ33=[]
    data(f,MPX33,MPY33,MPZ33) #Obtains midpoint values for corresponding file
    time33,x33,y33,xvalues33,yvalues33=perform_spline(MPX33,MPY33)

nf31=compare(time31,time32,time33)
meanX3=[]
meanY3=[]
X_axis31=[]
Y_axis31=[]
X_axis32=[]
Y_axis32=[]
X_axis33=[]
Y_axis33=[]
sample31=[]

for i in xrange(0,nf31):
    sample31.append(Decimal(i)/nf31)
    X_axis31.append(xvalues31[sample31[i]*len(x31)])
    Y_axis31.append(yvalues31[sample31[i]*len(y31)])
    X_axis32.append(xvalues32[sample31[i]*len(x32)])
    Y_axis32.append(yvalues32[sample31[i]*len(y32)])
    X_axis33.append(xvalues33[sample31[i]*len(x33)])
    Y_axis33.append(yvalues33[sample31[i]*len(y33)])
    meanX3.append(Decimal((X_axis31[i]+X_axis32[i]+X_axis33[i]))/3)
    meanY3.append(Decimal((Y_axis31[i]+Y_axis32[i]+Y_axis33[i]))/3)


"""
#____________________________P04_____________________#

with open('/home/cuebong/git/cri4/data_5_9_14/P02/P02_C2N_S_vert_VF_01.csv') as f:
    MPX41=[]
    MPY41=[]
    MPZ41=[]
    data(f,MPX41,MPY41,MPZ41) #Obtains midpoint values for corresponding file
    time41,x41,y41,xvalues41,yvalues41=perform_spline(MPX41,MPY41)

with open('/home/cuebong/git/cri4/data_5_9_14/P02/P02_C2N_S_vert_VF_02.csv') as f:
    MPX42=[]
    MPY42=[]
    MPZ42=[]
    data(f,MPX42,MPY42,MPZ42) #Obtains midpoint values for corresponding file
    time42,x42,y42,xvalues42,yvalues42=perform_spline(MPX42,MPY42)

with open('/home/cuebong/git/cri4/data_5_9_14/P02/P02_C2N_S_vert_VF_03.csv') as f:
    MPX43=[]
    MPY43=[]
    MPZ43=[]
    data(f,MPX43,MPY43,MPZ43) #Obtains midpoint values for corresponding file
    time43,x43,y43,xvalues43,yvalues43=perform_spline(MPX43,MPY43)

nf41=compare(time41,time42,time43)

meanX4=[]
meanY4=[]
X_axis41=[]
Y_axis41=[]
X_axis42=[]
Y_axis42=[]
X_axis43=[]
Y_axis43=[]
sample41=[]

for i in xrange(0,nf41):
    sample41.append(Decimal(i)/nf41)
    X_axis41.append(xvalues41[sample41[i]*len(x41)])
    Y_axis41.append(yvalues41[sample41[i]*len(y41)])
    X_axis42.append(xvalues42[sample41[i]*len(x42)])
    Y_axis42.append(yvalues42[sample41[i]*len(y42)])
    X_axis43.append(xvalues43[sample41[i]*len(x43)])
    Y_axis43.append(yvalues43[sample41[i]*len(y43)])
    meanX4.append(Decimal((X_axis41[i]+X_axis42[i]+X_axis43[i]))/3)
    meanY4.append(Decimal((Y_axis41[i]+Y_axis42[i]+Y_axis43[i]))/3)


plt.close(1)
fig2=plt.figure(2)
mean_traject=plt.plot(meanX1,meanY1,meanX2,meanY2,meanX3,meanY3)
traj1=plt.plot(MPX11,MPY11,MPX21,MPY21,MPX31,MPY31)
traj2=plt.plot(MPX12,MPY12,MPX22,MPY22,MPX32,MPY32)
traj3=plt.plot(MPX13,MPY13,MPX23,MPY23,MPX33,MPY33)
plt.setp(traj1, linestyle='--')
plt.setp(traj2, linestyle='--')
plt.setp(traj3, linestyle='--')
plt.axis('equal')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
fig2.suptitle('Mean Trajectory')


fig3=plt.figure(3)
plt.plot(sample11, X_axis11, sample11, X_axis12, sample11, X_axis13)
plt.plot(sample11, Y_axis11, sample11, Y_axis12, sample11, Y_axis13)
fig3.suptitle('Normalised Trajectories')
plt.xlabel('Normalised Time')
plt.ylabel('X/Y Axis')
plt.show



TD1=traj_dev(X_axis11,Y_axis11,meanX1,meanY1)
TD2=traj_dev(X_axis12,Y_axis12,meanX1,meanY1)
TD3=traj_dev(X_axis13,Y_axis13,meanX1,meanY1)


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
"""

#_____________P01_________________#
fig10=plt.figure(10)
plt.axis('equal')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
fig10.suptitle('C07 Trajectory')

variability1=[]

for i in xrange(0,len(sample11)):
    data=array([[X_axis11[i],Y_axis11[i]],[X_axis12[i],Y_axis12[i]],[X_axis13[i],Y_axis13[i]]])
    data2=array(data)
    
    meanxval=mean(data[:,0])
    meanyval=mean(data[:,1])
    
    for i in range(data.shape[0]):
        data2[i,0] = data[i,0] - meanxval
        data2[i,1] = data[i,1] - meanyval

    ax = gca()

    xy = (meanxval,meanyval)
    u,d,v = linalg.svd(data2)
    width = d[0]
    height = d[1]
 
    angle = arctan2(v[0,1],v[0,0])*180/pi
    variability1.append(sqrt(width*width+height*height))
    ellipse = Ellipse(xy, width, height, angle, edgecolor='c', fc='None', lw=2)
    ax.add_patch(ellipse)

mean_traject=plt.plot(meanX1,meanY1,meanX2,meanY2,meanX3,meanY3)
traj1=plt.plot(MPX11,MPY11,MPX21,MPY21,MPX31,MPY31)
traj2=plt.plot(MPX12,MPY12,MPX22,MPY22,MPX32,MPY32)
traj3=plt.plot(MPX13,MPY13,MPX23,MPY23,MPX33,MPY33)
plt.setp(traj1, linestyle='--')
plt.setp(traj2, linestyle='--')
plt.setp(traj3, linestyle='--')

#_____________P02___________________#

variability2=[]

for i in xrange(0,len(sample21)):
    data=array([[X_axis21[i],Y_axis21[i]],[X_axis22[i],Y_axis22[i]],[X_axis23[i],Y_axis23[i]]])
    data2=array(data)
    
    meanxval=mean(data[:,0])
    meanyval=mean(data[:,1])
    
    for i in range(data.shape[0]):
        data2[i,0] = data[i,0] - meanxval
        data2[i,1] = data[i,1] - meanyval

    ax = gca()

    xy = (meanxval,meanyval)
    u,d,v = linalg.svd(data2)
    width = d[0]
    height = d[1]
 
    angle = arctan2(v[0,1],v[0,0])*180/pi
    variability2.append(sqrt(width*width+height*height))
    ellipse = Ellipse(xy, width, height, angle, edgecolor='y', fc='None', lw=2)
    ax.add_patch(ellipse)

#_____________P03_____________#
variability3=[]

for i in xrange(0,len(sample31)):
    data=array([[X_axis31[i],Y_axis31[i]],[X_axis32[i],Y_axis32[i]],[X_axis33[i],Y_axis33[i]]])
    data2=array(data)
    
    meanxval=mean(data[:,0])
    meanyval=mean(data[:,1])
    
    for i in range(data.shape[0]):
        data2[i,0] = data[i,0] - meanxval
        data2[i,1] = data[i,1] - meanyval

    ax = gca()

    xy = (meanxval,meanyval)
    u,d,v = linalg.svd(data2)
    width = d[0]
    height = d[1]

    angle = arctan2(v[0,1],v[0,0])*180/pi
    variability3.append(sqrt(width*width+height*height))
    ellipse = Ellipse(xy, width, height, angle, edgecolor='m', fc='None', lw=2)
    ax.add_patch(ellipse)
"""
#_______________P04______________#

variability4=[]

for i in xrange(0,len(sample41)):
    data=array([[X_axis41[i],Y_axis41[i]],[X_axis42[i],Y_axis42[i]],[X_axis43[i],Y_axis43[i]]])
    data2=array(data)
    
    meanxval=mean(data[:,0])
    meanyval=mean(data[:,1])
    
    for i in range(data.shape[0]):
        data2[i,0] = data[i,0] - meanxval
        data2[i,1] = data[i,1] - meanyval

    ax = gca()

    xy = (meanxval,meanyval)
    u,d,v = linalg.svd(data2)
    width = d[0]
    height = d[1]

    angle = arctan2(v[0,1],v[0,0])*180/pi
    variability4.append(sqrt(width*width+height*height))
    ellipse = Ellipse(xy, 2*width, 2*height, angle, edgecolor='b', fc='None', lw=2)
    ax.add_patch(ellipse)
"""
fig11=plt.figure(11)
plt.plot(sample11,variability1,sample21,variability2,sample31,variability3)
plt.xlabel('Time')
plt.ylabel('Variability')
fig11.suptitle('C07 Variance Profile')


