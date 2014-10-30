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
from butter_filter import butter_lowpass, butter_lowpass_filter

fs=120.
lowcut=1

"""#---Displaying butterworth filter---
plt.figure(5)
plt.clf()
b,a=butter_lowpass(lowcut,fs,order=2)
w,h=freqz(b,a,worN=500)
plt.plot((fs*0.5/np.pi)*w,abs(h))
"""

plt.ion() #turns on interactive mode
fig1=plt.figure(1)

file_paths=[]
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/C01"))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/C01"))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/C01"))
use_files,nf,meanX,meanY,sample,Xax,Yax=[],[],[],[],[],[],[]
MPX,MPY,MPZ,time,x,y,xvalues,yvalues=[],[],[],[],[],[],[],[]
fX,fY,time_vel,vel_x,vel_y,vel=[],[],[],[],[],[]

for i in xrange(0,len(file_paths)):
    use_files.append([])
    for j in xrange(0,len(file_paths[i])):
    	filename=file_paths[i][j]
    	if i==0:
		target='C3N_S_vert_BF_'
	elif i==1:
		target='C4N_L_bleu_BF_'
	else:
		target='C4N_R_rouge_BF_'

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
    fX.append([])
    fY.append([])
    time_vel.append([])
    vel_x.append([])
    vel_y.append([])
    vel.append([])

    for j in xrange(0,len(use_files[i])):
        with open(use_files[i][j]) as f:
    	    a,b,c=data(f)
	    MPX[i].append(a)
	    MPY[i].append(b)
	    MPZ[i].append(c)
            noiseX=[]
            noiseY=[]
            for l in xrange(0,len(MPX[i][j])):
                noiseX.append(float(MPX[i][j][l]))
                noiseY.append(float(MPY[i][j][l]))
            fX[i].append(butter_lowpass_filter(noiseX,lowcut,fs,order=2))
            fY[i].append(butter_lowpass_filter(noiseY,lowcut,fs,order=2))
	    d,e,f,g,h=perform_spline(fX[i][j],fY[i][j])
	    time[i].append(d)
	    x[i].append(e)
	    y[i].append(f)
	    xvalues[i].append(g)
	    yvalues[i].append(h)

plt.close(1)

#__________Velocity_Profile_______________________
def resultant_profile(x,y):
    val=[]
    for i in xrange(0,len(x)):
        x_term=x[i]*x[i]
        y_term=y[i]*y[i]
        a=(x_term+y_term)**0.5
        val.append(a)
    return val

for i in xrange(0,len(file_paths)):
    for j in xrange(0,len(use_files[i])):
        a,b=deriv_vel(x[i][j])
        time_vel[i].append(a)
        vel_x[i].append(b)
        a,c=deriv_vel(y[i][j])
        vel_y[i].append(c)
        d=resultant_profile(vel_x[i][j],vel_y[i][j])
        vel[i].append(d)

        while len(time_vel[i][j])!=len(vel[i][j]):
            if len(time_vel[i][j])>len(vel[i][j]):
                time_vel[i][j]=np.delete(time_vel[i][j],(len(time_vel[i][j])-1))
            else:
                vel[i][j]=np.delete(vel[i][j],len(vel[i][j])-1)
                print(len(vel[i][j]))

        for l in xrange(0, len(time_vel[i][j])):
            m=len(time_vel[i][j])-l-1
            n=vel[i][j][m]
            if n>0.2:
                break
        vel[i][j]=np.delete(vel[i][j],xrange(m,len(vel[i][j])))
        time_vel[i][j]=np.delete(time_vel[i][j],xrange(m,len(time_vel[i][j])))
        x[i][j]=np.delete(x[i][j],xrange(m,len(x[i][j])))
        y[i][j]=np.delete(y[i][j],xrange(m,len(y[i][j])))
        fX[i][j]=np.delete(fX[i][j],xrange(m,len(fX[i][j])))
        fY[i][j]=np.delete(fY[i][j],xrange(m,len(fY[i][j])))

        for l in xrange(0, len(time_vel[i][j])):
            n=vel[i][j][l]
            if n>0.2:
                break
        vel[i][j]=np.delete(vel[i][j],xrange(0,l))
        time_vel[i][j]=np.delete(time_vel[i][j],xrange(0,l))
        x[i][j]=np.delete(x[i][j],xrange(0,l))
        y[i][j]=np.delete(y[i][j],xrange(0,l))
        xvalues[i][j]=np.delete(xvalues[i][j],xrange(0,l))
        yvalues[i][j]=np.delete(yvalues[i][j],xrange(0,l))
        fX[i][j]=np.delete(fX[i][j],xrange(0,l))
        fY[i][j]=np.delete(fY[i][j],xrange(0,l))

    #plt.figure()
    #plt.plot(time_vel[i][0],vel[i][0],time_vel[i][1],vel[i][1],time_vel[i][2],vel[i][2])

#__________Mean_Trajectory________________________

for i in xrange(0,len(file_paths)):

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

"""#Displaying original (unfiltered) trjectory paths
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

#__________Variance_Ellipses______________________
fig4=plt.figure(4)
plt.xlim(0, 4.5)
plt.ylim(0, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
fig4.suptitle('C01 Trajectories - Blindfolded')

variability=[]

for i in xrange(0,len(file_paths)):
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i)
    variability.append(a)
        
plt.plot(meanX[0],meanY[0],label='C3N_S_vert_BF')
plt.plot(meanX[1],meanY[1],label='C4N_L_bleu_BF')
plt.plot(meanX[2],meanY[2],label='C4N_R_rouge_BF')
traj1=plt.plot(fX[0][0],fY[0][0],fX[0][1],fY[0][1],fX[0][2],fY[0][2])
traj2=plt.plot(fX[1][0],fY[1][0],fX[1][1],fY[1][1],fX[1][2],fY[1][2])
traj3=plt.plot(fX[2][0],fY[2][0],fX[2][1],fY[2][1],fX[2][2],fY[2][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper right')
fig4.savefig("/home/cuebong/git/cri4/Variance_Plots/27_10_14/C01_trajectory_BF.eps")

fig5=plt.figure(5)
plt.plot(sample[0],variability[0],label='C2N_S_vert_BF')
plt.plot(sample[1],variability[1],label='C4N_L_bleu_BF')
plt.plot(sample[2],variability[2],label='C4N_R_rouge_BF')
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig5.suptitle('C01 Variance Profile - Blindedfolded')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
fig5.savefig("/home/cuebong/git/cri4/Variance_Plots/27_10_14/C01_Variability_profile_BF.eps")
