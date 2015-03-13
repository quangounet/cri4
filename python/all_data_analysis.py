from extract_midpoint import data
from derivative import *
from perform_splines import perform_spline
from frame_comparison import compare
from trajectory_deviation import traj_dev
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
import matplotlib.pyplot as plt
import numpy as np
import csv
from numpy import *
from scipy import interpolate
from matplotlib.patches import Ellipse
from pylab import *
from read_filenames import get_filepaths
import sys
from mean_traj import mean_calc
from ANOVA import ANOVA
from t_test import T_test
from variance_ellipse_new import variance_ellipse
from butter_filter import butter_lowpass, butter_lowpass_filter

fs=120
lowcut=1

#_________________________Data Extraction________________________#

plt.ion()
subjects=['C01','C03','C04','C05','C07','C06','C08','C09','C10','C11','P01','P02','P03','P04','P05','P06','P07','P08','P09','P10']
#subjects=['C01', 'C04','P01','P03']
fig1=plt.figure(1)
P_VF_Var=[]
P_BF_Var=[]
C_VF_Var=[]
C_BF_Var=[]
eliminate_list=[]

for i in xrange(0,20):
    subject=subjects[i]
    file_paths=[]
    title_list=[]
    use_files,nf,meanX,meanY,sample,Xax,Yax=[],[],[],[],[],[],[]
    MPX,MPY,MPZ,time,x,y,xvalues,yvalues=[],[],[],[],[],[],[],[]
    fX,fY,time_vel,vel_x,vel_y,vel=[],[],[],[],[],[]
    for j in xrange(0,38):
        file_paths.append(get_filepaths("/home/cuebong/git/cri4/AllData/Post_processedCSV/"+subject))
        use_files.append([])
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
        if len(use_files[j])<3:
            print(subject,target,"skipped - not enough datasets")
            title_list.append(0)
            eliminate_list.append(subject+'_'+target)
        else:
            title_list.append(target)

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

        for k in xrange(0,len(use_files[j])):
            with open(use_files[j][k]) as f:
                a,b,c=data(f)
                MPX[j].append(a)
                MPY[j].append(b)
                MPZ[j].append(c)
                noiseX=[]
                noiseY=[]
                for l in xrange(0,len(MPX[j][k])):
                    noiseX.append(float(MPX[j][k][l]))
                    noiseY.append(float(MPY[j][k][l]))
                fX[j].append(butter_lowpass_filter(noiseX,lowcut,fs,order=2))
                fY[j].append(butter_lowpass_filter(noiseY,lowcut,fs,order=2))
                d,e,f,g,h=perform_spline(fX[j][k],fY[j][k])
                time[j].append(d)
                x[j].append(e)
                y[j].append(f)
                xvalues[j].append(g)
                yvalues[j].append(h)

    #plt.close(1)

