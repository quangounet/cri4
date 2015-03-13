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
from ANOVA import ANOVA
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
pc='P04'
pc1='C05'
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
#file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))
#file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc))

file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
#file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))
#file_paths.append(get_filepaths("/home/cuebong/git/cri4/data_8_10_14/"+pc1))

use_files,nf,meanX,meanY,sample,Xax,Yax=[],[],[],[],[],[],[]
MPX,MPY,MPZ,time,x,y,xvalues,yvalues=[],[],[],[],[],[],[],[]
fX,fY,time_vel,vel_x,vel_y,vel=[],[],[],[],[],[]

for i in xrange(0,len(file_paths)):
    use_files.append([])
    for j in xrange(0,len(file_paths[i])):
    	filename=file_paths[i][j]
    	if i==0 or i==14:
            target='C4E_R_rouge_VF_'
	elif i==1 or i==15:
            target='C4N_R_rouge_VF_'
        elif i==2 or i==16:
            target='C4S_R_rouge_VF_'
	elif i==3 or i==17:
            target='C4W_R_rouge_VF_'
        elif i==4 or i==18:
            target='C4E_R_rouge_BF_'
	elif i==5 or i==19:
            target='C4N_R_rouge_BF_'
        elif i==6 or i==20:
            target='C4S_R_rouge_BF_'
	elif i==7 or i==21:
            target='C4W_R_rouge_BF_'
        elif i==8 or i==22:
            target='C5E_R_rouge_VF_'
	elif i==9 or i==23:
            target='C5S_R_rouge_VF_'
        elif i==10 or i==24:
            target='C5W_R_rouge_VF_'
	elif i==11 or i==25:
            target='C5E_R_rouge_BF_'
        elif i==12 or i==26:
            target='C5S_R_rouge_BF_'
	elif i==13 or i==27:
            target='C5W_R_rouge_BF_'
       # elif i==14 or i==30:
     #       target='C5S_L_bleu_BF_'
    #    else:
     #       target='C5W_L_bleu_BF_'

    	if target in filename:
       		use_files[i].append(filename)
    if len(use_files[i])!=3:
	sys.exit("Error: not enough datasets",i)

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

for i in xrange(0,28):###################################################
    a=variance_ellipse(sample[i],Xax[i][0],Xax[i][1],Xax[i][2],Yax[i][0],Yax[i][1],Yax[i][2],i)
    variability.append(a)
        
plt.plot(meanX[0],meanY[0],label='C4E_L_bleu_VF',color='b')
plt.plot(meanX[1],meanY[1],label='C4N_L_bleu_VF',color='g')
plt.plot(meanX[2],meanY[2],label='C4S_L_bleu_VF',color='r')
plt.plot(meanX[3],meanY[3],label='C4W_L_bleu_VF',color='k')######################################
traj1=plt.plot(fX[0][0],fY[0][0],fX[0][1],fY[0][1],fX[0][2],fY[0][2])
traj2=plt.plot(fX[1][0],fY[1][0],fX[1][1],fY[1][1],fX[1][2],fY[1][2])
traj3=plt.plot(fX[2][0],fY[2][0],fX[2][1],fY[2][1],fX[2][2],fY[2][2])
traj4=plt.plot(fX[3][0],fY[3][0],fX[3][1],fY[3][1],fX[3][2],fY[3][2])#######################################
plt.setp(traj1,linestyle='--')
plt.setp(traj2,linestyle='--')
plt.setp(traj3,linestyle='--')
plt.setp(traj4,linestyle='--')#############################################
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper right')
fig4.suptitle(pc+'Trajectories-Visual Forward')
#fig4.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_S_vert_trajectories_BF.eps")

