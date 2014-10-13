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
from read_filenames import get_filepaths
import sys
from mean_traj import mean_calc
from variance_ellipse import variance_ellipse

plt.ion() #turns on interactive mode
fig1=plt.figure(1)

file_paths=[]
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/P07"))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/P07"))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/P07"))
use_files,nf,meanX,meanY,sample,Xax,Yax=[],[],[],[],[],[],[]
MPX,MPY,MPZ,time,x,y,xvalues,yvalues=[],[],[],[],[],[],[],[]

for i in xrange(0,len(file_paths)):
    use_files.append([])
    for j in xrange(0,len(file_paths[i])):
    	filename=file_paths[i][j]
    	if i==0:
		target='C2N_S_vert_BF_'
	elif i==1:
		target='C4E_L_bleu_BF_'
	else:
		target='C4W_R_rouge_BF_'

    	if target in filename:
       		use_files[i].append(filename)
    if len(use_files[i])!=3:
	sys.exit("Error: not enough datasets")

    MPX.append([])
    MPY.append([])
    MPZ.append([])
    time.append([])
    x.append([])
    y.append([])
    xvalues.append([])
    yvalues.append([])
    Xax.append([])
    Yax.append([])

    for j in xrange(0,len(use_files[i])):
        with open(use_files[i][j]) as f:
    	    a,b,c=data(f)
	    MPX[i].append(a)
	    MPY[i].append(b)
	    MPZ[i].append(c)
	    d,e,f,g,h=perform_spline(MPX[i][j],MPY[i][j])
	    time[i].append(d)
	    x[i].append(e)
	    y[i].append(f)
	    xvalues[i].append(g)
	    yvalues[i].append(h)

    nf.append(compare(time[i][0],time[i][1],time[i][2]))

    a,b,c,d,e,f,g,h,k=mean_calc(nf[i],x[i][0],x[i][1],x[i][2],y[i][0],y[i][1],y[i][2],xvalues[i][0],xvalues[i][1],xvalues[i][2],yvalues[i][0],yvalues[i][1],yvalues[i][2])
    meanX.append(a)
    meanY.append(b)
    sample.append(c)
    Xax[i].append(d)
    Xax[i].append(e)
    Xax[i].append(f)
    Yax[i].append(g)
    Yax[i].append(h)
    Yax[i].append(k)

plt.close(1)
"""
fig2=plt.figure(2)
plt.plot(meanX[0],meanY[0],meanX[1],meanY[1],meanX[2],meanY[2])
traj1=plt.plot(MPX[0][0],MPY[0][0],MPX[0][1],MPY[0][1],MPX[0][2],MPY[0][2])
traj2=plt.plot(MPX[1][0],MPY[1][0],MPX[1][1],MPY[1][1],MPX[1][2],MPY[1][2])
traj3=plt.plot(MPX[2][0],MPY[2][0],MPX[2][1],MPY[2][1],MPX[2][2],MPY[2][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
plt.axis('equal')
plt.xlabel=('X-axis')
plt.ylabel=('Y-axis')
fig2.suptitle('Mean Trajectory')
"""

#_____________________________________________________________________

fig3=plt.figure(3)
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
fig3.suptitle('P07 Trajectories')

variability=[]

for i in xrange(0,len(file_paths)):
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i)
    variability.append(a)
        
plt.plot(meanX[0],meanY[0],meanX[1],meanY[1],meanX[2],meanY[2])
traj1=plt.plot(MPX[0][0],MPY[0][0],MPX[0][1],MPY[0][1],MPX[0][2],MPY[0][2])
traj2=plt.plot(MPX[1][0],MPY[1][0],MPX[1][1],MPY[1][1],MPX[1][2],MPY[1][2])
traj3=plt.plot(MPX[2][0],MPY[2][0],MPX[2][1],MPY[2][1],MPX[2][2],MPY[2][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')

fig4=plt.figure(4)
plt.plot(sample[0],variability[0],sample[1],variability[1],sample[2],variability[2])
plt.xlim(0, 1)
plt.ylim(0, 1.9)
plt.xlabel('Time')
plt.ylabel('Variability')
fig4.suptitle('P07 Variance Profile')
