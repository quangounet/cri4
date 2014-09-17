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


def perform_spline(MPX,MPY,MPZ):
    res=100
    Nf=len(MPX)
    t=range(0,Nf)
    xsplines,xn=Splines(t,MPX)
    ysplines,yn=Splines(t,MPY)
    xx,yx=splinesToPlot(xsplines,xn,res)
    xy,yy=splinesToPlot(ysplines,yn,res)
    xline=plt.plot(xx,yx)
    yline=plt.plot(xy,yy)
    xvalues=xline[0].get_ydata()
    yvalues=yline[0].get_ydata()

    return xx,yx,xy,yy,xvalues,yvalues


plt.ion() #turns on interactive mode
fig1=plt.figure(1)

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_01.csv') as f:
    MPX=[]
    MPY=[]
    MPZ=[]
    data(f,MPX,MPY,MPZ) #Obtains midpoint values for corresponding file
    X1x,Y1x,X1y,Y1y,xvalues1,yvalues1=perform_spline(MPX,MPY,MPZ)

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_02.csv') as f:
    MPX2=[]
    MPY2=[]
    MPZ2=[]
    data(f,MPX2,MPY2,MPZ2) #Obtains midpoint values for corresponding file
    X2x,Y2x,X2y,Y2y,xvalues2,yvalues2=perform_spline(MPX2,MPY2,MPZ2)

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_03.csv') as f:
    MPX3=[]
    MPY3=[]
    MPZ3=[]
    data(f,MPX3,MPY3,MPZ3) #Obtains midpoint values for corresponding file
    X3x,Y3x,X3y,Y3y,xvalues3,yvalues3=perform_spline(MPX3,MPY3,MPZ3)


if len(X1x)<len(X2x) and len(X1x)<len(X3x):
    nf=len(X1x)
elif len(X2x)<len(X1x) and len(X2x)<len(X3x):
    nf=len(X2x)
else:
    nf=len(X3x)


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
    X_axis1.append(xvalues1[sample[i]*len(Y1x)])
    Y_axis1.append(yvalues1[sample[i]*len(Y1y)])
    X_axis2.append(xvalues2[sample[i]*len(Y2x)])
    Y_axis2.append(yvalues2[sample[i]*len(Y2y)])
    X_axis3.append(xvalues3[sample[i]*len(Y3x)])
    Y_axis3.append(yvalues3[sample[i]*len(Y3y)])
    meanX.append(Decimal((X_axis1[i]+X_axis2[i]+X_axis3[i]))/3)
    meanY.append(Decimal((Y_axis1[i]+Y_axis2[i]+Y_axis3[i]))/3)


print(nf)    
fig1.suptitle('Midpoint Trajectories')
plt.xlabel('Time')
plt.ylabel('X/Y Axis')


fig2=plt.figure(2)
mean_traject=plt.plot(meanX,meanY)
traj1=plt.plot(MPX,MPY)
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