#_____________________Velocity Profile____________________#

    def resultant_profile(x,y):
        val=[]
        for j in xrange(0,len(x)):
            x_term=x[j]*x[j]
            y_term=y[j]*y[j]
            a=(x_term+y_term)**0.5
            val.append(a)
        return val

    for j in xrange(0,len(file_paths)):
        if len(use_files[j])>2:
            for k in xrange(0,len(use_files[j])):
                for l in xrange(0, len(y[j][k])):
                    n=y[j][k][l]
                    if n>0.5:
                        break
                x[j][k]=np.delete(x[j][k],xrange(0,l))
                y[j][k]=np.delete(y[j][k],xrange(0,l))
                xvalues[j][k]=np.delete(xvalues[j][k],xrange(0,l))
                yvalues[j][k]=np.delete(yvalues[j][k],xrange(0,l))
                fX[j][k]=np.delete(fX[j][k],xrange(0,l))
                fY[j][k]=np.delete(fY[j][k],xrange(0,l))
                
                a,b=deriv_vel(x[j][k])
                time_vel[j].append(a)
                vel_x[j].append(b)
                a,c=deriv_vel(y[j][k])
                vel_y[j].append(c)
                d=resultant_profile(vel_x[j][k],vel_y[j][k])
                vel[j].append(d)
                
                while len(time_vel[j][k])!=len(vel[j][k]):
                    if len(time_vel[j][k])>len(vel[j][k]):
                        time_vel[j][k]=np.delete(time_vel[j][k],(len(time_vel[j][k])-1))
                    else:
                        vel[j][k]=np.delete(vel[j][k],len(vel[j][k])-1)
                        print(len(vel[j][k]))
                        
                for l in xrange(0, len(time_vel[j][k])):
                    m=len(time_vel[j][k])-l-1
                    n=vel[j][k][m]
                    if n>0.4:
                        break
                vel[j][k]=np.delete(vel[j][k],xrange(m,len(vel[j][k])))
                time_vel[j][k]=np.delete(time_vel[j][k],xrange(m,len(time_vel[j][k])))
                x[j][k]=np.delete(x[j][k],xrange(m,len(x[j][k])))
                y[j][k]=np.delete(y[j][k],xrange(m,len(y[j][k])))
                xvalues[j][k]=np.delete(xvalues[j][k],xrange(m,len(x[j][k])))
                yvalues[j][k]=np.delete(yvalues[j][k],xrange(m,len(x[j][k])))
                fX[j][k]=np.delete(fX[j][k],xrange(m,len(fX[j][k])))
                fY[j][k]=np.delete(fY[j][k],xrange(m,len(fY[j][k])))
                                        
               # for l in xrange(0, len(time_vel[j][k])):
                #    n=vel[j][k][l]
                #    if n>0.2:
                #        break
                #vel[j][k]=np.delete(vel[j][k],xrange(0,l))
                #time_vel[j][k]=np.delete(time_vel[j][k],xrange(0,l))
                #x[j][k]=np.delete(x[j][k],xrange(0,l))
                #y[j][k]=np.delete(y[j][k],xrange(0,l))
                #xvalues[j][k]=np.delete(xvalues[j][k],xrange(0,l))
                #yvalues[j][k]=np.delete(yvalues[j][k],xrange(0,l))
                #fX[j][k]=np.delete(fX[j][k],xrange(0,l))
                #fY[j][k]=np.delete(fY[j][k],xrange(0,l))

#___________________Mean Trajectory Plots______________________#

    variability=[]
    if 'C' in subject:
        C_VF_Var.append([])
        C_BF_Var.append([])
        z=len(C_VF_Var)-1
    elif 'P' in subject:
        P_VF_Var.append([])
        P_BF_Var.append([])
        z=len(P_VF_Var)-1

    for j in xrange(0,len(file_paths)):
        if len(use_files[j])<3:
            nf.append(0)
            meanX.append(0)
            meanY.append(0)
            sample.append(0)
            variability.append(0)
            if 'P' in subject:
                if 'VF' in use_files[j][0]:
                    P_VF_Var[z].append(0)
                elif 'BF' in use_files[j][0]:
                    P_BF_Var[z].append(0)
            elif 'C' in subject:
                if 'VF' in use_files[j][0]:
                    C_VF_Var[z].append(0)
                elif 'BF' in use_files[j][0]:
                    C_BF_Var[z].append(0) 

            print(j)
        else:
            nf.append(compare(time[j][0],time[j][1],time[j][2]))
            a,b,c,d,e,f,g,h,k=mean_calc(nf[j],x[j][0],x[j][1],x[j][2],y[j][0],y[j][1],y[j][2],xvalues[j][0],xvalues[j][1],xvalues[j][2],yvalues[j][0],yvalues[j][1],yvalues[j][2])
            meanX.append(a)
            meanY.append(b)
            sample.append(c)
            Xax[j].append(d)
            Xax[j].append(e)
            Xax[j].append(f)
            Yax[j].append(g)
            Yax[j].append(h)
            Yax[j].append(k)
        
            #plt.figure(j+2)
            #mean_traj=plot(meanX[j],meanY[j])
            #actual_traj=plot(MPX[j][0],MPY[j][0],MPX[j][1],MPY[j][1],MPX[j][2],MPY[j][2])
            #plt.setp(actual_traj,linestyle='--')
            #plt.xlim(0,4.5)
           # plt.ylim(0,6) 
            #plt.gca().set_aspect('equal',adjustable='box')
            #plt.xlabel=('X_axis')
            #plt.ylabel=('Y_axis')
            #plt.suptitle('Mean Trajectory '+subject+"_"+title_list[j])
            #plt.suptitle('Variance Profile '+subject+"_"+title_list[j])

            a=variance_ellipse(sample[j],Xax[j][0],Xax[j][1],Xax[j][2],Yax[j][0],Yax[j][1],Yax[j][2])
            variability.append(a)     
            if 'P' in subject:
                if 'VF' in title_list[j]:
                    P_VF_Var[z].append(max(variability[j]))
                elif 'BF' in title_list[j]:
                    P_BF_Var[z].append(max(variability[j]))
            elif 'C' in subject:
                if 'VF' in title_list[j]:
                    C_VF_Var[z].append(max(variability[j]))
                elif 'BF' in title_list[j]:
                    C_BF_Var[z].append(max(variability[j])) 

            #plt.savefig("/home/cuebong/git/cri4/Trajectory_Plots/"+subject+"_"+title_list[j])
            plt.close()
           # plt.figure(j+2)
            #plt.cla()
           # plt.plot(sample[j],variability[j])
            #plt.figure(j+40)
           # plt.xlim(0,1)
           # plt.ylim(0,3)
            #plt.xlabel('Time')
            #plt.ylabel('Variability')
           # plt.suptitle('Variance Profile '+subject+"_"+title_list[j])
           # plt.savefig("/home/cuebong/git/cri4/Trajectory_Plots/Variance_Profiles/"+subject+"_"+title_list[j])
            #plt.close(j+40)
            #plt.close()