fig5=plt.figure(5)
plt.plot(sample[0],variability[0],label='C4E_L_bleu_VF',color='b')
plt.plot(sample[1],variability[1],label='C4N_L_bleu_VF',color='g')
plt.plot(sample[2],variability[2],label='C4S_L_bleu_VF',color='r')
plt.plot(sample[3],variability[3],label='C4W_L_bleu_VF',color='k')##################################
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig5.suptitle(pc+'Variance Profile-Blindfolded')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
#fig5.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_S_vert_Variability_profile_BF.eps")



fig6=plt.figure(6)
plt.xlim(0, 4.5)
plt.ylim(0, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
	

plt.plot(meanX[4],meanY[4],label='C4E_L_bleu_BF',color='b')
plt.plot(meanX[5],meanY[5],label='C4N_L_bleu_BF',color='g')
plt.plot(meanX[6],meanY[6],label='C4S_L_bleu_BF',color='r')
plt.plot(meanX[7],meanY[7],label='C4W_L_bleu_BF',color='k')############################
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
fig6.suptitle(pc+'Trajectories-Blindfolded')
#fig4.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_S_vert_trajectories_BF.eps")

fig7=plt.figure(7)
plt.plot(sample[4],variability[4],label='C4E_L_bleu_BF',color='b')
plt.plot(sample[5],variability[5],label='C4N_L_bleu_BF',color='g')
plt.plot(sample[6],variability[6],label='C4S_L_bleu_BF',color='r')
plt.plot(sample[7],variability[7],label='C4W_L_bleu_BF',color='k')############################
plt.xlim(0, 1)
plt.ylim(0, 2.5)
plt.xlabel('Time')
plt.ylabel('Variability')
fig5.suptitle(pc+'Variance Profile-Blindfolded')
params = {'legend.fontsize': 8,
          'legend.linewidth': 2}
plt.rcParams.update(params)
plt.legend(loc='upper left')
#fig5.savefig("/home/cuebong/git/cri4/Variance_Plots/31_10_14/"+pc+"_S_vert_Variability_profile_BF.eps")

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
for i in xrange(0,4):##########
    resampled_meanX1.append([])
    resampled_meanX2.append([])
    resampled_meanY1.append([])
    resampled_meanY2.append([])
    mean_diff.append([])
    j=i+4########################
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

for l in xrange(4,8):##################
    resampled_meanX1.append([])
    resampled_meanX2.append([])
    resampled_meanY1.append([])
    resampled_meanY2.append([])
    mean_diff.append([])
    i=l+4###############
    j=i+4###############
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


for l in xrange(8,11):##########
    resampled_meanX1.append([])
    resampled_meanX2.append([])
    resampled_meanY1.append([])
    resampled_meanY2.append([])
    mean_diff.append([])
    i=l+8##################
    j=i+3#################
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

for l in xrange(11,14):#############
    resampled_meanX1.append([])
    resampled_meanX2.append([])
    resampled_meanY1.append([])
    resampled_meanY2.append([])
    mean_diff.append([])
    i=l+11############
    j=i+3#################
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
patientVF=[]
controlVF=[]
patientBF=[]
controlBF=[]
patientMTS=[]
controlMTS=[]

for i in xrange(0,4):##############
    VF_Var.append(max(variability[i]))
    BF_Var.append(max(variability[i+4]))
    VFBF_Var.append(max(mean_diff[i]))

for l in xrange(4,8):##############
    i=l+4################
    VF_Var.append(max(variability[i]))
    BF_Var.append(max(variability[i+4]))
    VFBF_Var.append(max(mean_diff[l]))

for l in xrange(8,11):############
    i=l+8#################
    VF_Var.append(max(variability[i]))
    BF_Var.append(max(variability[i+3]))
    VFBF_Var.append(max(mean_diff[l]))

for l in xrange(11,14):############
    i=l+11##########
    VF_Var.append(max(variability[i]))
    BF_Var.append(max(variability[i+3]))
    VFBF_Var.append(max(mean_diff[l]))

for i in xrange(0,7):################
    patientVF.append(VF_Var[i])
    patientBF.append(BF_Var[i])
    patientMTS.append(VFBF_Var[i])
    controlVF.append(VF_Var[i+7])
    controlBF.append(BF_Var[i+7])
    controlMTS.append(VFBF_Var[i+7])##################

N=14 
ind=np.arange(N)+1
width=0.3
fig, ax=plt.subplots()
VF_bar=ax.bar(ind,VF_Var,width,color='b')
BF_bar=ax.bar(ind+width,BF_Var,width,color='g')
VFBF_bar=ax.bar(ind+width+width,VFBF_Var,width,color='r')

ax.set_ylabel('Max Variance')
ax.set_ylim(0,2.5)
ax.set_title(pc+'/'+pc1+'-Maximum Variance across Trajectories-R_rouge')##########################
ax.set_xlabel('Target')
ax.set_xticks(ind+1.5*width)
ax.set_xticklabels(('PC4E','PC4N','PC4S','PC4W','PC5E','PC5S','PC5W','CC4E','CC4N','CC4S','CC4W','CC5E','CC5S','CC5W'))
ax.legend((VF_bar[0],BF_bar[0],VFBF_bar[0]),('MTD-VF','MTD-BF','MTS'),loc='upper left')

N2=7
ind2=np.arange(N2)+1
width2=0.4
fig,ax=plt.subplots()
pVF=ax.bar(ind2,patientVF,width2,color='b')
cVF=ax.bar(ind2+width2,controlVF,width2,color='g')
ax.set_ylabel('Max Variance')
ax.set_ylim(0,2.5)
ax.set_title(pc+'/'+pc1+'-Maximum Variance-R_rouge-VF')#########################
ax.set_xlabel('Target')
ax.set_xticks(ind2+width2)
ax.set_xticklabels(('C4E','C4N','C4S','C4W','C5E','C5S','C5W'))
ax.legend((pVF[0],cVF[0]),('MTD-patient','MTD-control'),loc='upper left')

N3=7
ind3=np.arange(N3)+1
width3=0.4
fig,ax=plt.subplots()
pBF=ax.bar(ind3,patientBF,width3,color='b')
cBF=ax.bar(ind3+width3,controlBF,width3,color='g')
ax.set_ylabel('Max Variance')
ax.set_ylim(0,2.5)
ax.set_title(pc+'/'+pc1+'-Maximum Variance-R_rouge-BF')################################
ax.set_xlabel('Target')
ax.set_xticks(ind3+width3)
ax.set_xticklabels(('C4E','C4N','C4S','C4W','C5E','C5S','C5W'))
ax.legend((pBF[0],cBF[0]),('MTD-patient','MTD-control'),loc='upper left')

N4=7
ind4=np.arange(N4)+1
width4=0.4
fig,ax=plt.subplots()
pMTS=ax.bar(ind4,patientMTS,width4,color='b')
cMTS=ax.bar(ind4+width4,controlMTS,width4,color='g')
ax.set_ylabel('Max Variance')
ax.set_ylim(0,2.5)
ax.set_title(pc+'/'+pc1+'-Maximum Variance-R_rouge-MTS')################################
ax.set_xlabel('Target')
ax.set_xticks(ind4+width4)
ax.set_xticklabels(('C4E','C4N','C4S','C4W','C5E','C5S','C5W'))
ax.legend((pMTS[0],cMTS[0]),('MTD-patient','MTD-control'),loc='upper left')

MTD_Data=[]
MTD_Data.append([])
MTD_Data.append([])
MTD_Data[0].append([])
MTD_Data[0].append([])
MTD_Data[1].append([])
MTD_Data[1].append([])

for i in xrange(0,6):
    MTD_Data[0][0].append(VF_Var[i])
    MTD_Data[0][1].append(BF_Var[i])
    MTD_Data[1][0].append(VF_Var[i+6])
    MTD_Data[1][1].append(BF_Var[i+6])

Fscore,DoF=ANOVA(MTD_Data)
print(MTD_Data)
print(Fscore,DoF)

