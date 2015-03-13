from extract_midpoint import data
from derivative import *
from perform_splines import perform_spline
from perform_splines import perform_spline2
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
from mean_traj import mean_calc2
from ANOVA import ANOVA
from t_test import T_test
from variance_ellipse_new2 import variance_ellipse
from variance_ellipse_new2 import variance_ellipse2
from variance_ellipse_new2 import variance_ellipse_2
from variance_ellipse_new2 import variance_ellipse2_2
from butter_filter import butter_lowpass, butter_lowpass_filter
from collections import defaultdict
import csv 

fs=120
lowcut=1
lowcutpat=0.4
lowcutextrapat=0.35
lowcuthipat=0.30
filterpat=[12,19]
extrafilterpat=16
hifilterpat=[13,17,18]
velcuthi=[0,1,2,3,7,8,9,10,11]
velcutmed=[4,5,6,14,16,18]
velcutlow=[12,15,19]

def resultant_profile(x,y):
        val=[]
        for j in xrange(0,len(x)):
            x_term=x[j]*x[j]
            y_term=y[j]*y[j]
            a=(x_term+y_term)**0.5
            val.append(a)
        return val

plt.ion()
subjects=['C01','C03','C04','C05','C07','C06','C08','C09','C10','C11','P01','P02','P03','P04','P05','P06','P07','P08','P09','P10']
target_list=['C4E_L_bleu_VF','C4N_L_bleu_VF','C4S_L_bleu_VF','C4W_L_bleu_VF','C4E_L_bleu_BF','C4N_L_bleu_BF','C4S_L_bleu_BF','C4W_L_bleu_BF','C5E_L_bleu_VF','C5N_L_bleu_VF','C5S_L_bleu_VF','C5W_L_bleu_VF','C5E_L_bleu_BF','C5N_L_bleu_BF','C5S_L_bleu_BF','C5W_L_bleu_BF','C4E_R_rouge_VF','C4N_R_rouge_VF','C4S_R_rouge_VF','C4W_R_rouge_VF','C4E_R_rouge_BF','C4N_R_rouge_BF','C4S_R_rouge_BF','C4W_R_rouge_BF','C5E_R_rouge_VF','C5N_R_rouge_VF','C5S_R_rouge_VF','C5W_R_rouge_VF','C5E_R_rouge_BF','C5N_R_rouge_BF','C5S_R_rouge_BF','C5W_R_rouge_BF','C1N_S_vert_VF','C1N_S_vert_BF','C2N_S_vert_VF','C2N_S_vert_BF','C3N_S_vert_VF','C3N_S_vert_BF']

RheelX=[]
RheelY=[]
RheelZ=[]
LheelX=[]
LheelY=[]
LheelZ=[]
Rstepnumber=[]
Lstepnumber=[]
Rsubjectstepvel=[0.5,0.5,0.5,0.3,0.4,0.4,0.5,0.5,0.4,0.3,0.4,0.4,0.1,0.1,0.4,0.3,0.3,-0.1,0.4,0.5]
Lsubjectstepvel=list(Rsubjectstepvel)
Lsteptrial=[[],[],[]]
Rsteptrial=[[],[],[]]
x,y=[],[]
Xax,Yax=[],[]
xvalues,yvalues=[],[]

for j in xrange(0,38):
    for r in xrange(0,3):
        Lsteptrial[r].append([])
        Rsteptrial[r].append([])