patientVF=[]
controlVF=[]
patientBF=[]
controlBF=[]
HpatientVF=[]
HcontrolVF=[]
HpatientBF=[]
HcontrolBF=[]

patient_vert_VF=[]
control_vert_VF=[]
patient_vert_BF=[]
control_vert_BF=[]
Hpatient_vert_VF=[]
Hcontrol_vert_VF=[]
Hpatient_vert_BF=[]
Hcontrol_vert_BF=[]

patient_curved_VF=[]
control_curved_VF=[]
patient_curved_BF=[]
control_curved_BF=[]
Hpatient_curved_VF=[]
Hcontrol_curved_VF=[]
Hpatient_curved_BF=[]
Hcontrol_curved_BF=[]

patient_uturn_VF=[]
control_uturn_VF=[]
patient_uturn_BF=[]
control_uturn_BF=[]
Hpatient_uturn_VF=[]
Hcontrol_uturn_VF=[]
Hpatient_uturn_BF=[]
Hcontrol_uturn_BF=[]

for i in eliminate_list:
    if 'P01' in i or 'C01' in i:
        u=0
        v=0
    elif 'P02' in i or 'C03' in i:
        u=1
        v=1
    elif 'P03' in i or 'C04' in i:
        u=2
        v=2  
    elif 'P04' in i or 'C05' in i:
        u=3
        v=3
    elif 'P05' in i or 'C07' in i:
        u=4
        v=4   
    elif 'P06' in i or 'C06' in i:
        u=5
        v=5    
    elif 'P07' in i or 'C08' in i:
        u=6
        v=6    
    elif 'P08' in i or 'C09' in i:
        u=7
        v=7    
    elif 'P09' in i or 'C10' in i:
        u=8
        v=8    
    elif 'P10' in i or 'C11' in i:
        u=9
        v=9

    for j in xrange(0, len(P_VF_Var[u])):
        if P_VF_Var[u][j]==0:
            C_VF_Var[v][j]=0
            P_BF_Var[u][j]=0
            C_BF_Var[v][j]=0
    for j in xrange(0, len(P_BF_Var[u])):
        if P_BF_Var[u][j]==0:
            C_BF_Var[v][j]=0
            P_VF_Var[u][j]=0
            C_VF_Var[v][j]=0
    for j in xrange(0, len(C_VF_Var[v])):
        if C_VF_Var[v][j]==0 and P_VF_Var[u][j]!=0:
            P_VF_Var[u][j]=0
            P_BF_Var[u][j]=0
            C_BF_Var[v][j]=0
    for j in xrange(0, len(C_BF_Var[v])):   
        if C_BF_Var[v][j]==0 and P_BF_Var[u][j]!=0:
            P_BF_Var[u][j]=0
            P_VF_Var[u][j]=0
            C_VF_Var[v][j]=0

