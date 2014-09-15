from splines_function import Splines
from splines_function import splinesToPlot
import csv
from collections import defaultdict
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
import matplotlib.pyplot as plt
from extract_midpoint import data
from normalize import normalize
import numpy as np

plt.ion() #turns on interactive mode
fig1=plt.figure(1)

res=100

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_01.csv') as f:
    MPX=[]
    MPY=[]
    MPZ=[]
    data(f,MPX,MPY,MPZ) #Obtains midpoint values for corresponding file
    Nf1=len(MPX)
    t=range(0,Nf1)
    xsplines1,xn1=Splines(t,MPX)
    ysplines1,yn1=Splines(t,MPY)
    X1x,Y1x=splinesToPlot(xsplines1,xn1,res)
    X1y,Y1y=splinesToPlot(ysplines1,yn1,res)
    xline1=plt.plot(X1x,Y1x)
    yline1=plt.plot(X1y,Y1y)
    xvalues1=xline1[0].get_ydata()
    yvalues1=yline1[0].get_ydata()

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_02.csv') as f:
    MPX2=[]
    MPY2=[]
    MPZ2=[]
    data(f,MPX2,MPY2,MPZ2) #Obtains midpoint values for corresponding file
    Nf2=len(MPX2)
    t2=range(0,Nf2)
    xsplines2,xn2=Splines(t2,MPX2)
    ysplines2,yn2=Splines(t2,MPY2)
    X2x,Y2x=splinesToPlot(xsplines2,xn2,res)
    X2y,Y2y=splinesToPlot(ysplines2,yn2,res)
    xline2=plt.plot(X2x,Y2x)
    yline2=plt.plot(X2y,Y2y)
    xvalues2=xline2[0].get_ydata()
    yvalues2=yline2[0].get_ydata()

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_BF_03.csv') as f:
    MPX3=[]
    MPY3=[]
    MPZ3=[]
    data(f,MPX3,MPY3,MPZ3) #Obtains midpoint values for corresponding file
    Nf3=len(MPX3)
    t3=range(0,Nf3)
    xsplines3,xn3=Splines(t3,MPX3)
    ysplines3,yn3=Splines(t3,MPY3)
    X3x,Y3x=splinesToPlot(xsplines3,xn3,res)
    X3y,Y3y=splinesToPlot(ysplines3,yn3,res)
    xline3=plt.plot(X3x,Y3x)
    yline3=plt.plot(X3y,Y3y)
    xvalues3=xline3[0].get_ydata()
    yvalues3=yline3[0].get_ydata()

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
