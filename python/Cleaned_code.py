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
pc='C05'
plt.xlabel('Sample Number')
plt.ylabel('X/Y Axis')
fig1.suptitle('X/Y Trajectories')

file_paths=[]
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
use_files,nf,meanX,meanY,sample,Xax,Yax=[],[],[],[],[],[],[]
MPX,MPY,MPZ,time,x,y,xvalues,yvalues=[],[],[],[],[],[],[],[]
fX,fY,time_vel,vel_x,vel_y,vel=[],[],[],[],[],[]

for i in xrange(0,len(file_paths)):
    use_files.append([])
    for j in xrange(0,len(file_paths[i])):
    	filename=file_paths[i][j]
    	if i==0:
            target='C4E_R_rouge_VF_'
	elif i==1:
            target='C4N_R_rouge_VF_'
        elif i==2:
            target='C4S_R_rouge_VF_'
	elif i==3:
            target='C4W_R_rouge_VF_'
        elif i==4:
            target='C4E_R_rouge_BF_'
	elif i==5:
            target='C4N_R_rouge_BF_'
        elif i==6:
            target='C4S_R_rouge_BF_'
	elif i==7:
            target='C4W_R_rouge_BF_'
        elif i==8:
            target='C5E_R_rouge_VF_'
	elif i==9:
            target='C5N_R_rouge_VF_'
        elif i==10:
            target='C5S_R_rouge_VF_'
	elif i==11:
            target='C5W_R_rouge_VF_'
        elif i==12:
            target='C5E_R_rouge_BF_'
	elif i==13:
            target='C5N_R_rouge_BF_'
        elif i==14:
            target='C5S_R_rouge_BF_'
        elif i==15:
            target='C5W_R_rouge_BF_'
        elif i==16:
            target='C1N_S_vert_VF_'
	elif i==17:
            target='C2N_S_vert_VF_'
        elif i==18:
            target='C3N_S_vert_VF_'
	elif i==19:
            target='C1N_S_vert_BF_'
        elif i==20:
            target='C2N_S_vert_BF_'
        else:
            target='C3N_S_vert_BF_'

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


variability=[]

for i in xrange(0,4):
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i)
    variability.append(a)
        