hemPC=[2,3,6,7,8]
NHPC=[0,1,4,5,9]
straight=[16,17,18]
curved=[0,1,3,4,5,7,8,9,11,12,13,15]
uturn=[2,6,10,14]

for i in hemPC:
    for j in xrange(0, len(P_VF_Var[i])):
        if P_VF_Var[i][j]!=0:
            HpatientVF.append(P_VF_Var[i][j])
            HcontrolVF.append(C_VF_Var[i][j])
            if j in straight:
                Hpatient_vert_VF.append(P_VF_Var[i][j])
                Hcontrol_vert_VF.append(C_VF_Var[i][j])
            elif j in curved:
                Hpatient_curved_VF.append(P_VF_Var[i][j])
                Hcontrol_curved_VF.append(C_VF_Var[i][j])
            elif j in uturn:
                Hpatient_uturn_VF.append(P_VF_Var[i][j])
                Hcontrol_uturn_VF.append(C_VF_Var[i][j])

    for j in xrange(0,len(P_BF_Var[i])):
        if P_BF_Var[i][j]!=0:
            HpatientBF.append(P_BF_Var[i][j])
            HcontrolBF.append(C_BF_Var[i][j])
            if j in straight:
                Hpatient_vert_BF.append(P_BF_Var[i][j])
                Hcontrol_vert_BF.append(C_BF_Var[i][j])
            elif j in curved:
                Hpatient_curved_BF.append(P_BF_Var[i][j])
                Hcontrol_curved_BF.append(C_BF_Var[i][j])
            elif j in uturn:
                Hpatient_uturn_BF.append(P_BF_Var[i][j])
                Hcontrol_uturn_BF.append(C_BF_Var[i][j])
                                        
for i in NHPC:
    for j in xrange(0,len(P_VF_Var[i])):
        if P_VF_Var[i][j]!=0:
            patientVF.append(P_VF_Var[i][j])
            controlVF.append(C_VF_Var[i][j])
            if j in straight:
                patient_vert_VF.append(P_VF_Var[i][j])
                control_vert_VF.append(C_VF_Var[i][j])
            elif j in curved:
                patient_curved_VF.append(P_VF_Var[i][j])
                control_curved_VF.append(C_VF_Var[i][j])
            elif j in uturn:
                patient_uturn_VF.append(P_VF_Var[i][j])
                control_uturn_VF.append(C_VF_Var[i][j])

    for j in xrange(0,len(P_BF_Var[i])):
        if P_BF_Var[i][j]!=0:
            patientBF.append(P_BF_Var[i][j])
            controlBF.append(C_BF_Var[i][j])
            if j in straight:
                patient_vert_BF.append(P_BF_Var[i][j])
                control_vert_BF.append(C_BF_Var[i][j])
            elif j in curved:
                patient_curved_BF.append(P_BF_Var[i][j])
                control_curved_BF.append(C_BF_Var[i][j])
            elif j in uturn:
                patient_uturn_BF.append(P_BF_Var[i][j])
                control_uturn_BF.append(C_BF_Var[i][j])
   
MTD1_Data, MTD2_Data, MTD3_Data=[],[],[]
MTD1_Data.append([])
MTD1_Data.append([])
MTD1_Data[0].append([])
MTD1_Data[0].append([])
MTD1_Data[1].append([])
MTD1_Data[1].append([])
MTD2_Data.append([])
MTD2_Data.append([])
MTD2_Data[0].append([])
MTD2_Data[0].append([])
MTD2_Data[1].append([])
MTD2_Data[1].append([])
MTD3_Data.append([])
MTD3_Data.append([])
MTD3_Data[0].append([])
MTD3_Data[0].append([])
MTD3_Data[1].append([])
MTD3_Data[1].append([])
                                        
for i in xrange(0,len(controlVF)):
    MTD1_Data[0][0].append(patientVF[i])
    MTD1_Data[0][0].append(HpatientVF[i])
    MTD1_Data[0][1].append(patientBF[i])
    MTD1_Data[0][1].append(HpatientBF[i])
    MTD1_Data[1][0].append(controlVF[i])
    MTD1_Data[1][0].append(HcontrolVF[i])
    MTD1_Data[1][1].append(controlBF[i])
    MTD1_Data[1][1].append(HcontrolBF[i])
    
    MTD2_Data[0][0].append(HpatientVF[i])
    MTD2_Data[0][1].append(HpatientBF[i])
    MTD2_Data[1][0].append(HcontrolVF[i])
    MTD2_Data[1][1].append(HcontrolBF[i])  

    MTD3_Data[0][0].append(patientVF[i])
    MTD3_Data[0][1].append(patientBF[i])
    MTD3_Data[1][0].append(controlVF[i])
    MTD3_Data[1][1].append(controlBF[i])