for i in xrange(0,20):
    subject=subjects[i]
    file_paths=[]
    use_files=[]
    RheelX.append([])
    RheelY.append([])
    RheelZ.append([])
    LheelX.append([])
    LheelY.append([])
    LheelZ.append([])
    x.append([])
    y.append([])
    Xax.append([])
    Yax.append([])
    xvalues.append([])
    yvalues.append([])
    MPX,MPY,MPZ,shtime=[],[],[],[]
    fX,fY,time_vel,vel_x,vel_y,vel=[],[],[],[],[],[]
    #Rstepnumber.append([])
    #Lstepnumber.append([])
    for j in xrange(0,38):
        file_paths.append(get_filepaths("/home/cuebong/git/cri4/AllData/Post_processedCSV/"+subject))
        use_files.append([])
        plt.figure()
        for k in xrange(0,len(file_paths[j])):
            filename=file_paths[j][k]
            if j==0: 
                target='C4E_L_bleu_VF_'
            elif j==1:
                target='C4N_L_bleu_VF_'
            elif j==2: 
                target='C4S_L_bleu_VF_'
            elif j==3: 
                target='C4W_L_bleu_VF_'
            elif j==4: 
                target='C4E_L_bleu_BF_'
            elif j==5:
                target='C4N_L_bleu_BF_'
            elif j==6: 
                target='C4S_L_bleu_BF_'
            elif j==7: 
                target='C4W_L_bleu_BF_'
            elif j==8: 
                target='C5E_L_bleu_VF_'
            elif j==9: 
                target='C5N_L_bleu_VF_'
            elif j==10:
                target='C5S_L_bleu_VF_'
            elif j==11: 
                target='C5W_L_bleu_VF_'
            elif j==12: 
                target='C5E_L_bleu_BF_'
            elif j==13: 
                target='C5N_L_bleu_BF_'
            elif j==14: 
                target='C5S_L_bleu_BF_'
            elif j==15: 
                target='C5W_L_bleu_BF_'
            elif j==16: 
                target='C4E_R_rouge_VF_'
            elif j==17: 
                target='C4N_R_rouge_VF_'
            elif j==18: 
                target='C4S_R_rouge_VF_'
            elif j==19:
                target='C4W_R_rouge_VF_'
            elif j==20:
                target='C4E_R_rouge_BF_'
            elif j==21:
                target='C4N_R_rouge_BF_'
            elif j==22: 
                target='C4S_R_rouge_BF_'
            elif j==23: 
                target='C4W_R_rouge_BF_'
            elif j==24:
                target='C5E_R_rouge_VF_'
            elif j==25: 
                target='C5N_R_rouge_VF_'
            elif j==26: 
                target='C5S_R_rouge_VF_'
            elif j==27: 
                target='C5W_R_rouge_VF_'
            elif j==28:
                target='C5E_R_rouge_BF_'
            elif j==29: 
                target='C5N_R_rouge_BF_'
            elif j==30:
                target='C5S_R_rouge_BF_'
            elif j==31: 
                target='C5W_R_rouge_BF_'
            elif j==32:
                target='C1N_S_vert_VF_'
            elif j==33:
                target='C1N_S_vert_BF_'
            elif j==34: 
                target='C2N_S_vert_VF_'
            elif j==35:
                target='C2N_S_vert_BF_'
            elif j==36: 
                target='C3N_S_vert_VF_'
            else:
                target='C3N_S_vert_BF_'

            if target in filename:
                use_files[j].append(filename)
        RheelX[i].append([])
        RheelY[i].append([])
        RheelZ[i].append([])
        LheelX[i].append([])
        LheelY[i].append([])
        LheelZ[i].append([])
        x[i].append([])
        y[i].append([])
        xvalues[i].append([])
        yvalues[i].append([])
        Xax[i].append([])
        Yax[i].append([])
        fX.append([])
        fY.append([])
        time_vel.append([])
        vel_x.append([])
        vel_y.append([])
        vel.append([])
        MPX.append([])
        MPY.append([])
        MPZ.append([])
        shtime.append([])
        #Rstepnumber[i].append([])
        #Lstepnumber[i].append([])
        for k in xrange(0,len(use_files[j])):
            with open(use_files[j][k]) as f:
                n=defaultdict(list)
                reader=csv.reader(f)
                for row in reader: #running through each row in csv file
                    for (u,v) in enumerate(row):
                        a=Decimal(v) #converts string to decimal
                        n[u].append(a)

            RShouX=n[15]
            RShouY=n[16]
            RShouZ=n[17]
            LShouX=n[18]
            LShouY=n[19]
            LShouZ=n[20]
            for frame in xrange(0, len(RShouX)):
                MPX[j].append((RShouX[frame]+LShouX[frame])/2)
                MPY[j].append((RShouY[frame]+LShouY[frame])/2)
                MPZ[j].append((RShouZ[frame]+LShouZ[frame])/2)
            RheelX[i][j].append(n[30])
            RheelY[i][j].append(n[31])
            RheelZ[i][j].append(n[32])
            LheelX[i][j].append(n[24])
            LheelY[i][j].append(n[25])
            LheelZ[i][j].append(n[26])
            time=[]
            NoiseRZ=[]
            NoiseLZ=[]
            filteredLheelZ=[]
            filteredRheelZ=[]
            noiseX=[]
            noiseY=[]
            for l in xrange(0,len(MPX[j])):
                noiseX.append(float(MPX[j][l]))
                noiseY.append(float(MPY[j][l]))
            for l in xrange(0,len(RheelZ[i][j][k])):
                NoiseRZ.append(float(RheelZ[i][j][k][l]))
                NoiseLZ.append(float(LheelZ[i][j][k][l]))
            filteredRheelZ.append(butter_lowpass_filter(NoiseRZ,3,120,order=2))
            filteredLheelZ.append(butter_lowpass_filter(NoiseLZ,3,120,order=2))
            length=xrange(0,len(filteredRheelZ[0]))

            if i in filterpat:
                fX[j].append(butter_lowpass_filter(noiseX,lowcutpat,fs,order=2))
                fY[j].append(butter_lowpass_filter(noiseY,lowcutpat,fs,order=2))
            elif i==extrafilterpat:
                fX[j].append(butter_lowpass_filter(noiseX,lowcutextrapat,fs,order=2))
                fY[j].append(butter_lowpass_filter(noiseY,lowcutextrapat,fs,order=2))
            elif i in hifilterpat:
                fX[j].append(butter_lowpass_filter(noiseX,lowcuthipat,fs,order=2))
                fY[j].append(butter_lowpass_filter(noiseY,lowcuthipat,fs,order=2))
            else:
                fX[j].append(butter_lowpass_filter(noiseX,lowcut,fs,order=2))
                fY[j].append(butter_lowpass_filter(noiseY,lowcut,fs,order=2))
            d,e,f,g,h=perform_spline(fX[j][k],fY[j][k])
            shtime[j].append(d)
            x[i][j].append(e)
            y[i][j].append(f)
            xvalues[i][j].append(g)
            yvalues[i][j].append(h)

            for n in length:
                time.append(Decimal(n)/120)

            for l in xrange(0,len(y[i][j][k])):
                n=y[i][j][k][l]
                if n>0.5:
                    break
            x[i][j][k]=np.delete(x[i][j][k],xrange(0,l))
            y[i][j][k]=np.delete(y[i][j][k],xrange(0,l))
            xvalues[i][j][k]=np.delete(xvalues[i][j][k],xrange(0,l))
            yvalues[i][j][k]=np.delete(yvalues[i][j][k],xrange(0,l))
            fX[j][k]=np.delete(fX[j][k],xrange(0,l))
            fY[j][k]=np.delete(fY[j][k],xrange(0,l))
            time=np.delete(time,xrange(0,l))
            filteredRheelZ[0]=np.delete(filteredRheelZ[0],xrange(0,l))
            filteredLheelZ[0]=np.delete(filteredLheelZ[0],xrange(0,l))

            a,b=deriv_vel(x[i][j][k])
            time_vel[j].append(a)
            vel_x[j].append(b)
            a,c=deriv_vel(y[i][j][k])
            vel_y[j].append(c)
            d=resultant_profile(vel_x[j][k],vel_y[j][k])
            vel[j].append(d)

            while len(time_vel[j][k])!=len(vel[j][k]):
                if len(time_vel[j][k])>len(vel[j][k]):
                    time_vel[j][k]=np.delete(time_vel[j][k],len(time_vel[j][k])-1)
                else:
                    vel[j][k]=np.delete(vel[j][k],len(vel[j][k])-1)

            for l in xrange(0,len(time_vel[j][k])):
                n=0
                m=len(time_vel[j][k])-l-1
                n=vel[j][k][m]
                if i==11 and j==37 and n>0.9:
                    break
                if i==11 and j==20 and n>0.7:
                    break
                if i==6 and j==20 and n>0.6:
                    break
                if i==6 and j==5 and n>0.6:
                    break
                if i==19 and j==28 and n>0.62:
                    break
                if i==6 and j==28 and n>0.6:
                    break
                if (i==13 or i==17) and n>0.24:
                    break
                if n>0.4 and ((i!=11 or j!=37) and (i!=11 or j!=20) and (i!=76 or j!=20) and (i!=6 or j!=5) and (i!=19 or j!=28) and (i!=6 or j!=28)) and (i in velcutlow):
                    break
                if n>0.5 and ((i!=11 or j!=37) and (i!=11 or j!=20) and (i!=76 or j!=20) and (i!=6 or j!=5) and (i!=19 or j!=28) and (i!=6 or j!=28)) and (i in velcutmed):
                    break
                if n>0.7 and ((i!=11 or j!=37) and (i!=11 or j!=20) and (i!=76 or j!=20) and (i!=6 or j!=5) and (i!=19 or j!=28) and (i!=6 or j!=28)) and (i in velcuthi):
                    break

            vel[j][k]=np.delete(vel[j][k],xrange(m,len(vel[j][k])))
            time_vel[j][k]=np.delete(time_vel[j][k],xrange(m,len(time_vel[j][k])))
            x[i][j][k]=np.delete(x[i][j][k],xrange(m,len(x[i][j][k])))
            y[i][j][k]=np.delete(y[i][j][k],xrange(m,len(y[i][j][k])))
            xvalues[i][j][k]=np.delete(xvalues[i][j][k],xrange(m,len(xvalues[i][j][k])))
            yvalues[i][j][k]=np.delete(yvalues[i][j][k],xrange(m,len(yvalues[i][j][k])))
            fX[j][k]=np.delete(fX[j][k],xrange(m,len(fX[j][k])))
            fY[j][k]=np.delete(fY[j][k],xrange(m,len(fY[j][k])))
            
            time=np.delete(time, xrange(m,len(time)))
            filteredRheelZ[0]=np.delete(filteredRheelZ[0],xrange(m,len(filteredRheelZ[0])))
            filteredLheelZ[0]=np.delete(filteredLheelZ[0],xrange(m,len(filteredLheelZ[0]))) 

            if k==0:
                linecolor='b'
            elif k==1:
                linecolor='r'
            else: 
                linecolor='g'
            #plt.plot(time,filteredRheelZ[0],color=linecolor)
            Rtraj_time,Rheelpeaks=deriv_vel(filteredRheelZ[0])
            while len(Rtraj_time)!=len(Rheelpeaks):
                if len(Rtraj_time)>len(Rheelpeaks):
                    Rtraj_time=np.delete(Rtraj_time,(len(Rtraj_time)-1))
                else:
                    Rheelpeaks=np.delete(Rheelpeaks,len(Rheelpeaks)-1)
            #plt.plot(Rtraj_time,Rheelpeaks,color=linecolor)
            Ltraj_time,Lheelpeaks=deriv_vel(filteredLheelZ[0])
            while len(Ltraj_time)!=len(Lheelpeaks):
                if len(Ltraj_time)>len(Lheelpeaks):
                    Ltraj_time=np.delete(Ltraj_time,(len(Ltraj_time)-1))
                else:
                    Lheelpeaks=np.delete(Lheelpeaks,len(Lheelpeaks)-1)
            plt.plot(time,filteredLheelZ[0],color=linecolor)        
            plt.plot(Ltraj_time,Lheelpeaks,color=linecolor)
            if i !=17:
                Rhalfstep=0
                Rstepcount=0
                for timeinstant in xrange(0,len(Rtraj_time)):
                    if Rheelpeaks[timeinstant]>Rsubjectstepvel[i]:
                        Rhalfstep=1
                    if Rheelpeaks[timeinstant]<Rsubjectstepvel[i] and Rhalfstep==1:
                        Rstepcount=Rstepcount+1
                        Rhalfstep=0
                #Rstepnumber[i][j].append(Rstepcount)
                Rsteptrial[k][j].append(Rstepcount)

                Lhalfstep=0
                Lstepcount=0
                for timeinstant in xrange(0,len(Ltraj_time)):
                    if Lheelpeaks[timeinstant]>Lsubjectstepvel[i]:
                        Lhalfstep=1
                    if Lheelpeaks[timeinstant]<Lsubjectstepvel[i] and Lhalfstep==1:
                        Lstepcount=Lstepcount+1
                        Lhalfstep=0
                #Lstepnumber[i][j].append(Lstepcount)
                Lsteptrial[k][j].append(Lstepcount)

            else:
                Rhalfstep=0
                Rstepcount=0
                for timeinstant in xrange(0,len(Rtraj_time)):
                    if Rheelpeaks[timeinstant]<Rsubjectstepvel[i]:
                        Rhalfstep=1
                    if Rheelpeaks[timeinstant]>Rsubjectstepvel[i] and Rhalfstep==1:
                        Rstepcount=Rstepcount+1
                        Rhalfstep=0
                #Rstepnumber[i][j].append(Rstepcount)
                Rsteptrial[k][j].append(Rstepcount)
                
                Lhalfstep=0
                Lstepcount=0
                for timeinstant in xrange(0,len(Ltraj_time)):
                    if Lheelpeaks[timeinstant]<Lsubjectstepvel[i]:
                        Lhalfstep=1
                    if Lheelpeaks[timeinstant]>Lsubjectstepvel[i] and Lhalfstep==1:
                        Lstepcount=Lstepcount+1
                        Lhalfstep=0
                #Lstepnumber[i][j].append(Lstepcount)      
                Lsteptrial[k][j].append(Lstepcount)
        plt.savefig("/home/cuebong/git/cri4/Stepping motion/Lheel/"+subject+"_"+target_list[j]+".jpg")
        plt.close()

for r in xrange(0,3):
    for j in xrange(0,38):
        Rstepnumbertrialcsv="/home/cuebong/git/cri4/Stepping motion/step_number/Right/Rstep_number_"+target_list[j]+"_trial_"+str(r+1)+".csv"
        with open(Rstepnumbertrialcsv,"w") as output:
            writer=csv.writer(output,lineterminator='\n')
            for val in Rsteptrial[r][j]:
                writer.writerow([val])
        
        Lstepnumbertrialcsv="/home/cuebong/git/cri4/Stepping motion/step_number/left/Lstep_number_"+target_list[j]+"_trial_"+str(r+1)+".csv"
        with open(Lstepnumbertrialcsv,"w") as output:
            writer=csv.writer(output,lineterminator='\n')
            for val in Lsteptrial[r][j]:
                writer.writerow([val])