plt.plot(meanX[0],meanY[0],label='C4E_R_rouge_VF',color='b')
plt.plot(meanX[1],meanY[1],label='C4N_R_rouge_VF',color='g')
plt.plot(meanX[2],meanY[2],label='C4S_R_rouge_VF',color='r')
plt.plot(meanX[3],meanY[3],label='C4W_R_rouge_VF',color='k')
traj1=plt.plot(fX[0][0],fY[0][0],fX[0][1],fY[0][1],fX[0][2],fY[0][2])
traj2=plt.plot(fX[1][0],fY[1][0],fX[1][1],fY[1][1],fX[1][2],fY[1][2])
traj3=plt.plot(fX[2][0],fY[2][0],fX[2][1],fY[2][1],fX[2][2],fY[2][2])
traj4=plt.plot(fX[3][0],fY[3][0],fX[3][1],fY[3][1],fX[3][2],fY[3][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
plt.setp(traj4,linestyle='--')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper right')
fig4.suptitle(pc+'-C4-R_rouge-Trajectories-Visual Forward')
fig4.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_C4_R_rouge_trajectories_VF.eps")

fig5=plt.figure(5)
plt.plot(sample[0],variability[0],label='C4E_R_rouge_VF',color='b')
plt.plot(sample[1],variability[1],label='C4N_R_rouge_VF',color='g')
plt.plot(sample[2],variability[2],label='C4S_R_rouge_VF',color='r')
plt.plot(sample[3],variability[3],label='C4W_R_rouge_VF',color='k')
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig5.suptitle(pc+'-C4-R_rouge-Variance Profile-Visual Forward')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
fig5.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_C4_R_rouge_Variability_profile_VF.eps")

fig6=plt.figure(6)
plt.xlim(0, 4.5)
plt.ylim(0, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

for i in xrange(4,8):
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i-4)
    variability.append(a)
	
plt.plot(meanX[4],meanY[4],label='C4E_R_rouge_BF',color='b')
plt.plot(meanX[5],meanY[5],label='C4N_R_rouge_BF',color='g')
plt.plot(meanX[6],meanY[6],label='C4S_R_rouge_BF',color='r')
plt.plot(meanX[7],meanY[7],label='C4W_R_rouge_BF',color='k')
traj1=plt.plot(fX[4][0],fY[4][0],fX[4][1],fY[4][1],fX[4][2],fY[4][2])
traj2=plt.plot(fX[5][0],fY[5][0],fX[5][1],fY[5][1],fX[5][2],fY[5][2])
traj3=plt.plot(fX[6][0],fY[6][0],fX[6][1],fY[6][1],fX[6][2],fY[6][2])
traj4=plt.plot(fX[7][0],fY[7][0],fX[7][1],fY[7][1],fX[7][2],fY[7][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
plt.setp(traj4,linestyle='--')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper right')
fig6.suptitle(pc+'-C4-R_rouge-Trajectories-Blindfolded')
fig6.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_C4_R_rouge_trajectories_BF.eps")

fig7=plt.figure(7)
plt.plot(sample[4],variability[4],label='C4E_R_rouge_BF',color='b')
plt.plot(sample[5],variability[5],label='C4N_R_rouge_BF',color='g')
plt.plot(sample[6],variability[6],label='C4S_R_rouge_BF',color='r')
plt.plot(sample[7],variability[7],label='C4W_R_rouge_BF',color='k')
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig7.suptitle(pc+'-C4_R_rouge-Variance Profile-Blindfolded')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
fig7.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_C4_R_rouge_Variability_profile_BF.eps")

fig8=plt.figure(8)
plt.xlim(0, 4.5)
plt.ylim(0, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

for i in xrange(8,12):
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i-8)
    variability.append(a)
        
plt.plot(meanX[8],meanY[8],label='C5E_R_rouge_VF',color='b')
plt.plot(meanX[9],meanY[9],label='C5N_R_rouge_VF',color='g')
plt.plot(meanX[10],meanY[10],label='C5S_R_rouge_VF',color='r')
plt.plot(meanX[11],meanY[11],label='C5W_R_rouge_VF',color='k')
traj1=plt.plot(fX[8][0],fY[8][0],fX[8][1],fY[8][1],fX[8][2],fY[8][2])
traj2=plt.plot(fX[9][0],fY[9][0],fX[9][1],fY[9][1],fX[9][2],fY[9][2])
traj3=plt.plot(fX[10][0],fY[10][0],fX[10][1],fY[10][1],fX[10][2],fY[10][2])
traj4=plt.plot(fX[11][0],fY[11][0],fX[11][1],fY[11][1],fX[11][2],fY[11][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
plt.setp(traj4,linestyle='--')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper right')
fig8.suptitle(pc+'-C5-R_rouge-Trajectories-Visual Forward')
fig8.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_C5_R_rouge_trajectories_VF.eps")

fig9=plt.figure(9)
plt.plot(sample[8],variability[8],label='C5E_R_rouge_VF',color='b')
plt.plot(sample[9],variability[9],label='C5N_R_rouge_VF',color='g')
plt.plot(sample[10],variability[10],label='C5S_R_rouge_VF',color='r')
plt.plot(sample[11],variability[11],label='C5W_R_rouge_VF',color='k')
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig9.suptitle(pc+'-C5-R_rouge-Variance Profile-Visual Forward')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
fig9.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_C5_R_rouge_Variability_profile_VF.eps")

fig10=plt.figure(10)
plt.xlim(0, 4.5)
plt.ylim(0, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

for i in xrange(12,16):
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i-12)
    variability.append(a)
	
plt.plot(meanX[12],meanY[12],label='C5E_R_rouge_BF',color='b')
plt.plot(meanX[13],meanY[13],label='C5N_R_rouge_BF',color='g')
plt.plot(meanX[14],meanY[14],label='C5S_R_rouge_BF',color='r')
plt.plot(meanX[15],meanY[15],label='C5W_R_rouge_BF',color='k')
traj1=plt.plot(fX[12][0],fY[12][0],fX[12][1],fY[12][1],fX[12][2],fY[12][2])
traj2=plt.plot(fX[13][0],fY[13][0],fX[13][1],fY[13][1],fX[13][2],fY[13][2])
traj3=plt.plot(fX[14][0],fY[14][0],fX[14][1],fY[14][1],fX[14][2],fY[14][2])
traj4=plt.plot(fX[15][0],fY[15][0],fX[15][1],fY[15][1],fX[15][2],fY[15][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
plt.setp(traj4,linestyle='--')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper right')
fig10.suptitle(pc+'-C5-R_rouge-Trajectories-Blindfolded')
fig10.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_C5_R_rouge_trajectories_BF.eps")

fig11=plt.figure(11)
plt.plot(sample[12],variability[12],label='C5E_R_rouge_BF',color='b')
plt.plot(sample[13],variability[13],label='C5N_R_rouge_BF',color='g')
plt.plot(sample[14],variability[14],label='C5S_R_rouge_BF',color='r')
plt.plot(sample[15],variability[15],label='C5W_R_rouge_BF',color='k')
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig11.suptitle(pc+'-C5_R_rouge-Variance Profile-Blindfolded')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
fig11.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_C5_R_rouge_Variability_profile_BF.eps")

fig12=plt.figure(12)
plt.xlim(0, 4.5)
plt.ylim(0, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

for i in xrange(16,19):
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i-16)
    variability.append(a)
	
plt.plot(meanX[16],meanY[16],label='C1N_S_vert_VF',color='b')
plt.plot(meanX[17],meanY[17],label='C2N_S_vert_VF',color='g')
plt.plot(meanX[18],meanY[18],label='C3N_S_vert_VF',color='r')
traj1=plt.plot(fX[16][0],fY[16][0],fX[16][1],fY[16][1],fX[16][2],fY[16][2])
traj2=plt.plot(fX[17][0],fY[17][0],fX[17][1],fY[17][1],fX[17][2],fY[17][2])
traj3=plt.plot(fX[18][0],fY[18][0],fX[18][1],fY[18][1],fX[18][2],fY[18][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper right')
fig12.suptitle(pc+'-S_vert-Trajectories-Visual Forward')
fig12.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_S_vert_trajectories_VF.eps")

fig13=plt.figure(13)
plt.plot(sample[16],variability[16],label='C1N_S_vert_VF',color='b')
plt.plot(sample[17],variability[17],label='C2N_S_vert_VF',color='g')
plt.plot(sample[18],variability[18],label='C3N_S_vert_VF',color='r')
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig13.suptitle(pc+'-S_vert-Variance Profile-Visual Forward')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
fig13.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_S_vert_Variability_profile_VF.eps")

fig14=plt.figure(14)
plt.xlim(0, 4.5)
plt.ylim(0, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

for i in xrange(19,22):
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i-19)
    variability.append(a)
	
plt.plot(meanX[19],meanY[19],label='C1N_S_vert_BF',color='b')
plt.plot(meanX[20],meanY[20],label='C2N_S_vert_BF',color='g')
plt.plot(meanX[21],meanY[21],label='C3N_S_vert_BF',color='r')
traj1=plt.plot(fX[19][0],fY[19][0],fX[19][1],fY[19][1],fX[19][2],fY[19][2])
traj2=plt.plot(fX[20][0],fY[20][0],fX[20][1],fY[20][1],fX[20][2],fY[20][2])
traj3=plt.plot(fX[21][0],fY[21][0],fX[21][1],fY[21][1],fX[21][2],fY[21][2])
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper right')
fig14.suptitle(pc+'-S_vert-Trajectories-Blindfolded')
fig14.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_S_vert_trajectories_BF.eps")

fig15=plt.figure(15)
plt.plot(sample[19],variability[19],label='C1N_S_vert_BF',color='b')
plt.plot(sample[20],variability[20],label='C2N_S_vert_BF',color='g')
plt.plot(sample[21],variability[21],label='C3N_S_vert_BF',color='r')
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig15.suptitle(pc+'-S_vert-Variance Profile-Blindfolded')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
fig15.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_S_vert_Variability_profile_BF.eps")

"""
fig12=plt.figure(12)

meanVarxinterp,meanVaryinterp,meanVarX,meanVarY,mean_diff=[],[],[],[],[]

for i in xrange(0,len(meanX)):
    a,b,c,d,e=perform_spline(meanX[i],meanY[i])
    meanVarxinterp.append(b)
    meanVaryinterp.append(c)
    meanVarX.append(d)
    meanVarY.append(e)

plt.close(12)
fig13=plt.figure(13)
resampled_meanX1,resampled_meanX2,resampled_meanY1,resampled_meanY2=[],[],[],[]
mean_diff=[]
intersubject_time=[]
for i in xrange(0,4):
    resampled_meanX1.append([])
    resampled_meanX2.append([])
    resampled_meanY1.append([])
    resampled_meanY2.append([])
    mean_diff.append([])
    j=i+4
    if len(sample[i])>len(sample[j]):
        intersubject_time.append(sample[j])
    else:
        intersubject_time.append(sample[i])
    for k in xrange(0,len(intersubject_time[i])):
        resampled_meanX1[i].append(meanVarX[i][intersubject_time[i][k]*len(meanVarxinterp[i])])
        resampled_meanX2[i].append(meanVarX[j][intersubject_time[i][k]*len(meanVarxinterp[j])])
        resampled_meanY1[i].append(meanVarX[i][intersubject_time[i][k]*len(meanVaryinterp[i])])
        resampled_meanY2[i].append(meanVarX[j][intersubject_time[i][k]*len(meanVaryinterp[j])])
    
    for l in xrange(0,len(intersubject_time[i])):
        diffX=resampled_meanX1[i][l]-resampled_meanX2[i][l]
        diffY=resampled_meanY1[i][l]-resampled_meanY2[i][l]
        mean_diff[i].append(sqrt(diffX*diffX+diffY*diffY))

for l in xrange(4,8):
    resampled_meanX1.append([])
    resampled_meanX2.append([])
    resampled_meanY1.append([])
    resampled_meanY2.append([])
    mean_diff.append([])
    i=l+4
    j=i+4
    if len(sample[i])>len(sample[j]):
        intersubject_time.append(sample[j])
    else:
        intersubject_time.append(sample[i])
    for k in xrange(0,len(intersubject_time[l])):
        resampled_meanX1[l].append(meanVarX[i][intersubject_time[l][k]*len(meanVarxinterp[i])])
        resampled_meanX2[l].append(meanVarX[j][intersubject_time[l][k]*len(meanVarxinterp[j])])
        resampled_meanY1[l].append(meanVarX[i][intersubject_time[l][k]*len(meanVaryinterp[i])])
        resampled_meanY2[l].append(meanVarX[j][intersubject_time[l][k]*len(meanVaryinterp[j])])
    
    for m in xrange(0,len(intersubject_time[l])):
        diffX=resampled_meanX1[l][m]-resampled_meanX2[l][m]
        diffY=resampled_meanY1[l][m]-resampled_meanY2[l][m]
        mean_diff[l].append(sqrt(diffX*diffX+diffY*diffY))

for l in xrange(8,11):
    resampled_meanX1.append([])
    resampled_meanX2.append([])
    resampled_meanY1.append([])
    resampled_meanY2.append([])
    mean_diff.append([])
    i=l+8
    j=i+3
    if len(sample[i])>len(sample[j]):
        intersubject_time.append(sample[j])
    else:
        intersubject_time.append(sample[i])
    for k in xrange(0,len(intersubject_time[l])):
        resampled_meanX1[l].append(meanVarX[i][intersubject_time[l][k]*len(meanVarxinterp[i])])
        resampled_meanX2[l].append(meanVarX[j][intersubject_time[l][k]*len(meanVarxinterp[j])])
        resampled_meanY1[l].append(meanVarX[i][intersubject_time[l][k]*len(meanVaryinterp[i])])
        resampled_meanY2[l].append(meanVarX[j][intersubject_time[l][k]*len(meanVaryinterp[j])])
    
    for m in xrange(0,len(intersubject_time[l])):
        diffX=resampled_meanX1[l][m]-resampled_meanX2[l][m]
        diffY=resampled_meanY1[l][m]-resampled_meanY2[l][m]
        mean_diff[l].append(sqrt(diffX*diffX+diffY*diffY))

#plt.plot(intersubject_time[0],mean_diff[0],label='C4E_L_bleu', color='b')
#plt.plot(intersubject_time[1],mean_diff[1],label='C4N_L_bleu', color='g')
#plt.plot(intersubject_time[2],mean_diff[2],label='C4S_L_bleu', color='r')
#plt.plot(intersubject_time[3],mean_diff[3],label='C4W_L_bleu', color='k')
#plt.xlim(0, 1)
#plt.ylim(0, 2.5)
#plt.xlabel('Time')
#plt.ylabel('Deviation')
#fig13.suptitle(pc+'BF-VF Trajectory Deviations')
#params = {'legend.fontsize': 8,
#          'legend.linewidth': 2}
#plt.rcParams.update(params)
#plt.legend(loc='upper left')


VF_Var=[]
BF_Var=[]
VFBF_Var=[]

for i in xrange(0,4):
    VF_Var.append(max(variability[i]))
    BF_Var.append(max(variability[i+4]))
    VFBF_Var.append(max(mean_diff[i]))

for l in xrange(4,8):
    i=l+4
    VF_Var.append(max(variability[i]))
    BF_Var.append(max(variability[i+4]))
    VFBF_Var.append(max(mean_diff[l]))

for l in xrange(8,11):
    i=l+8
    VF_Var.append(max(variability[i]))
    BF_Var.append(max(variability[i+3]))
    VFBF_Var.append(max(mean_diff[l]))

N=11
ind=np.arange(N)+1
width=0.3
fig, ax=plt.subplots()
VF_bar=ax.bar(ind,VF_Var,width,color='b')
BF_bar=ax.bar(ind+width,BF_Var,width,color='g')
VFBF_bar=ax.bar(ind+width+width,VFBF_Var,width,color='r')

ax.set_ylabel('Max Variance')
ax.set_title(pc+'Maximum Variance across Trajectories')
ax.set_xlabel('Target')
ax.set_xticks(ind+1.5*width)
ax.set_xticklabels(('C4E','C4N','C4S','C4W','C5E','C5N','C5S','C5W','C1N','C2N','C3N'))

ax.legend((VF_bar[0],BF_bar[0],VFBF_bar[0]),('MTD-VF','MTD-BF','MTS'))
"""