t1DoF3=(len(MTD1_Data[0][0])-1)*4
t2DoF3=(len(MTD2_Data[0][0])-1)*4
t3DoF3=(len(MTD3_Data[0][0])-1)*4

test1_f,DoF1,effPC1,effV1=ANOVA(MTD1_Data,t1DoF3)
test2_f,DoF2,effPC2,effV2=ANOVA(MTD2_Data,t2DoF3)
test3_f,DoF3,effPC3,effV3=ANOVA(MTD3_Data,t3DoF3)

vertMTD1_Data, vertMTD2_Data, vertMTD3_Data=[],[],[]
vertMTD1_Data.append([])
vertMTD1_Data.append([])
vertMTD1_Data[0].append([])
vertMTD1_Data[0].append([])
vertMTD1_Data[1].append([])
vertMTD1_Data[1].append([])
vertMTD2_Data.append([])
vertMTD2_Data.append([])
vertMTD2_Data[0].append([])
vertMTD2_Data[0].append([])
vertMTD2_Data[1].append([])
vertMTD2_Data[1].append([])
vertMTD3_Data.append([])
vertMTD3_Data.append([])
vertMTD3_Data[0].append([])
vertMTD3_Data[0].append([])
vertMTD3_Data[1].append([])
vertMTD3_Data[1].append([])

for i in xrange(0,len(control_vert_VF)):
    vertMTD1_Data[0][0].append(patient_vert_VF[i])
    vertMTD1_Data[0][0].append(Hpatient_vert_VF[i])
    vertMTD1_Data[0][1].append(patient_vert_BF[i])
    vertMTD1_Data[0][1].append(Hpatient_vert_BF[i])
    vertMTD1_Data[1][0].append(control_vert_VF[i])
    vertMTD1_Data[1][0].append(Hcontrol_vert_VF[i])
    vertMTD1_Data[1][1].append(control_vert_BF[i])
    vertMTD1_Data[1][1].append(Hcontrol_vert_BF[i])
    vertMTD2_Data[0][0].append(Hpatient_vert_VF[i])
    vertMTD2_Data[0][1].append(Hpatient_vert_BF[i])
    vertMTD2_Data[1][0].append(Hcontrol_vert_VF[i])
    vertMTD2_Data[1][1].append(Hcontrol_vert_BF[i]) 
    vertMTD3_Data[0][0].append(patient_vert_VF[i])
    vertMTD3_Data[0][1].append(patient_vert_BF[i])
    vertMTD3_Data[1][0].append(control_vert_VF[i])
    vertMTD3_Data[1][1].append(control_vert_BF[i])
                                        
vertt1DoF3=(len(vertMTD1_Data[0][0])-1)*4
vertt2DoF3=(len(vertMTD2_Data[0][0])-1)*4
vertt3DoF3=(len(vertMTD3_Data[0][0])-1)*4

verttest1_f,vertDoF1,verteffPC1,verteffV1=ANOVA(vertMTD1_Data,vertt1DoF3)
verttest2_f,vertDoF2,verteffPC2,verteffV2=ANOVA(vertMTD2_Data,vertt2DoF3)
verttest3_f,vertDoF3,verteffPC3,verteffV3=ANOVA(vertMTD3_Data,vertt3DoF3)

curvedMTD1_Data, curvedMTD2_Data,curvedMTD3_Data=[],[],[]
curvedMTD1_Data.append([])
curvedMTD1_Data.append([])
curvedMTD1_Data[0].append([])
curvedMTD1_Data[0].append([])
curvedMTD1_Data[1].append([])
curvedMTD1_Data[1].append([])
curvedMTD2_Data.append([])
curvedMTD2_Data.append([])
curvedMTD2_Data[0].append([])
curvedMTD2_Data[0].append([])
curvedMTD2_Data[1].append([])
curvedMTD2_Data[1].append([])
curvedMTD3_Data.append([])
curvedMTD3_Data.append([])
curvedMTD3_Data[0].append([])
curvedMTD3_Data[0].append([])
curvedMTD3_Data[1].append([])
curvedMTD3_Data[1].append([])

for i in xrange(0,len(control_curved_VF)):
    curvedMTD1_Data[0][0].append(patient_curved_VF[i])
    curvedMTD1_Data[0][0].append(Hpatient_curved_VF[i])
    curvedMTD1_Data[0][1].append(patient_curved_BF[i])
    curvedMTD1_Data[0][1].append(Hpatient_curved_BF[i])
    curvedMTD1_Data[1][0].append(control_curved_VF[i])
    curvedMTD1_Data[1][0].append(Hcontrol_curved_VF[i])
    curvedMTD1_Data[1][1].append(control_curved_BF[i])
    curvedMTD1_Data[1][1].append(Hcontrol_curved_BF[i])
    curvedMTD2_Data[0][0].append(Hpatient_curved_VF[i])
    curvedMTD2_Data[0][1].append(Hpatient_curved_BF[i])
    curvedMTD2_Data[1][0].append(Hcontrol_curved_VF[i])
    curvedMTD2_Data[1][1].append(Hcontrol_curved_BF[i]) 
    curvedMTD3_Data[0][0].append(patient_curved_VF[i])
    curvedMTD3_Data[0][1].append(patient_curved_BF[i])
    curvedMTD3_Data[1][0].append(control_curved_VF[i])
    curvedMTD3_Data[1][1].append(control_curved_BF[i])
                                        
curvedt1DoF3=(len(curvedMTD1_Data[0][0])-1)*4
curvedt2DoF3=(len(curvedMTD2_Data[0][0])-1)*4
curvedt3DoF3=(len(curvedMTD3_Data[0][0])-1)*4

curvedtest1_f,curvedDoF1,curvedeffPC1,curvedeffV1=ANOVA(curvedMTD1_Data,curvedt1DoF3)
curvedtest2_f,curvedDoF2,curvedeffPC2,curvedeffV2=ANOVA(curvedMTD2_Data,curvedt2DoF3)
curvedtest3_f,curvedDoF3,curvedeffPC3,curvedeffV3=ANOVA(curvedMTD3_Data,curvedt3DoF3)


uturnMTD1_Data, uturnMTD2_Data, uturnMTD3_Data=[],[],[]
uturnMTD1_Data.append([])
uturnMTD1_Data.append([])
uturnMTD1_Data[0].append([])
uturnMTD1_Data[0].append([])
uturnMTD1_Data[1].append([])
uturnMTD1_Data[1].append([])
uturnMTD2_Data.append([])
uturnMTD2_Data.append([])
uturnMTD2_Data[0].append([])
uturnMTD2_Data[0].append([])
uturnMTD2_Data[1].append([])
uturnMTD2_Data[1].append([])
uturnMTD3_Data.append([])
uturnMTD3_Data.append([])
uturnMTD3_Data[0].append([])
uturnMTD3_Data[0].append([])
uturnMTD3_Data[1].append([])
uturnMTD3_Data[1].append([])
                                        
for i in xrange(0,len(control_uturn_VF)):
    uturnMTD1_Data[0][0].append(patient_uturn_VF[i])
    uturnMTD1_Data[0][0].append(Hpatient_uturn_VF[i])
    uturnMTD1_Data[0][1].append(patient_uturn_BF[i])
    uturnMTD1_Data[0][1].append(Hpatient_uturn_BF[i])
    uturnMTD1_Data[1][0].append(control_uturn_VF[i])
    uturnMTD1_Data[1][0].append(Hcontrol_uturn_VF[i])
    uturnMTD1_Data[1][1].append(control_uturn_BF[i])
    uturnMTD1_Data[1][1].append(Hcontrol_uturn_BF[i])
    uturnMTD2_Data[0][0].append(Hpatient_uturn_VF[i])
    uturnMTD2_Data[0][1].append(Hpatient_uturn_BF[i])
    uturnMTD2_Data[1][0].append(Hcontrol_uturn_VF[i])
    uturnMTD2_Data[1][1].append(Hcontrol_uturn_BF[i]) 
    uturnMTD3_Data[0][0].append(patient_uturn_VF[i])
    uturnMTD3_Data[0][1].append(patient_uturn_BF[i])
    uturnMTD3_Data[1][0].append(control_uturn_VF[i])
    uturnMTD3_Data[1][1].append(control_uturn_BF[i])
                                        
uturnt1DoF3=(len(uturnMTD1_Data[0][0])-1)*4
uturnt2DoF3=(len(uturnMTD2_Data[0][0])-1)*4
uturnt3DoF3=(len(uturnMTD3_Data[0][0])-1)*4

uturntest1_f,uturnDoF1,uturneffPC1,uturneffV1=ANOVA(uturnMTD1_Data,uturnt1DoF3)
uturntest2_f,uturnDoF2,uturneffPC2,uturneffV2=ANOVA(uturnMTD2_Data,uturnt2DoF3)
uturntest3_f,uturnDoF3,uturneffPC3,uturneffV3=ANOVA(uturnMTD3_Data,uturnt3DoF3)

Anovagroup=[MTD1_Data,MTD2_Data,MTD3_Data,vertMTD1_Data,vertMTD2_Data,vertMTD3_Data,curvedMTD1_Data,curvedMTD2_Data,curvedMTD3_Data,uturnMTD1_Data,uturnMTD2_Data,uturnMTD3_Data]
    
csv_names=['all','hem','non-hem','straight-all','straight-hem','straight-non-hem','curved-all','curved-hem','curved-non-hem','uturn-all','uturn-hem','uturn-non-hem']
MTD_csv_data=[[MTD1_Data[0][0],MTD1_Data[0][1],MTD1_Data[1][0],MTD1_Data[1][1]],[MTD2_Data[0][0],MTD2_Data[0][1],MTD2_Data[1][0],MTD2_Data[1][1]],[MTD3_Data[0][0],MTD3_Data[0][1],MTD3_Data[1][0],MTD3_Data[1][1]],[vertMTD1_Data[0][0],vertMTD1_Data[0][1],vertMTD1_Data[1][0],vertMTD1_Data[1][1]],[vertMTD2_Data[0][0],vertMTD2_Data[0][1],vertMTD2_Data[1][0],vertMTD2_Data[1][1]],[vertMTD3_Data[0][0],vertMTD3_Data[0][1],vertMTD3_Data[1][0],vertMTD3_Data[1][1]],[curvedMTD1_Data[0][0],curvedMTD1_Data[0][1],curvedMTD1_Data[1][0],curvedMTD1_Data[1][1]],[curvedMTD2_Data[0][0],curvedMTD2_Data[0][1],curvedMTD2_Data[1][0],curvedMTD2_Data[1][1]],[curvedMTD3_Data[0][0],curvedMTD3_Data[0][1],curvedMTD3_Data[1][0],curvedMTD3_Data[1][1]],[uturnMTD1_Data[0][0],uturnMTD1_Data[0][1],uturnMTD1_Data[1][0],uturnMTD1_Data[1][1]],[uturnMTD2_Data[0][0],uturnMTD2_Data[0][1],uturnMTD2_Data[1][0],uturnMTD2_Data[1][1]],[uturnMTD3_Data[0][0],uturnMTD3_Data[0][1],uturnMTD3_Data[1][0],uturnMTD3_Data[1][1]]]

for i in xrange(0,len(csv_names)):
    for j in xrange(0,len(MTD_csv_data[i])):
        csvfile="/home/cuebong/git/cri4/MTD data/MTD_data"+csv_names[i]+str(j+1)+".csv"
        with open(csvfile,"w") as output:
            writer=csv.writer(output,lineterminator='\n')
            for val in MTD_csv_data[i][j]:
                writer.writerow([val])
    
#VFt_test, VFDoF=T_test(patientVF,controlVF)
#BFt_test, BFDoF=T_test(patientBF,controlBF)
#HVFt_test, HVFDoF=T_test(HpatientVF,HcontrolVF)
#HBFt_test, HBFDoF=T_test(HpatientBF,HcontrolBF)
#print(VFt_test, VFDoF,BFt_test,BFDoF)
#print(HVFt_test, HVFDoF,HBFt_test,HBFDoF)