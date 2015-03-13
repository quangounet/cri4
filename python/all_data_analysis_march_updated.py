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
import csv
from mean_traj import mean_calc
from mean_traj import mean_calc2
from ANOVA import ANOVA
from t_test import T_test
from variance_ellipse_new2 import variance_ellipse
from variance_ellipse_new2 import variance_ellipse2
from variance_ellipse_new2 import variance_ellipse_2
from variance_ellipse_new2 import variance_ellipse2_2
from butter_filter import butter_lowpass, butter_lowpass_filter

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

#_________________________Data Extraction________________________#

plt.ion()
subjects=['C01','C03','C04','C05','C07','C06','C08','C09','C10','C11','P01','P02','P03','P04','P05','P06','P07','P08','P09','P10']
#subjects=['C01', 'C04','P01','P03']
target_list=['C4E_L_bleu','C4N_L_bleu','C4S_L_bleu','C4W_L_bleu','C5E_L_bleu','C5N_L_bleu','C5S_L_bleu','C5W_L_bleu','C4E_R_rouge','C4N_R_rouge','C4S_R_rouge','C4W_R_rouge','C5E_R_rouge','C5N_R_rouge','C5S_R_rouge','C5W_R_rouge','C1N_S_vert','C2N_S_vert','C3N_S_vert']

target_list2=['C4E_L_bleu_VF','C4N_L_bleu_VF','C4S_L_bleu_VF','C4W_L_bleu_VF','C4E_L_bleu_BF','C4N_L_bleu_BF','C4S_L_bleu_BF','C4W_L_bleu_BF','C5E_L_bleu_VF','C5N_L_bleu_VF','C5S_L_bleu_VF','C5W_L_bleu_VF','C5E_L_bleu_BF','C5N_L_bleu_BF','C5S_L_bleu_BF','C5W_L_bleu_BF','C4E_R_rouge_VF','C4N_R_rouge_VF','C4S_R_rouge_VF','C4W_R_rouge_VF','C4E_R_rouge_BF','C4N_R_rouge_BF','C4S_R_rouge_BF','C4W_R_rouge_BF','C5E_R_rouge_VF','C5N_R_rouge_VF','C5S_R_rouge_VF','C5W_R_rouge_VF','C5E_R_rouge_BF','C5N_R_rouge_BF','C5S_R_rouge_BF','C5W_R_rouge_BF','C1N_S_vert_VF','C1N_S_vert_BF','C2N_S_vert_VF','C2N_S_vert_BF','C3N_S_vert_VF','C3N_S_vert_BF']

fig1=plt.figure(1)
P_VF_Var=[]
P_BF_Var=[]
C_VF_Var=[]
C_BF_Var=[]
meanX=[]
meanY=[]
sample=[]
meanvel=[]
velsample=[]
velax=[]
eliminate_list=[]
Xax=[]
Yax=[]
x,y=[],[]
xvalues,yvalues=[],[]
velinterp,velvalue=[],[]


for i in xrange(0,20):
    subject=subjects[i]
    file_paths=[]
    title_list=[]
    use_files,nf=[],[]
    meanX.append([])
    meanY.append([])
    sample.append([])
    meanvel.append([])
    velsample.append([])
    velax.append([])
    Xax.append([])
    Yax.append([])    
    x.append([])
    y.append([])
    velinterp.append([])
    velvalue.append([])
    xvalues.append([])
    yvalues.append([])
    MPX,MPY,MPZ,time=[],[],[],[]
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
        #if len(use_files[j])<3:
            #print(subject,target,"skipped - not enough datasets")
            #title_list.append(0)
            #eliminate_list.append(subject+'_'+target)
        #else:
        title_list.append(target)

        MPX.append([])
        MPY.append([])
        MPZ.append([])
        time.append([])
        x[i].append([])
        y[i].append([])
        xvalues[i].append([])
        yvalues[i].append([])
        Xax[i].append([])
        Yax[i].append([])
        velax[i].append([])
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
                time[j].append(d)
                x[i][j].append(e)
                y[i][j].append(f)
                xvalues[i][j].append(g)
                yvalues[i][j].append(h)

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
        velinterp[i].append([])
        velvalue[i].append([])
        if len(use_files[j])>2:
            for k in xrange(0,len(use_files[j])):
                for l in xrange(0, len(y[i][j][k])):
                    n=y[i][j][k][l]
                    if n>0.5:
                        break
                x[i][j][k]=np.delete(x[i][j][k],xrange(0,l))
                y[i][j][k]=np.delete(y[i][j][k],xrange(0,l))
                xvalues[i][j][k]=np.delete(xvalues[i][j][k],xrange(0,l))
                yvalues[i][j][k]=np.delete(yvalues[i][j][k],xrange(0,l))
                fX[j][k]=np.delete(fX[j][k],xrange(0,l))
                fY[j][k]=np.delete(fY[j][k],xrange(0,l))

                a,b=deriv_vel(x[i][j][k])
                time_vel[j].append(a)
                vel_x[j].append(b)
                a,c=deriv_vel(y[i][j][k])
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

                #for l in xrange(0, len(time_vel[j][k])):
                    #n=vel[j][k][l]
                    #if n>0.2:
                        #break
                #vel[j][k]=np.delete(vel[j][k],xrange(0,l))
                #time_vel[j][k]=np.delete(time_vel[j][k],xrange(0,l))
                #x[j][k]=np.delete(x[j][k],xrange(0,l))
                #y[j][k]=np.delete(y[j][k],xrange(0,l))
                #xvalues[j][k]=np.delete(xvalues[j][k],xrange(0,l))
                #yvalues[j][k]=np.delete(yvalues[j][k],xrange(0,l))
                #fX[j][k]=np.delete(fX[j][k],xrange(0,l))
                #fY[j][k]=np.delete(fY[j][k],xrange(0,l))
                
                e,f=perform_spline2(vel[j][k])
                velinterp[i][j].append(e)
                velvalue[i][j].append(f)
            
            velnf=compare(time_vel[j][0],time_vel[j][1],time_vel[j][2])
            g,h,p,n,o=mean_calc2(velnf,velinterp[i][j][0],velinterp[i][j][1],velinterp[i][j][2],velvalue[i][j][0],velvalue[i][j][1],velvalue[i][j][2])
            meanvel[i].append(h)
            velsample[i].append(g)
            velax[i][j].append(p)
            velax[i][j].append(n)
            velax[i][j].append(o)
        else:
            #meanvel[i].append(0)
            #velsample[i].append(0)
            for k in xrange(0,len(use_files[j])):
                for l in xrange(0, len(y[i][j][k])):
                    n=y[i][j][k][l]
                    if n>0.5:
                        break
                x[i][j][k]=np.delete(x[i][j][k],xrange(0,l))
                y[i][j][k]=np.delete(y[i][j][k],xrange(0,l))
                xvalues[i][j][k]=np.delete(xvalues[i][j][k],xrange(0,l))
                yvalues[i][j][k]=np.delete(yvalues[i][j][k],xrange(0,l))
                fX[j][k]=np.delete(fX[j][k],xrange(0,l))
                fY[j][k]=np.delete(fY[j][k],xrange(0,l))
                
                a,b=deriv_vel(x[i][j][k])
                time_vel[j].append(a)
                vel_x[j].append(b)
                a,c=deriv_vel(y[i][j][k])
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
                    n=0
                    m=len(time_vel[j][k])-l-1
                    n=vel[j][k][m]
                    if i==17 and j==33 and n>0.2:
                        break
                    if (i==13 or i==17) and n>0.28:
                        break
                    if n>0.4 and (i in velcutlow):
                        break
                    if n>0.5 and (i in velcutmed):
                        break
                    if n>0.7 and (i in velcuthi):
                        break
                vel[j][k]=np.delete(vel[j][k],xrange(m,len(vel[j][k])))
                time_vel[j][k]=np.delete(time_vel[j][k],xrange(m,len(time_vel[j][k])))
                x[i][j][k]=np.delete(x[i][j][k],xrange(m,len(x[i][j][k])))
                y[i][j][k]=np.delete(y[i][j][k],xrange(m,len(y[i][j][k])))
                xvalues[i][j][k]=np.delete(xvalues[i][j][k],xrange(m,len(xvalues[i][j][k])))
                yvalues[i][j][k]=np.delete(yvalues[i][j][k],xrange(m,len(yvalues[i][j][k])))
                fX[j][k]=np.delete(fX[j][k],xrange(m,len(fX[j][k])))
                fY[j][k]=np.delete(fY[j][k],xrange(m,len(fY[j][k])))

                e,f=perform_spline2(vel[j][k])
                velinterp[i][j].append(e)
                velvalue[i][j].append(f)

            if len(time_vel[j][0])<len(time_vel[j][1]):
                velnf=len(time_vel[j][0])
            else:
                velnf=len(time_vel[j][1])
            g,h,p,o=[],[],[],[]
            for r in xrange(0,velnf):
                g.append(Decimal(r)/velnf)
                p.append(velvalue[i][j][0][g[r]*len(velinterp[i][j][0])])
                o.append(velvalue[i][j][1][g[r]*len(velinterp[i][j][1])])
                h.append(Decimal(p[r]+o[r])/2)
            meanvel[i].append(h)
            velsample[i].append(g)
            velax[i][j].append(p)
            velax[i][j].append(o)

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
            #nf.append(0)
            #meanX[i].append(0)
            #meanY[i].append(0)
            #sample[i].append(0)
            #variability.append(0)
            #if 'P' in subject:
                #if 'VF' in use_files[j][0]:
                    #P_VF_Var[z].append(0)
                #elif 'BF' in use_files[j][0]:
                    #P_BF_Var[z].append(0)
            #elif 'C' in subject:
                #if 'VF' in use_files[j][0]:
                    #C_VF_Var[z].append(0)
                #elif 'BF' in use_files[j][0]:
                    #C_BF_Var[z].append(0) 
            if len(time[j][0])<len(time[j][1]):
                nf.append(len(time_vel[j][0]))
            else:
                nf.append(len(time_vel[j][1]))
            a,b,c,d,e,f,g=[],[],[],[],[],[],[]
            for r in xrange(0,nf[j]):
                c.append(Decimal(r)/nf[j])
                d.append(xvalues[i][j][0][c[r]*len(x[i][j][0])])
                e.append(xvalues[i][j][1][c[r]*len(x[i][j][1])])
                f.append(yvalues[i][j][0][c[r]*len(y[i][j][0])])
                g.append(yvalues[i][j][1][c[r]*len(y[i][j][1])])
                a.append(Decimal(d[r]+e[r])/2)
                b.append(Decimal(f[r]+g[r])/2)
            meanX[i].append(a)
            meanY[i].append(b)
            sample[i].append(c)
            Xax[i][j].append(d)
            Xax[i][j].append(e)
            Yax[i][j].append(f)
            Yax[i][j].append(g)
        else:
            nf.append(compare(time[j][0],time[j][1],time[j][2]))
            a,b,c,d,e,f,g,h,k=mean_calc(nf[j],x[i][j][0],x[i][j][1],x[i][j][2],y[i][j][0],y[i][j][1],y[i][j][2],xvalues[i][j][0],xvalues[i][j][1],xvalues[i][j][2],yvalues[i][j][0],yvalues[i][j][1],yvalues[i][j][2])
            meanX[i].append(a)
            meanY[i].append(b)
            sample[i].append(c)
            Xax[i][j].append(d)
            Xax[i][j].append(e)
            Xax[i][j].append(f)
            Yax[i][j].append(g)
            Yax[i][j].append(h)
            Yax[i][j].append(k)
        
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
"""
target_order=[0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27,32,34,36,4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31,33,35,37]

for j in xrange(0,19):
    l=target_order[j]
    k=j+19
    m=target_order[k]
    x_count1=0
    x_count2=0
    f1,targetplots=plt.subplots(10,2,figsize=(11,44))###
    for i in xrange(0,20):###
        if i in xrange(0,10):###
            y_count=0
            x_count=x_count1
        elif i in xrange(10,20):###
            y_count=1
            x_count=x_count2
        #if meanX[i][l]!=0:
        targetplots[x_count,y_count].plot(meanX[i][l],meanY[i][l],color='r')
        targetplots[x_count,y_count].set_title(subjects[i])
        if len(Xax[i][l])==3:
            a=variance_ellipse(sample[i][l],Xax[i][l][0],Xax[i][l][1],Xax[i][l][2],Yax[i][l][0],Yax[i][l][1],Yax[i][l][2],x_count,y_count,targetplots,1,0.1)
        else:
            a=variance_ellipse_2(sample[i][l],Xax[i][l][0],Xax[i][l][1],Yax[i][l][0],Yax[i][l][1],x_count,y_count,targetplots,1,0.1)
        #else:
            #targetplots[x_count,y_count].plot(0,0)
            #targetplots[x_count,y_count].set_title(subjects[i])
        #if meanX[i][m]!=0:
        targetplots[x_count,y_count].plot(meanX[i][m],meanY[i][m],color='k')
        if len(Xax[i][m])==3:
            a=variance_ellipse(sample[i][m],Xax[i][m][0],Xax[i][m][1],Xax[i][m][2],Yax[i][m][0],Yax[i][m][1],Yax[i][m][2],x_count,y_count,targetplots,2,0.02)
        else:
            a=variance_ellipse_2(sample[i][m],Xax[i][m][0],Xax[i][m][1],Yax[i][m][0],Yax[i][m][1],x_count,y_count,targetplots,2,0.02)
        if i in xrange(0,10):###
           x_count1=x_count1+1
        elif i in xrange(10,20):###
            x_count2=x_count2+1
        targetplots[x_count,y_count].set_xlim(0,4.5)
        targetplots[x_count,y_count].set_ylim(0,6)
        targetplots[x_count,y_count].set_aspect('equal')
    f1.savefig("/home/cuebong/git/cri4/Trajectory_Plots/Combined/trajectory_plots_"+target_list[j]+".pdf")
    plt.close()


for j in xrange(0,19):
    l=target_order[j]
    k=j+19
    m=target_order[k]
    x_count1=0
    x_count2=0
    f2,velplots=plt.subplots(10,2,figsize=(12,48))###
    for i in xrange(0,20):###
        if i in xrange(0,10):###
            y_count=0
            x_count=x_count1
        elif i in xrange(10,20):###
            y_count=1
            x_count=x_count2
        #if meanX[i][l]!=0
        velplots[x_count,y_count].plot(velsample[i][l],meanvel[i][l],color='r')
        velplots[x_count,y_count].set_title(subjects[i])
        if len(velax[i][l])==3:
            a=variance_ellipse2(velsample[i][l],velax[i][l][0],velax[i][l][1],velax[i][l][2],x_count,y_count,velplots,1)
        else:
            a=variance_ellipse2_2(velsample[i][l],velax[i][l][0],velax[i][l][1],x_count,y_count,velplots,1)
        #else:
            #velplots[x_count,y_count].plot(0,0)
            #velplots[x_count,y_count].set_title(subjects[i])
        #if meanX[i][m]!=0:
        velplots[x_count,y_count].plot(velsample[i][m],meanvel[i][m],color='k')
        if len(velax[i][m])==3:
            a=variance_ellipse2(velsample[i][m],velax[i][m][0],velax[i][m][1],velax[i][m][2],x_count,y_count,velplots,2)
        else:
            a=variance_ellipse2_2(velsample[i][m],velax[i][m][0],velax[i][m][1],x_count,y_count,velplots,2)

        if i in xrange(0,10):###
           x_count1=x_count1+1
        elif i in xrange(10,20):###
            x_count2=x_count2+1
        velplots[x_count,y_count].set_xlim(0,1)
        velplots[x_count,y_count].set_ylim(0,1.6)
        velplots[x_count,y_count].set_aspect('equal')
    f2.savefig("/home/cuebong/git/cri4/Trajectory_Plots/Velocity_Plots/velocity_profiles_"+target_list[j]+".pdf")
    plt.close()
"""
#___________START_____________#
"""
#____Calculating Distance_____#

Distancetrial1=[]
Distancetrial2=[]
Distancetrial3=[]

for j in xrange(0,38):
    Distancetrial1.append([])
    Distancetrial2.append([])
    Distancetrial3.append([])
    for i in xrange(0,20):
        for r in xrange(0,len(x[i][j])):
            distance=0
            if r==0:
                for l in xrange(0,len(x[i][j][r])-1):
                    xsq=(float(x[i][j][r][l+1])-x[i][j][r][l])**2
                    ysq=(float(y[i][j][r][l+1])-y[i][j][r][l])**2
                    distance=distance+float(sqrt(xsq+ysq))
                Distancetrial1[j].append(distance)
            if r==1:
               for l in xrange(0,len(x[i][j][r])-1):
                    xsq=(float(x[i][j][r][l+1])-x[i][j][r][l])**2
                    ysq=(float(y[i][j][r][l+1])-y[i][j][r][l])**2
                    distance=distance+float(sqrt(xsq+ysq))
               Distancetrial2[j].append(distance) 
            if r==2:
               for l in xrange(0,len(x[i][j][r])-1):
                    xsq=(float(x[i][j][r][l+1])-x[i][j][r][l])**2
                    ysq=(float(y[i][j][r][l+1])-y[i][j][r][l])**2
                    distance=distance+float(sqrt(xsq+ysq))
               Distancetrial3[j].append(distance)  

for j in xrange(0,len(Distancetrial1)):
    Distancetrial1csv="/home/cuebong/git/cri4/Distance_Data/Distance_trial_1_"+target_list2[j]+".csv"
    with open(Distancetrial1csv,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in Distancetrial1[j]:
            writer.writerow([val])

    Distancetrial2csv="/home/cuebong/git/cri4/Distance_Data/Distance_trial_2_"+target_list2[j]+".csv"
    with open(Distancetrial2csv,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in Distancetrial2[j]:
            writer.writerow([val])

    Distancetrial3csv="/home/cuebong/git/cri4/Distance_Data/Distance_trial_3_"+target_list2[j]+".csv"
    with open(Distancetrial3csv,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in Distancetrial3[j]:
            writer.writerow([val])

#____Calculating Duration_____#

Durationtrial1=[]
Durationtrial2=[]
Durationtrial3=[]

for j in xrange(0,38):
    Durationtrial1.append([])
    Durationtrial2.append([])
    Durationtrial3.append([])
    for i in xrange(0,20):
        for r in xrange(0,len(x[i][j])):
            if r==0:
                Durationtrial1[j].append(float(len(x[i][j][r]))/120)
            if r==1:
                Durationtrial2[j].append(float(len(x[i][j][r]))/120)
            if r==2:
                Durationtrial3[j].append(float(len(x[i][j][r]))/120)

for j in xrange(0,len(Durationtrial1)):
    Durationtrial1csv="/home/cuebong/git/cri4/Duration_Data/Duration_trial_1_"+target_list2[j]+".csv"
    with open(Durationtrial1csv,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in Durationtrial1[j]:
            writer.writerow([val])

    Durationtrial2csv="/home/cuebong/git/cri4/Duration_Data/Duration_trial_2_"+target_list2[j]+".csv"
    with open(Durationtrial2csv,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in Durationtrial2[j]:
            writer.writerow([val])

    Durationtrial3csv="/home/cuebong/git/cri4/Duration_Data/Duration_trial_3_"+target_list2[j]+".csv"
    with open(Durationtrial3csv,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in Durationtrial3[j]:
            writer.writerow([val])
"""        
#________________END_________________#
"""    
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
"""


"""
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

controlMTDVF=[]
controlMTDBF=[]
for i in xrange(0,len(C_VF_Var)):
    controlMTDVF.append([])
    controlMTDBF.append([])
    for j in xrange(0, len(C_VF_Var[i])):
        if C_VF_Var[i][j]!=0:
            controlMTDVF[i].append(C_VF_Var[i][j])
    for j in xrange(0,len(C_BF_Var[i])):
        if C_BF_Var[i][j]!=0:
            controlMTDBF[i].append(C_BF_Var[i][j])

patientVF=[]
controlVF=[]
patientBF=[]
controlBF=[]
HpatientVF=[]
HcontrolVF=[]
HpatientBF=[]
HcontrolBF=[]

for i in eliminate_list:
    if 'P01' in i or 'C01' in i:
        u=0
        v=0
    elif 'P02' in i or 'C03' in i:
        u=1
        v=1
    elif 'P03' in i or 'C04' in i:
        u=1
        v=1  
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

#hemPC=[2,3,6,7,8]
#NHPC=[0,1,4,5,9]
hemPC=[1] #change u and v!!!
NHPC=[0]
for i in hemPC:
    for j in xrange(0, len(P_VF_Var[i])):
        if P_VF_Var[i][j]!=0:
            HpatientVF.append(P_VF_Var[i][j])
            HcontrolVF.append(C_VF_Var[i][j])
    for j in xrange(0,len(P_BF_Var[i])):
        if P_BF_Var[i][j]!=0:
            HpatientBF.append(P_BF_Var[i][j])
            HcontrolBF.append(C_BF_Var[i][j])

for i in NHPC:
    for j in xrange(0,len(P_VF_Var[i])):
        if P_VF_Var[i][j]!=0:
            patientVF.append(P_VF_Var[i][j])
            controlVF.append(C_VF_Var[i][j])
    for j in xrange(0,len(P_BF_Var[i])):
        if P_BF_Var[i][j]!=0:
            patientBF.append(P_BF_Var[i][j])
            controlBF.append(C_BF_Var[i][j])
   
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
    
   # MTD2_Data[0][0].append(HpatientVF[i])
   # MTD2_Data[0][1].append(HpatientBF[i])
   # MTD2_Data[1][0].append(HcontrolVF[i])
   # MTD2_Data[1][1].append(HcontrolBF[i])  

  #  MTD2_Data[0][0].append(patientVF[i])
  #  MTD2_Data[0][1].append(patientBF[i])
  #  MTD2_Data[1][0].append(controlVF[i])
  #  MTD2_Data[1][1].append(controlBF[i])

#t1DoF3=(len(MTD1_Data[0][0])-1)*4
#t2DoF3=(len(MTD2_Data[0][0])-1)*4
#t3DoF3=(len(MTD3_Data[0][0])-1)*4

#test1_f,DoF1=ANOVA(MTD1_Data,t1DoF3)
#test2_f,DoF2=ANOVA(MTD2_Data,t2DoF3)
#test3_f,DoF3=ANOVA(MTD3_Data,t3DoF3)

meanVarxinterp, meanVaryinterp,meanVarX,meanVarY,mean_diff,unwanted_index=[],[],[],[],[],[]

for i in xrange(0,len(meanX)):
    meanVarxinterp.append([])
    meanVaryinterp.append([])
    meanVarX.append([])
    meanVarY.append([])
    unwanted_index.append([])
    for m in xrange(0,len(meanX[i])):
        if meanX[i][m]==0:
            meanVarxinterp[i].append(0)
            meanVaryinterp[i].append(0)
            meanVarX[i].append(0)
            meanVarY[i].append(0)
            unwanted_index[i].append(m)
            #if i<2:#change to 10
                #unwanted_index1.append(i+10)
            #elif i<20:
                #unwanted_index1.append(i-10)
        else:
            a, b, c, d, e= perform_spline(meanX[i][m],meanY[i][m])
            meanVarxinterp[i].append(b)
            meanVaryinterp[i].append(c)
            meanVarX[i].append(d)
            meanVarY[i].append(e)

P_resampled_meanX,C_resampled_meanX,P_resampled_meanY,C_resampled_meanY=[],[],[],[]
mean_diff=[]
intersubject_time=[]

for i in xrange(0,2):# change to 10
    P_resampled_meanX.append([])
    C_resampled_meanX.append([])
    P_resampled_meanY.append([])
    C_resampled_meanY.append([])
    mean_diff.append([])
    intersubject_time.append([])
    j=i+2 #change to 10
    for m in xrange(0,len(meanVarX[i])):
        if m in unwanted_index[i] or m in unwanted_index[j]:
            intersubject_time[i].append(0)
            P_resampled_meanX[i].append(0)
            C_resampled_meanX[i].append(0)
            P_resampled_meanY[i].append(0)
            C_resampled_meanY[i].append(0)
            mean_diff[i].append(0)
        else:
            P_resampled_meanX[i].append([])
            C_resampled_meanX[i].append([])
            P_resampled_meanY[i].append([])
            C_resampled_meanY[i].append([])
            mean_diff[i].append([])
            if len(sample[i][m])>len(sample[j][m]):
                intersubject_time[i].append(sample[j][m])
            else:
                intersubject_time[i].append(sample[i][m])
            for k in xrange(0, len(intersubject_time[i][m])):
                P_resampled_meanX[i][m].append(meanVarX[i][m][intersubject_time[i][m][k]*len(meanVarxinterp[i][m])])
                C_resampled_meanX[i][m].append(meanVarX[j][m][intersubject_time[i][m][k]*len(meanVarxinterp[j][m])])
                P_resampled_meanY[i][m].append(meanVarY[i][m][intersubject_time[i][m][k]*len(meanVaryinterp[i][m])]) 
                C_resampled_meanY[i][m].append(meanVarY[j][m][intersubject_time[i][m][k]*len(meanVaryinterp[j][m])])

            for l in xrange(0, len(intersubject_time[i][m])):
                diffX=P_resampled_meanX[i][m][l] - C_resampled_meanX[i][m][l]
                diffY=P_resampled_meanY[i][m][l] - C_resampled_meanY[i][m][l]
                mean_diff[i][m].append(((diffX**2)+(diffY**2))**0.5)

VF_index=[0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27,32,34,36]
BF_index=[4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31,33,35,37]

VF_MTS=[]
BF_MTS=[]

for i in xrange(0,len(mean_diff)):
    VF_MTS.append([])
    BF_MTS.append([])
    for m in xrange(0,len(mean_diff[i])):
        if mean_diff[i][m]==0:
            pass
        elif m in VF_index:
            VF_MTS[i].append(max(mean_diff[i][m]))
        elif m in BF_index:
            BF_MTS[i].append(max(mean_diff[i][m]))
                             
#VFt_test, VFDoF=T_test(patientVF,controlVF)
#BFt_test, BFDoF=T_test(patientBF,controlBF)
#HVFt_test, HVFDoF=T_test(HpatientVF,HcontrolVF)
#HBFt_test, HBFDoF=T_test(HpatientBF,HcontrolBF)
#print(VFt_test, VFDoF,BFt_test,BFDoF)
#print(HVFt_test, HVFDoF,HBFt_test,HBFDoF)

"""

#________START______________#

print("beginning mean trajectory calculations")
target_order=[0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27,32,34,36,4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31,33,35,37]

#______________START__________________#
"""

#_____________Global velocity mean calculations_______________#
globalvelmeansample, globalmeanvel=[],[]

for i in xrange (0,38):
    globalvelmeansample.append([])
    globalmeanvel.append([])

for j in target_order:
    globalvelnf=10000
    splinevel=[]
    splinevelval=[]
    meanvelvals=[]
    for i in xrange(0,20):
        e,f=perform_spline2(meanvel[i][j])
        splinevel.append(e)
        splinevelval.append(f)
        if len(velsample[i][j])<globalvelnf:
            globalvelnf=len(velsample[i][j])
    for t in xrange(0,globalvelnf):
        globalvelmeansample[j].append(Decimal(t)/globalvelnf)
        meanvelvals.append([])
        for i in xrange(0,20):
            meanvelvals[t].append(splinevelval[i][globalvelmeansample[j][t]*len(splinevel[i])])
        globalmeanvel[j].append(sum(meanvelvals[t])/float(20))

#_____________Obtaining Velocity Deviations_______________#
velTD=[]
velMTD=[]
velATD=[]

for j in xrange(0,38):
    velTD.append([])
    velMTD.append([])
    velATD.append([])
    for r in xrange(0,3):
        velTD[j].append([])
        velMTD[j].append([])
        velATD[j].append([])
        for i in xrange(0,20):
            velTD[j][r].append([])   
    for i in xrange(0,20):
        for r in xrange(0,len(velinterp[i][j])):
            resampled_ind_vel=[]
            for t in xrange(0, len(globalvelmeansample[j])):
                resampled_ind_vel.append(velvalue[i][j][r][globalvelmeansample[j][t]*len(velinterp[i][j][r])])
                velTD[j][r][i].append(sqrt((resampled_ind_vel[t]-globalmeanvel[j][t])**2))
            velMTD[j][r].append(max(velTD[j][r][i]))
            velATD[j][r].append(sum(velTD[j][r][i])/float(len(velTD[j][r][i])))
    
    for r in xrange(0,3):
        if r==0:
          MTDvelcsv="/home/cuebong/git/cri4/MTD data/Vel_MTD_"+target_list2[j]+"_1.csv"   
          with open(MTDvelcsv,"w") as output:
              writer=csv.writer(output,lineterminator='\n')
              for val in velMTD[j][r]:
                  writer.writerow([val])  

          ATDvelcsv="/home/cuebong/git/cri4/MTD data/Vel_ATD_"+target_list2[j]+"_1.csv"   
          with open(ATDvelcsv,"w") as output:
              writer=csv.writer(output,lineterminator='\n')
              for val in velATD[j][r]:
                  writer.writerow([val])  
        elif r==1:
          MTDvelcsv="/home/cuebong/git/cri4/MTD data/Vel_MTD_"+target_list2[j]+"_2.csv"   
          with open(MTDvelcsv,"w") as output:
              writer=csv.writer(output,lineterminator='\n')
              for val in velMTD[j][r]:
                  writer.writerow([val])  

          ATDvelcsv="/home/cuebong/git/cri4/MTD data/Vel_ATD_"+target_list2[j]+"_2.csv"   
          with open(ATDvelcsv,"w") as output:
              writer=csv.writer(output,lineterminator='\n')
              for val in velATD[j][r]:
                  writer.writerow([val])

        elif r==2:
          MTDvelcsv="/home/cuebong/git/cri4/MTD data/Vel_MTD_"+target_list2[j]+"_3.csv"   
          with open(MTDvelcsv,"w") as output:
              writer=csv.writer(output,lineterminator='\n')
              for val in velMTD[j][r]:
                  writer.writerow([val])  

          ATDvelcsv="/home/cuebong/git/cri4/MTD data/Vel_ATD_"+target_list2[j]+"_3.csv"   
          with open(ATDvelcsv,"w") as output:
              writer=csv.writer(output,lineterminator='\n')
              for val in velATD[j][r]:
                  writer.writerow([val])
#_______________END________________#
"""
"""
#_________________START_________________#

#______________Global mean calculations_______________#

globalmeansample,globalmeanX,globalmeanY=[],[],[]
patientmeanX,patientmeanY,controlmeanX,controlmeanY=[],[],[],[]
VFpatmeanX,VFpatmeanY,VFconmeanX,VFconmeanY=[],[],[],[]
BFpatmeanX,BFpatmeanY,BFconmeanX,BFconmeanY=[],[],[],[]

VFappend_index=0
BFappend_index=0

for j in xrange(0,19):
    VFpatmeanX.append([])
    VFpatmeanY.append([])
    VFconmeanX.append([])
    VFconmeanY.append([])
    BFpatmeanX.append([])
    BFpatmeanY.append([])
    BFconmeanX.append([])
    BFconmeanY.append([])

for i in xrange(0,38):
    globalmeansample.append([])
    globalmeanX.append([])
    globalmeanY.append([])
    patientmeanX.append([])
    patientmeanY.append([])
    controlmeanX.append([])
    controlmeanY.append([])

for j in target_order:
    globalnf=10000
    meanX_axis=[]
    meanY_axis=[]
    meanx=[]
    meany=[]
    meanxval=[]
    meanyval=[]
    patmeanX_axis=[]
    patmeanY_axis=[]
    conmeanX_axis=[]
    conmeanY_axis=[]
    VFpatmeanX_axis=[]
    VFpatmeanY_axis=[]
    VFconmeanX_axis=[]
    VFconmeanY_axis=[]
    BFpatmeanX_axis=[]
    BFpatmeanY_axis=[]
    BFconmeanX_axis=[]
    BFconmeanY_axis=[]
    for i in xrange(0,20):
        d,e,f,g,h=perform_spline(meanX[i][j],meanY[i][j])
        meanx.append(e)
        meany.append(f)
        meanxval.append(g)
        meanyval.append(h)
        if len(sample[i][j])<globalnf:
            globalnf=len(sample[i][j])
    for t in xrange(0,globalnf):
        globalmeansample[j].append(Decimal(t)/globalnf)
        meanX_axis.append([])
        meanY_axis.append([])
        patmeanX_axis.append([])
        patmeanY_axis.append([])
        conmeanX_axis.append([])
        conmeanY_axis.append([])
        VFpatmeanX_axis.append([])
        VFpatmeanY_axis.append([])
        VFconmeanX_axis.append([])
        VFconmeanY_axis.append([])
        BFpatmeanX_axis.append([])
        BFpatmeanY_axis.append([])
        BFconmeanX_axis.append([])
        BFconmeanY_axis.append([])

        for i in xrange(0,20):
            meanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
            meanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])
            if i in xrange(0,10):
                conmeanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
                conmeanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])   
                if j in (0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27,32,34,36):
                    VFconmeanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
                    VFconmeanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])
                else:
                    BFconmeanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
                    BFconmeanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])
            elif i in xrange(10,20):
                patmeanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
                patmeanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])
                if j in (0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27,32,34,36):
                    VFpatmeanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
                    VFpatmeanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])
                else:
                    BFpatmeanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
                    BFpatmeanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])

           
        globalmeanX[j].append(sum(meanX_axis[t])/20)
        globalmeanY[j].append(sum(meanY_axis[t])/20)
        patientmeanX[j].append(sum(patmeanX_axis[t])/10)
        patientmeanY[j].append(sum(patmeanY_axis[t])/10)
        controlmeanX[j].append(sum(conmeanX_axis[t])/10)
        controlmeanY[j].append(sum(conmeanY_axis[t])/10)
        if j in (0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27,32,34,36):
            VFpatmeanX[VFappend_index].append(sum(VFpatmeanX_axis[t])/10)
            VFpatmeanY[VFappend_index].append(sum(VFpatmeanY_axis[t])/10)
            VFconmeanX[VFappend_index].append(sum(VFconmeanX_axis[t])/10)
            VFconmeanY[VFappend_index].append(sum(VFconmeanY_axis[t])/10)
            if t==globalnf-1:
                VFappend_index=VFappend_index+1
        else:
            BFpatmeanX[BFappend_index].append(sum(BFpatmeanX_axis[t])/10)
            BFpatmeanY[BFappend_index].append(sum(BFpatmeanY_axis[t])/10)
            BFconmeanX[BFappend_index].append(sum(BFconmeanX_axis[t])/10)
            BFconmeanY[BFappend_index].append(sum(BFconmeanY_axis[t])/10) 
            if t==globalnf-1:
                BFappend_index=BFappend_index+1
"""
"""
#_________________START_________________#

#______________Subject mean calculations_______________#

globalmeansample,globalmeanX,globalmeanY=[],[],[]
patientmeanX,patientmeanY,controlmeanX,controlmeanY=[],[],[],[]


for j in xrange(0,38):
    globalmeansample.append([])
    globalmeanX.append([])
    globalmeanY.append([])
    patientmeanX.append([])
    patientmeanY.append([])
    controlmeanX.append([])
    controlmeanY.append([])
    for i in xrange(0,10):
       patientmeanX[j].append([])
       patientmeanY[j].append([])
       controlmeanX[j].append([])
       controlmeanY[j].append([]) 

for j in target_order:
    globalnf=10000
    meanX_axis=[]
    meanY_axis=[]
    meanx=[]
    meany=[]
    meanxval=[]
    meanyval=[]
    patmeanX_axis=[]
    patmeanY_axis=[]
    conmeanX_axis=[]
    conmeanY_axis=[]
    for i in xrange(0,20):
        d,e,f,g,h=perform_spline(meanX[i][j],meanY[i][j])
        meanx.append(e)
        meany.append(f)
        meanxval.append(g)
        meanyval.append(h)
        if len(sample[i][j])<globalnf:
            globalnf=len(sample[i][j])
    for t in xrange(0,globalnf):
        globalmeansample[j].append(Decimal(t)/globalnf)
        meanX_axis.append([])
        meanY_axis.append([])
        patmeanX_axis.append([])
        patmeanY_axis.append([])
        conmeanX_axis.append([])
        conmeanY_axis.append([])

        for i in xrange(0,20):
            meanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
            meanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])
            if i in xrange(0,10):
                conmeanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
                conmeanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])   

            elif i in xrange(10,20):
                patmeanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
                patmeanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])

           
        globalmeanX[j].append(sum(meanX_axis[t])/20)
        globalmeanY[j].append(sum(meanY_axis[t])/20)
        patientmeanX[j][i].append(sum(patmeanX_axis[t])/10)
        patientmeanY[j][i].append(sum(patmeanY_axis[t])/10)
        controlmeanX[j][i].append(sum(conmeanX_axis[t])/10)
        controlmeanY[j][i].append(sum(conmeanY_axis[t])/10)
"""
"""
#______________Obtaining trajectory separation(visual)______________#
patTS=[]
patMTS=[]
patATS=[]
conTS=[]
conMTS=[]
conATS=[]
VFpatsample=[]
VFpatX=[]
VFpatY=[]
VFpatxval=[]
VFpatyval=[]
BFpatsample=[]
BFpatX=[]
BFpatY=[]
BFpatxval=[]
BFpatyval=[]
VFconsample=[]
VFconX=[]
VFconY=[]
VFconxval=[]
VFconyval=[]
BFconsample=[]
BFconX=[]
BFconY=[]
BFconxval=[]
BFconyval=[]

for j in xrange(0,19):
    patTS.append([])
    conTS.append([])
    #VFpatsample.append([])
    #VFpatx.append([])
    #VFpatY.append([])
    #VFpatxval.append([])
    #VFpatyval.append([])
    #BFpatsample.append([])
   # BFpatX.append([])
    ##BFpatY.append([])
    #BFpatxval.append([])
    #BFpatyval.append([])
    d,e,f,g,h=perform_spline(VFpatmeanX[j],VFpatmeanY[j])
    VFpatsample.append(d)
    VFpatX.append(e)
    VFpatY.append(f)
    VFpatxval.append(g)
    VFpatyval.append(h)
    d,e,f,g,h=perform_spline(BFpatmeanX[j],BFpatmeanY[j])
    BFpatsample.append(d)
    BFpatX.append(e)
    BFpatY.append(f)
    BFpatxval.append(g)
    BFpatyval.append(h)
    if len(VFpatsample[j])<len(BFpatsample[j]):
        patnf=len(VFpatsample[j])
    else:
        patnf=len(BFpatsample[j])

    VFpatnormvalx=[]
    VFpatnormvaly=[]
    BFpatnormvalx=[]
    BFpatnormvaly=[]
    patsample=[]
    for frame in xrange(0,patnf):
        patsample.append(Decimal(frame)/patnf)
        VFpatnormvalx.append(VFpatxval[j][patsample[frame]*len(VFpatX[j])])
        VFpatnormvaly.append(VFpatyval[j][patsample[frame]*len(VFpatY[j])])
        BFpatnormvalx.append(BFpatxval[j][patsample[frame]*len(BFpatX[j])])
        BFpatnormvaly.append(BFpatyval[j][patsample[frame]*len(BFpatY[j])])

    for t in xrange(0,len(VFpatnormvalx)):
        patTSxsq=(float(VFpatnormvalx[t])-BFpatnormvalx[t])**2
        patTSysq=(float(VFpatnormvaly[t])-BFpatnormvaly[t])**2
        patTS_t=sqrt(float(patTSxsq+patTSysq))
        patTS[j].append(patTS_t)


    #VFconsample.append([])
    #VFconX.append([])
    #VFconY.append([])
    #VFconxval.append([])
    #VFconyval.append([])
    #BFconsample.append([])
    #BFconX.append([])
    #BFconY.append([])
    #BFconxval.append([])
    #BFconyval.append([])
    d,e,f,g,h=perform_spline(VFconmeanX[j],VFconmeanY[j])
    VFconsample.append(d)
    VFconX.append(e)
    VFconY.append(f)
    VFconxval.append(g)
    VFconyval.append(h)
    d,e,f,g,h=perform_spline(BFconmeanX[j],BFconmeanY[j])
    BFconsample.append(d)
    BFconX.append(e)
    BFconY.append(f)
    BFconxval.append(g)
    BFconyval.append(h)
    if len(VFconsample[j])<len(BFconsample[j]):
        connf=len(VFconsample[j])
    else:
        connf=len(BFconsample[j])

    VFconnormvalx=[]
    VFconnormvaly=[]
    BFconnormvalx=[]
    BFconnormvaly=[]
    consample=[]
    for frame in xrange(0,connf):
        consample.append(Decimal(frame)/connf)
        VFconnormvalx.append(VFconxval[j][consample[frame]*len(VFconX[j])])
        VFconnormvaly.append(VFconyval[j][consample[frame]*len(VFconY[j])])
        BFconnormvalx.append(BFconxval[j][consample[frame]*len(BFconX[j])])
        BFconnormvaly.append(BFconyval[j][consample[frame]*len(BFconY[j])])

    for t in xrange(0,len(VFconnormvalx)):
        conTSxsq=(float(VFconnormvalx[t])-BFconnormvalx[t])**2
        conTSysq=(float(VFconnormvaly[t])-BFconnormvaly[t])**2
        conTS_t=sqrt(float(conTSxsq+conTSysq))
        conTS[j].append(conTS_t)

    patMTS.append(max(patTS[j]))
    patATS.append(sum(patTS[j])/float(len(patTS[j])))
    
    conMTS.append(max(conTS[j]))
    conATS.append(sum(conTS[j])/float(len(conTS[j])))   

MTSpatcsv="/home/cuebong/git/cri4/MTS_ATS_Data/Patient_MTS.csv"   
with open(MTSpatcsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for val in patMTS:
        writer.writerow([val])

ATSpatcsv="/home/cuebong/git/cri4/MTS_ATS_Data/Patient_ATS.csv"   
with open(ATSpatcsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for val in patATS:
        writer.writerow([val]) 

MTSconcsv="/home/cuebong/git/cri4/MTS_ATS_Data/Control_MTS.csv"   
with open(MTSconcsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for val in conMTS:
        writer.writerow([val])

ATSconcsv="/home/cuebong/git/cri4/MTS_ATS_Data/Control_ATS.csv"   
with open(ATSconcsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for val in conATS:
        writer.writerow([val]) 
"""
#______________Obtaining paired trajectory separation_______________#
TS=[]
MTS=[]
ATS=[]

for j in xrange(0,38):
    TS.append([])
    MTS.append([])
    ATS.append([])
    for i in xrange(0,10):
        TS[j].append([])
        pairsample=[]
        patientmeanX=[]
        patientmeanY=[]
        controlmeanX=[]
        controlmeanY=[]
        con_num=int(i)
        pat_num=con_num+10
        d,e,f,g,h=perform_spline(meanX[con_num][j],meanY[con_num][j])
        conlength=d
        conmeanx=e
        conmeany=f
        conmeanxval=g
        conmeanyval=h
        d,e,f,g,h=perform_spline(meanX[pat_num][j],meanY[pat_num][j])
        patlength=d
        patmeanx=e
        patmeany=f
        patmeanxval=g
        patmeanyval=h
        if len(patlength)>len(conlength):
            pairlength=len(conlength)
        else:
            pairlength=len(patlength)
        for t in xrange(0,pairlength):
            pairsample.append(Decimal(t)/pairlength)
            patientmeanX.append(patmeanxval[pairsample[t]*len(patmeanx)])
            patientmeanY.append(patmeanyval[pairsample[t]*len(patmeany)])
            controlmeanX.append(conmeanxval[pairsample[t]*len(conmeanx)])
            controlmeanY.append(conmeanyval[pairsample[t]*len(conmeany)])
 
            TSxsq=(float(patientmeanX[t])-controlmeanX[t])**2
            TSysq=(float(patientmeanY[t])-controlmeanY[t])**2
            TS_t=sqrt(float(TSxsq+TSysq))
            TS[j][i].append(TS_t)

        MTS[j].append(max(TS[j][i]))
        ATS[j].append(sum(TS[j][i])/float(len(TS[j][i])))
"""
    MTScsv="/home/cuebong/git/cri4/MTS_ATS_Data/intrasubject/MTS_"+target_list2[j]+".csv"   
    with open(MTScsv,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in MTS[j]:
            writer.writerow([val])

    ATScsv="/home/cuebong/git/cri4/MTS_ATS_Data/intrasubject/ATS_"+target_list2[j]+".csv"
    with open(ATScsv,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in ATS[j]:
            writer.writerow([val])
"""

MTScsv="/home/cuebong/git/cri4/MTS_ATS_Data/intrasubject/MTS.csv"
with open(MTScsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for rownum in xrange(0,10):
        val=[]
        for j in xrange(0,38):
            val.append(MTS[j][rownum])
        writer.writerow([val[32],val[33],val[34],val[35],val[36],val[37],val[1],val[5],val[9],val[13],val[17],val[21],val[25],val[29],val[3],val[7],val[11],val[15],val[16],val[20],val[24],val[28],val[2],val[6],val[10],val[14],val[0],val[4],val[8],val[12],val[18],val[22],val[26],val[30],val[19],val[23],val[27],val[31]])

ATScsv="/home/cuebong/git/cri4/MTS_ATS_Data/intrasubject/ATS.csv"
with open(ATScsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for rownum in xrange(0,10):
        val=[]
        for j in xrange(0,38):
            val.append(ATS[j][rownum])
        writer.writerow([val[32],val[33],val[34],val[35],val[36],val[37],val[1],val[5],val[9],val[13],val[17],val[21],val[25],val[29],val[3],val[7],val[11],val[15],val[16],val[20],val[24],val[28],val[2],val[6],val[10],val[14],val[0],val[4],val[8],val[12],val[18],val[22],val[26],val[30],val[19],val[23],val[27],val[31]])



"""
#______________Obtaining trajectory separation(subject)_______________#
TS=[]
MTS=[[],[]]
ATS=[[],[]]

for j in xrange(0,38):
    TS.append([])
    for t in xrange(0,len(patientmeanX[j])):
        TSxsq=(float(patientmeanX[j][t])-controlmeanX[j][t])**2
        TSysq=(float(patientmeanY[j][t])-controlmeanY[j][t])**2
        TS_t=sqrt(float(TSxsq+TSysq))
        TS[j].append(TS_t)
    if j in (0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27,32,34,36):
        MTS[0].append(max(TS[j]))
        ATS[0].append(sum(TS[j])/float(len(TS[j])))
    else:
        MTS[1].append(max(TS[j]))
        ATS[1].append(sum(TS[j])/float(len(TS[j])))

MTSVFcsv="/home/cuebong/git/cri4/MTS_ATS_Data/MTS_VF.csv"   
with open(MTSVFcsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for val in MTS[0]:
        writer.writerow([val])

ATSVFcsv="/home/cuebong/git/cri4/MTS_ATS_Data/ATS_VF.csv"
with open(ATSVFcsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for val in ATS[0]:
        writer.writerow([val])

MTSBFcsv="/home/cuebong/git/cri4/MTS_ATS_Data/MTS_BF.csv"
with open(MTSBFcsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for val in MTS[1]:
        writer.writerow([val])

ATSBFcsv="/home/cuebong/git/cri4/MTS_ATS_Data/ATS_BF.csv"
with open(ATSBFcsv,"w") as output:
    writer=csv.writer(output,lineterminator='\n')
    for val in ATS[1]:
        writer.writerow([val])

#_______________END_________________#
"""


"""
#______________Obtaining Trajectory Deviation_________________#

TD=[[],[]]
HglobalMTD=[[[],[]],[[],[]]]
HglobalATD=[[[],[]],[[],[]]]
HvertglobalMTD=[[[],[]],[[],[]]]
HvertglobalATD=[[[],[]],[[],[]]]
HlowcurveglobalMTD=[[[],[]],[[],[]]]
HlowcurveglobalATD=[[[],[]],[[],[]]]
HmedcurveglobalMTD=[[[],[]],[[],[]]]
HmedcurveglobalATD=[[[],[]],[[],[]]]
HhicurveglobalMTD=[[[],[]],[[],[]]]
HhicurveglobalATD=[[[],[]],[[],[]]]
globalMTD=[[[],[]],[[],[]]]
globalATD=[[[],[]],[[],[]]]
vertglobalMTD=[[[],[]],[[],[]]]
vertglobalATD=[[[],[]],[[],[]]]
lowcurveglobalMTD=[[[],[]],[[],[]]]
lowcurveglobalATD=[[[],[]],[[],[]]]
medcurveglobalMTD=[[[],[]],[[],[]]]
medcurveglobalATD=[[[],[]],[[],[]]]
hicurveglobalMTD=[[[],[]],[[],[]]]
hicurveglobalATD=[[[],[]],[[],[]]]


hemPC=[2,3,6,7,8,12,13,16,17,18]
NHPC=[0,1,4,5,9,10,11,14,15,19]
vert=[16,17,18]
low_curve=[1,5,9,13]
med_curve=[0,3,4,7,8,11,12,15]
hi_curve=[2,6,10,14]

for j in xrange(0,19):
    TD[0].append([])
    TD[1].append([])
    l=target_order[j]
    m=target_order[j+19]
    for i in xrange(0,20):
        TD[0][j].append([])
        TD[1][j].append([])
        x_td=[[],[]]
        y_td=[[],[]]
        for t in xrange(0,len(globalmeansample[l])):
            x_td[0].append([])
            y_td[0].append([])
            function=[[],[]]
            for r in xrange(len(x[i][l])):
                x_td[0][t].append(xvalues[i][l][r][globalmeansample[l][t]*len(x[i][l][r])])
                y_td[0][t].append(yvalues[i][l][r][globalmeansample[l][t]*len(y[i][l][r])])
                function[0].append((x_td[0][t][r]-globalmeanX[l][t])**2+(y_td[0][t][r]-globalmeanY[l][t])**2)
            
            td_calc1=sqrt((float(1)/(len(x[i][l])-1))*sum(function[0]))
            TD[0][j][i].append(td_calc1)

        for t in xrange(0,len(globalmeansample[m])):
            x_td[1].append([])
            y_td[1].append([])
            function=[[],[]]
            for r in xrange(len(x[i][m])):
                x_td[1][t].append(xvalues[i][m][r][globalmeansample[m][t]*len(x[i][m][r])])
                y_td[1][t].append(yvalues[i][m][r][globalmeansample[m][t]*len(y[i][m][r])])
                function[1].append((x_td[1][t][r]-globalmeanX[m][t])**2+(y_td[1][t][r]-globalmeanY[m][t])**2)
        
            td_calc2=sqrt((float(1)/(len(x[i][m])-1))*sum(function[1])) 
            TD[1][j][i].append(td_calc2)



    
                
#_______Extract MTD and ATD_________#

        if i in hemPC:
            if i in xrange(0,10):
                HglobalMTD[0][0].append(max(TD[0][j][i]))
                HglobalMTD[1][0].append(max(TD[1][j][i]))
                HglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                HglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                if l in vert:
                    HvertglobalMTD[0][0].append(max(TD[0][j][i]))
                    HvertglobalMTD[1][0].append(max(TD[1][j][i]))
                    HvertglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    HvertglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                elif l in low_curve:
                    HlowcurveglobalMTD[0][0].append(max(TD[0][j][i]))
                    HlowcurveglobalMTD[1][0].append(max(TD[1][j][i]))
                    HlowcurveglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    HlowcurveglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                elif l in med_curve:
                    HmedcurveglobalMTD[0][0].append(max(TD[0][j][i]))
                    HmedcurveglobalMTD[1][0].append(max(TD[1][j][i]))
                    HmedcurveglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    HmedcurveglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                else:
                    HhicurveglobalMTD[0][0].append(max(TD[0][j][i]))
                    HhicurveglobalMTD[1][0].append(max(TD[1][j][i]))
                    HhicurveglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    HhicurveglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))

            elif i in xrange(10,20):
                HglobalMTD[0][1].append(max(TD[0][j][i]))
                HglobalMTD[1][1].append(max(TD[1][j][i]))
                HglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                HglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                if l in vert:
                    HvertglobalMTD[0][1].append(max(TD[0][j][i]))
                    HvertglobalMTD[1][1].append(max(TD[1][j][i]))
                    HvertglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    HvertglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                elif l in low_curve:
                    HlowcurveglobalMTD[0][1].append(max(TD[0][j][i]))
                    HlowcurveglobalMTD[1][1].append(max(TD[1][j][i]))
                    HlowcurveglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    HlowcurveglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                elif l in med_curve:
                    HmedcurveglobalMTD[0][1].append(max(TD[0][j][i]))
                    HmedcurveglobalMTD[1][1].append(max(TD[1][j][i]))
                    HmedcurveglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    HmedcurveglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                else:
                    HhicurveglobalMTD[0][1].append(max(TD[0][j][i]))
                    HhicurveglobalMTD[1][1].append(max(TD[1][j][i]))
                    HhicurveglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    HhicurveglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))


        elif i in NHPC:
            if i in xrange(0,10):
                globalMTD[0][0].append(max(TD[0][j][i]))
                globalMTD[1][0].append(max(TD[1][j][i]))
                globalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                globalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                if l in vert:
                    vertglobalMTD[0][0].append(max(TD[0][j][i]))
                    vertglobalMTD[1][0].append(max(TD[1][j][i]))
                    vertglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    vertglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                elif l in low_curve:
                    lowcurveglobalMTD[0][0].append(max(TD[0][j][i]))
                    lowcurveglobalMTD[1][0].append(max(TD[1][j][i]))
                    lowcurveglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    lowcurveglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                elif l in med_curve:
                    medcurveglobalMTD[0][0].append(max(TD[0][j][i]))
                    medcurveglobalMTD[1][0].append(max(TD[1][j][i]))
                    medcurveglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    medcurveglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                else:
                    hicurveglobalMTD[0][0].append(max(TD[0][j][i]))
                    hicurveglobalMTD[1][0].append(max(TD[1][j][i]))
                    hicurveglobalATD[0][0].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    hicurveglobalATD[1][0].append(sum(TD[1][j][i])/len(TD[1][j][i]))

            elif i in xrange(10,20):
                globalMTD[0][1].append(max(TD[0][j][i]))
                globalMTD[1][1].append(max(TD[1][j][i]))
                globalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                globalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                if l in vert:
                    vertglobalMTD[0][1].append(max(TD[0][j][i]))
                    vertglobalMTD[1][1].append(max(TD[1][j][i]))
                    vertglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    vertglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                elif l in low_curve:
                    lowcurveglobalMTD[0][1].append(max(TD[0][j][i]))
                    lowcurveglobalMTD[1][1].append(max(TD[1][j][i]))
                    lowcurveglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    lowcurveglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                elif l in med_curve:
                    medcurveglobalMTD[0][1].append(max(TD[0][j][i]))
                    medcurveglobalMTD[1][1].append(max(TD[1][j][i]))
                    medcurveglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    medcurveglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))
                else:
                    hicurveglobalMTD[0][1].append(max(TD[0][j][i]))
                    hicurveglobalMTD[1][1].append(max(TD[1][j][i]))
                    hicurveglobalATD[0][1].append(sum(TD[0][j][i])/len(TD[0][j][i]))
                    hicurveglobalATD[1][1].append(sum(TD[1][j][i])/len(TD[1][j][i]))     
"""
#_______________END____________________#
     
"""
for j in xrange(0,19):
    l=target_order[j]
    k=j+19
    m=target_order[k]
    x_count1=0
    x_count2=0
    f1,targetplots=plt.subplots(10,2,figsize=(15,60))###
    for i in xrange(0,20):###
        if i in xrange(0,10):###
            y_count=0
            x_count=x_count1
        elif i in xrange(10,20):###
            y_count=1
            x_count=x_count2
        #if meanX[i][l]!=0:
        targetplots[x_count,y_count].plot(meanX[i][l],meanY[i][l])
        targetplots[x_count,y_count].set_title(subjects[i])
        if len(Xax[i][l])==3:
            a=variance_ellipse(sample[i][l],Xax[i][l][0],Xax[i][l][1],Xax[i][l][2],Yax[i][l][0],Yax[i][l][1],Yax[i][l][2],x_count,y_count,targetplots,1)
        else:
            a=variance_ellipse_2(sample[i][l],Xax[i][l][0],Xax[i][l][1],Yax[i][l][0],Yax[i][l][1],x_count,y_count,targetplots,1)
        #else:
            #targetplots[x_count,y_count].plot(0,0)
            #targetplots[x_count,y_count].set_title(subjects[i])
        #if meanX[i][m]!=0:
        targetplots[x_count,y_count].plot(meanX[i][m],meanY[i][m])
        if len(Xax[i][m])==3:
            a=variance_ellipse(sample[i][m],Xax[i][m][0],Xax[i][m][1],Xax[i][m][2],Yax[i][m][0],Yax[i][m][1],Yax[i][m][2],x_count,y_count,targetplots,2)
        else:
            a=variance_ellipse_2_2(sample[i][m],Xax[i][m][0],Xax[i][m][1],Yax[i][m][0],Yax[i][m][1],x_count,y_count,targetplots,2)
        if i in xrange(0,10):###
           x_count1=x_count1+1
        elif i in xrange(10,20):###
            x_count2=x_count2+1
        targetplots[x_count,y_count].set_xlim(0,4.5)
        targetplots[x_count,y_count].set_ylim(0,6)
        targetplots[x_count,y_count].set_aspect('equal')
    f1.savefig("/home/cuebong/git/cri4/Trajectory_Plots/Combined/trajectory_plots_"+target_list[j])
    plt.close()


for j in xrange(0,19):
    l=target_order[j]
    k=j+19
    m=target_order[k]
    x_count1=0
    x_count2=0
    f2,velplots=plt.subplots(2,2,figsize=(15,60))###
    for i in xrange(0,20):###
        if i in xrange(0,10):###
            y_count=0
            x_count=x_count1
        elif i in xrange(10,20):###
            y_count=1
            x_count=x_count2
        #if meanX[i][l]!=0
        velplots[x_count,y_count].plot(velsample[i][l],meanvel[i][l])
        velplots[x_count,y_count].set_title(subjects[i])
        if len(velax[i][l])==3:
            a=variance_ellipse2(velsample[i][l],velax[i][l][0],velax[i][l][1],velax[i][l][2],x_count,y_count,velplots,1)
        else:
            a=variance_ellipse2_2(velsample[i][l],velax[i][l][0],velax[i][l][1],x_count,y_count,velplots,1)
        #else:
            #velplots[x_count,y_count].plot(0,0)
            #velplots[x_count,y_count].set_title(subjects[i])
        #if meanX[i][m]!=0:
        velplots[x_count,y_count].plot(velsample[i][m],meanvel[i][m])
        if len(velax[i][m])==3:
            a=variance_ellipse2(velsample[i][m],velax[i][m][0],velax[i][m][1],velax[i][m][2],x_count,y_count,velplots,2)
        else:
            a=variance_ellipse2_2(velsample[i][m],velax[i][m][0],velax[i][m][1],x_count,y_count,velplots,2)

        if i in xrange(0,10):###
           x_count1=x_count1+1
        elif i in xrange(10,20):###
            x_count2=x_count2+1
        velplots[x_count,y_count].set_xlim(0,1)
        velplots[x_count,y_count].set_ylim(0,1.6)
        velplots[x_count,y_count].set_aspect('equal')
    f2.savefig("/home/cuebong/git/cri4/Trajectory_Plots/Velocity_Plots/velocity_profiles_"+target_list[j])
    plt.close()
"""
"""    
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
"""
"""
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
"""

#______________START________________#
"""
#_______Calculating individual MTD/ATD_________#

MTDtarget_file=[]
ATDtarget_file=[]
ind_TD=[]
indiv_x=[]
indiv_y=[]
indiv_x.append([])
indiv_x.append([])
indiv_y.append([])
indiv_y.append([])
indiv_function=[]
indiv_function.append([])
indiv_function.append([])
for k in xrange(0,38):
    MTDtarget_file.append([])
    ind_TD.append([])
    ATDtarget_file.append([])
for j in xrange(0,19):
    l=target_order[j]
    m=target_order[j+19]
    for i in xrange(0,20):
        ind_TD[l].append([])
        ind_TD[m].append([])
        for r in xrange(0, len(x[i][l])):
            indiv_x=[]
            indiv_y=[]
            indiv_x.append([])
            indiv_x.append([])
            indiv_y.append([])
            indiv_y.append([])
            indiv_function=[]
            indiv_function.append([])
            indiv_function.append([])
            ind_TD[l][i].append([])
            for t in xrange(len(globalmeansample[l])):
                indiv_x[0].append(xvalues[i][l][r][globalmeansample[l][t]*len(x[i][l][r])])
                indiv_y[0].append(yvalues[i][l][r][globalmeansample[l][t]*len(y[i][l][r])])
                indiv_function[0].append((indiv_x[0][t]-globalmeanX[l][t])**2+(indiv_y[0][t]-globalmeanY[l][t])**2)
                ind_TD[l][i][r].append(sqrt(float(indiv_function[0][t])))

            MTDtarget_file[l].append(max(ind_TD[l][i][r]))
            ATDtarget_file[l].append(float(sum(ind_TD[l][i][r]))/len(ind_TD[l][i][r]))
        for r in xrange(0, len(x[i][m])):
            ind_TD[m][i].append([])
            indiv_x=[]
            indiv_y=[]
            indiv_x.append([])
            indiv_x.append([])
            indiv_y.append([])
            indiv_y.append([])
            indiv_function=[]
            indiv_function.append([])
            indiv_function.append([])
            for t in xrange(len(globalmeansample[m])):
                indiv_x[1].append(xvalues[i][m][r][globalmeansample[m][t]*len(x[i][m][r])])
                indiv_y[1].append(yvalues[i][m][r][globalmeansample[m][t]*len(y[i][m][r])])
                indiv_function[1].append((indiv_x[1][t]-globalmeanX[m][t])**2+(indiv_y[1][t]-globalmeanY[m][t])**2)
                ind_TD[m][i][r].append(sqrt(float(indiv_function[1][t])))

            MTDtarget_file[m].append(max(ind_TD[m][i][r]))
            ATDtarget_file[m].append(float(sum(ind_TD[m][i][r]))/len(ind_TD[m][i][r]))          


for j in xrange(0,len(MTDtarget_file)):
    MTDcsvfile="/home/cuebong/git/cri4/MTD data/statstable/MTD_data_"+target_list2[j]+".csv"
    with open(MTDcsvfile,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in MTDtarget_file[j]:
            writer.writerow([val])

    ATDcsvfile="/home/cuebong/git/cri4/MTD data/statstable/ATD_data_"+target_list2[j]+".csv"
    with open(ATDcsvfile,"w") as output:
        writer=csv.writer(output,lineterminator='\n')
        for val in ATDtarget_file[j]:
            writer.writerow([val])

   
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
                                        
for i in xrange(0,len(globalMTD[0][0])):
    MTD1_Data[0][0].append(globalMTD[0][1][i])
    MTD1_Data[0][0].append(HglobalMTD[0][1][i])
    MTD1_Data[0][1].append(globalMTD[1][1][i])
    MTD1_Data[0][1].append(HglobalMTD[1][1][i])
    MTD1_Data[1][0].append(globalMTD[0][0][i])
    MTD1_Data[1][0].append(HglobalMTD[0][0][i])
    MTD1_Data[1][1].append(globalMTD[1][0][i])
    MTD1_Data[1][1].append(HglobalMTD[1][0][i])
    
    MTD2_Data[0][0].append(HglobalMTD[0][1][i])
    MTD2_Data[0][1].append(HglobalMTD[1][1][i])
    MTD2_Data[1][0].append(HglobalMTD[0][0][i])
    MTD2_Data[1][1].append(HglobalMTD[1][0][i])  

    MTD3_Data[0][0].append(globalMTD[0][1][i])
    MTD3_Data[0][1].append(globalMTD[1][1][i])
    MTD3_Data[1][0].append(globalMTD[0][0][i])
    MTD3_Data[1][1].append(globalMTD[1][0][i])

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

for i in xrange(0,len(vertglobalMTD[0][0])):
    vertMTD1_Data[0][0].append(vertglobalMTD[0][1][i])
    vertMTD1_Data[0][0].append(HvertglobalMTD[0][1][i])
    vertMTD1_Data[0][1].append(vertglobalMTD[1][1][i])
    vertMTD1_Data[0][1].append(HvertglobalMTD[1][1][i])
    vertMTD1_Data[1][0].append(vertglobalMTD[0][0][i])
    vertMTD1_Data[1][0].append(HvertglobalMTD[0][0][i])
    vertMTD1_Data[1][1].append(vertglobalMTD[1][0][i])
    vertMTD1_Data[1][1].append(HvertglobalMTD[1][0][i])
    vertMTD2_Data[0][0].append(HvertglobalMTD[0][1][i])
    vertMTD2_Data[0][1].append(HvertglobalMTD[1][1][i])
    vertMTD2_Data[1][0].append(HvertglobalMTD[0][0][i])
    vertMTD2_Data[1][1].append(HvertglobalMTD[1][0][i]) 
    vertMTD3_Data[0][0].append(vertglobalMTD[0][1][i])
    vertMTD3_Data[0][1].append(vertglobalMTD[1][1][i])
    vertMTD3_Data[1][0].append(vertglobalMTD[0][0][i])
    vertMTD3_Data[1][1].append(vertglobalMTD[1][0][i])
                                        
vertt1DoF3=(len(vertMTD1_Data[0][0])-1)*4
vertt2DoF3=(len(vertMTD2_Data[0][0])-1)*4
vertt3DoF3=(len(vertMTD3_Data[0][0])-1)*4

verttest1_f,vertDoF1,verteffPC1,verteffV1=ANOVA(vertMTD1_Data,vertt1DoF3)
verttest2_f,vertDoF2,verteffPC2,verteffV2=ANOVA(vertMTD2_Data,vertt2DoF3)
verttest3_f,vertDoF3,verteffPC3,verteffV3=ANOVA(vertMTD3_Data,vertt3DoF3)

lowcurveMTD1_Data, lowcurveMTD2_Data,lowcurveMTD3_Data=[],[],[]
lowcurveMTD1_Data.append([])
lowcurveMTD1_Data.append([])
lowcurveMTD1_Data[0].append([])
lowcurveMTD1_Data[0].append([])
lowcurveMTD1_Data[1].append([])
lowcurveMTD1_Data[1].append([])
lowcurveMTD2_Data.append([])
lowcurveMTD2_Data.append([])
lowcurveMTD2_Data[0].append([])
lowcurveMTD2_Data[0].append([])
lowcurveMTD2_Data[1].append([])
lowcurveMTD2_Data[1].append([])
lowcurveMTD3_Data.append([])
lowcurveMTD3_Data.append([])
lowcurveMTD3_Data[0].append([])
lowcurveMTD3_Data[0].append([])
lowcurveMTD3_Data[1].append([])
lowcurveMTD3_Data[1].append([])

for i in xrange(0,len(lowcurveglobalMTD[0][0])):
    lowcurveMTD1_Data[0][0].append(lowcurveglobalMTD[0][1][i])
    lowcurveMTD1_Data[0][0].append(HlowcurveglobalMTD[0][1][i])
    lowcurveMTD1_Data[0][1].append(lowcurveglobalMTD[1][1][i])
    lowcurveMTD1_Data[0][1].append(HlowcurveglobalMTD[1][1][i])
    lowcurveMTD1_Data[1][0].append(lowcurveglobalMTD[0][0][i])
    lowcurveMTD1_Data[1][0].append(HlowcurveglobalMTD[0][0][i])
    lowcurveMTD1_Data[1][1].append(lowcurveglobalMTD[1][0][i])
    lowcurveMTD1_Data[1][1].append(HlowcurveglobalMTD[1][0][i])
    lowcurveMTD2_Data[0][0].append(HlowcurveglobalMTD[0][1][i])
    lowcurveMTD2_Data[0][1].append(HlowcurveglobalMTD[1][1][i])
    lowcurveMTD2_Data[1][0].append(HlowcurveglobalMTD[0][0][i])
    lowcurveMTD2_Data[1][1].append(HlowcurveglobalMTD[1][0][i]) 
    lowcurveMTD3_Data[0][0].append(lowcurveglobalMTD[0][1][i])
    lowcurveMTD3_Data[0][1].append(lowcurveglobalMTD[1][1][i])
    lowcurveMTD3_Data[1][0].append(lowcurveglobalMTD[0][0][i])
    lowcurveMTD3_Data[1][1].append(lowcurveglobalMTD[1][0][i])
                                        
lowcurvet1DoF3=(len(lowcurveMTD1_Data[0][0])-1)*4
lowcurvet2DoF3=(len(lowcurveMTD2_Data[0][0])-1)*4
lowcurvet3DoF3=(len(lowcurveMTD3_Data[0][0])-1)*4

lowcurvetest1_f,lowcurveDoF1,lowcurveeffPC1,lowcurveeffV1=ANOVA(lowcurveMTD1_Data,lowcurvet1DoF3)
lowcurvetest2_f,lowcurveDoF2,lowcurveeffPC2,lowcurveeffV2=ANOVA(lowcurveMTD2_Data,lowcurvet2DoF3)
lowcurvetest3_f,lowcurveDoF3,lowcurveeffPC3,lowcurveeffV3=ANOVA(lowcurveMTD3_Data,lowcurvet3DoF3)


medcurveMTD1_Data, medcurveMTD2_Data,medcurveMTD3_Data=[],[],[]
medcurveMTD1_Data.append([])
medcurveMTD1_Data.append([])
medcurveMTD1_Data[0].append([])
medcurveMTD1_Data[0].append([])
medcurveMTD1_Data[1].append([])
medcurveMTD1_Data[1].append([])
medcurveMTD2_Data.append([])
medcurveMTD2_Data.append([])
medcurveMTD2_Data[0].append([])
medcurveMTD2_Data[0].append([])
medcurveMTD2_Data[1].append([])
medcurveMTD2_Data[1].append([])
medcurveMTD3_Data.append([])
medcurveMTD3_Data.append([])
medcurveMTD3_Data[0].append([])
medcurveMTD3_Data[0].append([])
medcurveMTD3_Data[1].append([])
medcurveMTD3_Data[1].append([])

for i in xrange(0,len(medcurveglobalMTD[0][0])):
    medcurveMTD1_Data[0][0].append(medcurveglobalMTD[0][1][i])
    medcurveMTD1_Data[0][0].append(HmedcurveglobalMTD[0][1][i])
    medcurveMTD1_Data[0][1].append(medcurveglobalMTD[1][1][i])
    medcurveMTD1_Data[0][1].append(HmedcurveglobalMTD[1][1][i])
    medcurveMTD1_Data[1][0].append(medcurveglobalMTD[0][0][i])
    medcurveMTD1_Data[1][0].append(HmedcurveglobalMTD[0][0][i])
    medcurveMTD1_Data[1][1].append(medcurveglobalMTD[1][0][i])
    medcurveMTD1_Data[1][1].append(HmedcurveglobalMTD[1][0][i])
    medcurveMTD2_Data[0][0].append(HmedcurveglobalMTD[0][1][i])
    medcurveMTD2_Data[0][1].append(HmedcurveglobalMTD[1][1][i])
    medcurveMTD2_Data[1][0].append(HmedcurveglobalMTD[0][0][i])
    medcurveMTD2_Data[1][1].append(HmedcurveglobalMTD[1][0][i]) 
    medcurveMTD3_Data[0][0].append(medcurveglobalMTD[0][1][i])
    medcurveMTD3_Data[0][1].append(medcurveglobalMTD[1][1][i])
    medcurveMTD3_Data[1][0].append(medcurveglobalMTD[0][0][i])
    medcurveMTD3_Data[1][1].append(medcurveglobalMTD[1][0][i])
                                        
medcurvet1DoF3=(len(medcurveMTD1_Data[0][0])-1)*4
medcurvet2DoF3=(len(medcurveMTD2_Data[0][0])-1)*4
medcurvet3DoF3=(len(medcurveMTD3_Data[0][0])-1)*4

medcurvetest1_f,medcurveDoF1,medcurveeffPC1,medcurveeffV1=ANOVA(medcurveMTD1_Data,medcurvet1DoF3)
medcurvetest2_f,medcurveDoF2,medcurveeffPC2,medcurveeffV2=ANOVA(medcurveMTD2_Data,medcurvet2DoF3)
medcurvetest3_f,medcurveDoF3,medcurveeffPC3,medcurveeffV3=ANOVA(medcurveMTD3_Data,medcurvet3DoF3)

hicurveMTD1_Data, hicurveMTD2_Data,hicurveMTD3_Data=[],[],[]
hicurveMTD1_Data.append([])
hicurveMTD1_Data.append([])
hicurveMTD1_Data[0].append([])
hicurveMTD1_Data[0].append([])
hicurveMTD1_Data[1].append([])
hicurveMTD1_Data[1].append([])
hicurveMTD2_Data.append([])
hicurveMTD2_Data.append([])
hicurveMTD2_Data[0].append([])
hicurveMTD2_Data[0].append([])
hicurveMTD2_Data[1].append([])
hicurveMTD2_Data[1].append([])
hicurveMTD3_Data.append([])
hicurveMTD3_Data.append([])
hicurveMTD3_Data[0].append([])
hicurveMTD3_Data[0].append([])
hicurveMTD3_Data[1].append([])
hicurveMTD3_Data[1].append([])

for i in xrange(0,len(hicurveglobalMTD[0][0])):
    hicurveMTD1_Data[0][0].append(hicurveglobalMTD[0][1][i])
    hicurveMTD1_Data[0][0].append(HhicurveglobalMTD[0][1][i])
    hicurveMTD1_Data[0][1].append(hicurveglobalMTD[1][1][i])
    hicurveMTD1_Data[0][1].append(HhicurveglobalMTD[1][1][i])
    hicurveMTD1_Data[1][0].append(hicurveglobalMTD[0][0][i])
    hicurveMTD1_Data[1][0].append(HhicurveglobalMTD[0][0][i])
    hicurveMTD1_Data[1][1].append(hicurveglobalMTD[1][0][i])
    hicurveMTD1_Data[1][1].append(HhicurveglobalMTD[1][0][i])
    hicurveMTD2_Data[0][0].append(HhicurveglobalMTD[0][1][i])
    hicurveMTD2_Data[0][1].append(HhicurveglobalMTD[1][1][i])
    hicurveMTD2_Data[1][0].append(HhicurveglobalMTD[0][0][i])
    hicurveMTD2_Data[1][1].append(HhicurveglobalMTD[1][0][i]) 
    hicurveMTD3_Data[0][0].append(hicurveglobalMTD[0][1][i])
    hicurveMTD3_Data[0][1].append(hicurveglobalMTD[1][1][i])
    hicurveMTD3_Data[1][0].append(hicurveglobalMTD[0][0][i])
    hicurveMTD3_Data[1][1].append(hicurveglobalMTD[1][0][i])

                                        
hicurvet1DoF3=(len(hicurveMTD1_Data[0][0])-1)*4
hicurvet2DoF3=(len(hicurveMTD2_Data[0][0])-1)*4
hicurvet3DoF3=(len(hicurveMTD3_Data[0][0])-1)*4

hicurvetest1_f,hicurveDoF1,hicurveeffPC1,hicurveeffV1=ANOVA(hicurveMTD1_Data,hicurvet1DoF3)
hicurvetest2_f,hicurveDoF2,hicurveeffPC2,hicurveeffV2=ANOVA(hicurveMTD2_Data,hicurvet2DoF3)
hicurvetest3_f,hicurveDoF3,hicurveeffPC3,hicurveeffV3=ANOVA(hicurveMTD3_Data,hicurvet3DoF3)

Anovagroup=[MTD1_Data,MTD2_Data,MTD3_Data,vertMTD1_Data,vertMTD2_Data,vertMTD3_Data,lowcurveMTD1_Data,lowcurveMTD2_Data,lowcurveMTD3_Data,medcurveMTD1_Data,medcurveMTD2_Data,medcurveMTD3_Data,hicurveMTD1_Data,hicurveMTD2_Data,hicurveMTD3_Data]
    
csv_names=['all','hem','non-hem','straight-all','straight-hem','straight-non-hem','lowcurve-all','lowcurve-hem','lowcurve-non-hem','medcurve-all','medcurve-hem','medcurve-non-hem','hicurve-all','hicurve-hem','hicurve-non-hem']
MTD_csv_data=[[MTD1_Data[0][0],MTD1_Data[0][1],MTD1_Data[1][0],MTD1_Data[1][1]],[MTD2_Data[0][0],MTD2_Data[0][1],MTD2_Data[1][0],MTD2_Data[1][1]],[MTD3_Data[0][0],MTD3_Data[0][1],MTD3_Data[1][0],MTD3_Data[1][1]],[vertMTD1_Data[0][0],vertMTD1_Data[0][1],vertMTD1_Data[1][0],vertMTD1_Data[1][1]],[vertMTD2_Data[0][0],vertMTD2_Data[0][1],vertMTD2_Data[1][0],vertMTD2_Data[1][1]],[vertMTD3_Data[0][0],vertMTD3_Data[0][1],vertMTD3_Data[1][0],vertMTD3_Data[1][1]],[lowcurveMTD1_Data[0][0],lowcurveMTD1_Data[0][1],lowcurveMTD1_Data[1][0],lowcurveMTD1_Data[1][1]],[lowcurveMTD2_Data[0][0],lowcurveMTD2_Data[0][1],lowcurveMTD2_Data[1][0],lowcurveMTD2_Data[1][1]],[lowcurveMTD3_Data[0][0],lowcurveMTD3_Data[0][1],lowcurveMTD3_Data[1][0],lowcurveMTD3_Data[1][1]],[medcurveMTD1_Data[0][0],medcurveMTD1_Data[0][1],medcurveMTD1_Data[1][0],medcurveMTD1_Data[1][1]],[medcurveMTD2_Data[0][0],medcurveMTD2_Data[0][1],medcurveMTD2_Data[1][0],medcurveMTD2_Data[1][1]],[medcurveMTD3_Data[0][0],medcurveMTD3_Data[0][1],medcurveMTD3_Data[1][0],medcurveMTD3_Data[1][1]],[hicurveMTD1_Data[0][0],hicurveMTD1_Data[0][1],hicurveMTD1_Data[1][0],hicurveMTD1_Data[1][1]],[hicurveMTD2_Data[0][0],hicurveMTD2_Data[0][1],hicurveMTD2_Data[1][0],hicurveMTD2_Data[1][1]],[hicurveMTD3_Data[0][0],hicurveMTD3_Data[0][1],hicurveMTD3_Data[1][0],hicurveMTD3_Data[1][1]]]

for i in xrange(0,len(csv_names)):
    for j in xrange(0,len(MTD_csv_data[i])):
        csvfile="/home/cuebong/git/cri4/MTD data/MTD_data"+csv_names[i]+str(j+1)+".csv"
        with open(csvfile,"w") as output:
            writer=csv.writer(output,lineterminator='\n')
            for val in MTD_csv_data[i][j]:
                writer.writerow([val])


ATD1_Data, ATD2_Data, ATD3_Data=[],[],[]
ATD1_Data.append([])
ATD1_Data.append([])
ATD1_Data[0].append([])
ATD1_Data[0].append([])
ATD1_Data[1].append([])
ATD1_Data[1].append([])
ATD2_Data.append([])
ATD2_Data.append([])
ATD2_Data[0].append([])
ATD2_Data[0].append([])
ATD2_Data[1].append([])
ATD2_Data[1].append([])
ATD3_Data.append([])
ATD3_Data.append([])
ATD3_Data[0].append([])
ATD3_Data[0].append([])
ATD3_Data[1].append([])
ATD3_Data[1].append([])
                                        
for i in xrange(0,len(globalATD[0][0])):
    ATD1_Data[0][0].append(globalATD[0][1][i])
    ATD1_Data[0][0].append(HglobalATD[0][1][i])
    ATD1_Data[0][1].append(globalATD[1][1][i])
    ATD1_Data[0][1].append(HglobalATD[1][1][i])
    ATD1_Data[1][0].append(globalATD[0][0][i])
    ATD1_Data[1][0].append(HglobalATD[0][0][i])
    ATD1_Data[1][1].append(globalATD[1][0][i])
    ATD1_Data[1][1].append(HglobalATD[1][0][i])
    
    ATD2_Data[0][0].append(HglobalATD[0][1][i])
    ATD2_Data[0][1].append(HglobalATD[1][1][i])
    ATD2_Data[1][0].append(HglobalATD[0][0][i])
    ATD2_Data[1][1].append(HglobalATD[1][0][i])  

    ATD3_Data[0][0].append(globalATD[0][1][i])
    ATD3_Data[0][1].append(globalATD[1][1][i])
    ATD3_Data[1][0].append(globalATD[0][0][i])
    ATD3_Data[1][1].append(globalATD[1][0][i])

At1DoF3=(len(ATD1_Data[0][0])-1)*4
At2DoF3=(len(ATD2_Data[0][0])-1)*4
At3DoF3=(len(ATD3_Data[0][0])-1)*4

Atest1_f,ADoF1,AeffPC1,AeffV1=ANOVA(ATD1_Data,At1DoF3)
Atest2_f,ADoF2,AeffPC2,AeffV2=ANOVA(ATD2_Data,At2DoF3)
Atest3_f,ADoF3,AeffPC3,AeffV3=ANOVA(ATD3_Data,At3DoF3)

vertATD1_Data, vertATD2_Data, vertATD3_Data=[],[],[]
vertATD1_Data.append([])
vertATD1_Data.append([])
vertATD1_Data[0].append([])
vertATD1_Data[0].append([])
vertATD1_Data[1].append([])
vertATD1_Data[1].append([])
vertATD2_Data.append([])
vertATD2_Data.append([])
vertATD2_Data[0].append([])
vertATD2_Data[0].append([])
vertATD2_Data[1].append([])
vertATD2_Data[1].append([])
vertATD3_Data.append([])
vertATD3_Data.append([])
vertATD3_Data[0].append([])
vertATD3_Data[0].append([])
vertATD3_Data[1].append([])
vertATD3_Data[1].append([])
                                        
for i in xrange(0,len(vertglobalATD[0][0])):
    vertATD1_Data[0][0].append(vertglobalATD[0][1][i])
    vertATD1_Data[0][0].append(HvertglobalATD[0][1][i])
    vertATD1_Data[0][1].append(vertglobalATD[1][1][i])
    vertATD1_Data[0][1].append(HvertglobalATD[1][1][i])
    vertATD1_Data[1][0].append(vertglobalATD[0][0][i])
    vertATD1_Data[1][0].append(HvertglobalATD[0][0][i])
    vertATD1_Data[1][1].append(vertglobalATD[1][0][i])
    vertATD1_Data[1][1].append(HvertglobalATD[1][0][i])
    
    vertATD2_Data[0][0].append(HvertglobalATD[0][1][i])
    vertATD2_Data[0][1].append(HvertglobalATD[1][1][i])
    vertATD2_Data[1][0].append(HvertglobalATD[0][0][i])
    vertATD2_Data[1][1].append(HvertglobalATD[1][0][i])  

    vertATD3_Data[0][0].append(vertglobalATD[0][1][i])
    vertATD3_Data[0][1].append(vertglobalATD[1][1][i])
    vertATD3_Data[1][0].append(vertglobalATD[0][0][i])
    vertATD3_Data[1][1].append(vertglobalATD[1][0][i])

vertAt1DoF3=(len(vertATD1_Data[0][0])-1)*4
vertAt2DoF3=(len(vertATD2_Data[0][0])-1)*4
vertAt3DoF3=(len(vertATD3_Data[0][0])-1)*4

vertAtest1_f,vertADoF1,vertAeffPC1,vertAeffV1=ANOVA(vertATD1_Data,vertAt1DoF3)
vertAtest2_f,vertADoF2,vertAeffPC2,vertAeffV2=ANOVA(vertATD2_Data,vertAt2DoF3)
vertAtest3_f,vertADoF3,vertAeffPC3,vertAeffV3=ANOVA(vertATD3_Data,vertAt3DoF3)


lowcurveATD1_Data, lowcurveATD2_Data, lowcurveATD3_Data=[],[],[]
lowcurveATD1_Data.append([])
lowcurveATD1_Data.append([])
lowcurveATD1_Data[0].append([])
lowcurveATD1_Data[0].append([])
lowcurveATD1_Data[1].append([])
lowcurveATD1_Data[1].append([])
lowcurveATD2_Data.append([])
lowcurveATD2_Data.append([])
lowcurveATD2_Data[0].append([])
lowcurveATD2_Data[0].append([])
lowcurveATD2_Data[1].append([])
lowcurveATD2_Data[1].append([])
lowcurveATD3_Data.append([])
lowcurveATD3_Data.append([])
lowcurveATD3_Data[0].append([])
lowcurveATD3_Data[0].append([])
lowcurveATD3_Data[1].append([])
lowcurveATD3_Data[1].append([])
                                        
for i in xrange(0,len(lowcurveglobalATD[0][0])):
    lowcurveATD1_Data[0][0].append(lowcurveglobalATD[0][1][i])
    lowcurveATD1_Data[0][0].append(HlowcurveglobalATD[0][1][i])
    lowcurveATD1_Data[0][1].append(lowcurveglobalATD[1][1][i])
    lowcurveATD1_Data[0][1].append(HlowcurveglobalATD[1][1][i])
    lowcurveATD1_Data[1][0].append(lowcurveglobalATD[0][0][i])
    lowcurveATD1_Data[1][0].append(HlowcurveglobalATD[0][0][i])
    lowcurveATD1_Data[1][1].append(lowcurveglobalATD[1][0][i])
    lowcurveATD1_Data[1][1].append(HlowcurveglobalATD[1][0][i])
    
    lowcurveATD2_Data[0][0].append(HlowcurveglobalATD[0][1][i])
    lowcurveATD2_Data[0][1].append(HlowcurveglobalATD[1][1][i])
    lowcurveATD2_Data[1][0].append(HlowcurveglobalATD[0][0][i])
    lowcurveATD2_Data[1][1].append(HlowcurveglobalATD[1][0][i])  

    lowcurveATD3_Data[0][0].append(lowcurveglobalATD[0][1][i])
    lowcurveATD3_Data[0][1].append(lowcurveglobalATD[1][1][i])
    lowcurveATD3_Data[1][0].append(lowcurveglobalATD[0][0][i])
    lowcurveATD3_Data[1][1].append(lowcurveglobalATD[1][0][i])

lowcurveAt1DoF3=(len(lowcurveATD1_Data[0][0])-1)*4
lowcurveAt2DoF3=(len(lowcurveATD2_Data[0][0])-1)*4
lowcurveAt3DoF3=(len(lowcurveATD3_Data[0][0])-1)*4

lowcurveAtest1_f,lowcurveADoF1,lowcurveAeffPC1,lowcurveAeffV1=ANOVA(lowcurveATD1_Data,lowcurveAt1DoF3)
lowcurveAtest2_f,lowcurveADoF2,lowcurveAeffPC2,lowcurveAeffV2=ANOVA(lowcurveATD2_Data,lowcurveAt2DoF3)
lowcurveAtest3_f,lowcurveADoF3,lowcurveAeffPC3,lowcurveAeffV3=ANOVA(lowcurveATD3_Data,lowcurveAt3DoF3)

medcurveATD1_Data, medcurveATD2_Data, medcurveATD3_Data=[],[],[]
medcurveATD1_Data.append([])
medcurveATD1_Data.append([])
medcurveATD1_Data[0].append([])
medcurveATD1_Data[0].append([])
medcurveATD1_Data[1].append([])
medcurveATD1_Data[1].append([])
medcurveATD2_Data.append([])
medcurveATD2_Data.append([])
medcurveATD2_Data[0].append([])
medcurveATD2_Data[0].append([])
medcurveATD2_Data[1].append([])
medcurveATD2_Data[1].append([])
medcurveATD3_Data.append([])
medcurveATD3_Data.append([])
medcurveATD3_Data[0].append([])
medcurveATD3_Data[0].append([])
medcurveATD3_Data[1].append([])
medcurveATD3_Data[1].append([])
                                        
for i in xrange(0,len(medcurveglobalATD[0][0])):
    medcurveATD1_Data[0][0].append(medcurveglobalATD[0][1][i])
    medcurveATD1_Data[0][0].append(HmedcurveglobalATD[0][1][i])
    medcurveATD1_Data[0][1].append(medcurveglobalATD[1][1][i])
    medcurveATD1_Data[0][1].append(HmedcurveglobalATD[1][1][i])
    medcurveATD1_Data[1][0].append(medcurveglobalATD[0][0][i])
    medcurveATD1_Data[1][0].append(HmedcurveglobalATD[0][0][i])
    medcurveATD1_Data[1][1].append(medcurveglobalATD[1][0][i])
    medcurveATD1_Data[1][1].append(HmedcurveglobalATD[1][0][i])
    
    medcurveATD2_Data[0][0].append(HmedcurveglobalATD[0][1][i])
    medcurveATD2_Data[0][1].append(HmedcurveglobalATD[1][1][i])
    medcurveATD2_Data[1][0].append(HmedcurveglobalATD[0][0][i])
    medcurveATD2_Data[1][1].append(HmedcurveglobalATD[1][0][i])  

    medcurveATD3_Data[0][0].append(medcurveglobalATD[0][1][i])
    medcurveATD3_Data[0][1].append(medcurveglobalATD[1][1][i])
    medcurveATD3_Data[1][0].append(medcurveglobalATD[0][0][i])
    medcurveATD3_Data[1][1].append(medcurveglobalATD[1][0][i])

medcurveAt1DoF3=(len(medcurveATD1_Data[0][0])-1)*4
medcurveAt2DoF3=(len(medcurveATD2_Data[0][0])-1)*4
medcurveAt3DoF3=(len(medcurveATD3_Data[0][0])-1)*4

medcurveAtest1_f,medcurveADoF1,medcurveAeffPC1,medcurveAeffV1=ANOVA(medcurveATD1_Data,medcurveAt1DoF3)
medcurveAtest2_f,medcurveADoF2,medcurveAeffPC2,medcurveAeffV2=ANOVA(medcurveATD2_Data,medcurveAt2DoF3)
medcurveAtest3_f,medcurveADoF3,medcurveAeffPC3,medcurveAeffV3=ANOVA(medcurveATD3_Data,medcurveAt3DoF3)

hicurveATD1_Data, hicurveATD2_Data, hicurveATD3_Data=[],[],[]
hicurveATD1_Data.append([])
hicurveATD1_Data.append([])
hicurveATD1_Data[0].append([])
hicurveATD1_Data[0].append([])
hicurveATD1_Data[1].append([])
hicurveATD1_Data[1].append([])
hicurveATD2_Data.append([])
hicurveATD2_Data.append([])
hicurveATD2_Data[0].append([])
hicurveATD2_Data[0].append([])
hicurveATD2_Data[1].append([])
hicurveATD2_Data[1].append([])
hicurveATD3_Data.append([])
hicurveATD3_Data.append([])
hicurveATD3_Data[0].append([])
hicurveATD3_Data[0].append([])
hicurveATD3_Data[1].append([])
hicurveATD3_Data[1].append([])
                                        
for i in xrange(0,len(hicurveglobalATD[0][0])):
    hicurveATD1_Data[0][0].append(hicurveglobalATD[0][1][i])
    hicurveATD1_Data[0][0].append(HhicurveglobalATD[0][1][i])
    hicurveATD1_Data[0][1].append(hicurveglobalATD[1][1][i])
    hicurveATD1_Data[0][1].append(HhicurveglobalATD[1][1][i])
    hicurveATD1_Data[1][0].append(hicurveglobalATD[0][0][i])
    hicurveATD1_Data[1][0].append(HhicurveglobalATD[0][0][i])
    hicurveATD1_Data[1][1].append(hicurveglobalATD[1][0][i])
    hicurveATD1_Data[1][1].append(HhicurveglobalATD[1][0][i])
    
    hicurveATD2_Data[0][0].append(HhicurveglobalATD[0][1][i])
    hicurveATD2_Data[0][1].append(HhicurveglobalATD[1][1][i])
    hicurveATD2_Data[1][0].append(HhicurveglobalATD[0][0][i])
    hicurveATD2_Data[1][1].append(HhicurveglobalATD[1][0][i])  

    hicurveATD3_Data[0][0].append(hicurveglobalATD[0][1][i])
    hicurveATD3_Data[0][1].append(hicurveglobalATD[1][1][i])
    hicurveATD3_Data[1][0].append(hicurveglobalATD[0][0][i])
    hicurveATD3_Data[1][1].append(hicurveglobalATD[1][0][i])

hicurveAt1DoF3=(len(hicurveATD1_Data[0][0])-1)*4
hicurveAt2DoF3=(len(hicurveATD2_Data[0][0])-1)*4
hicurveAt3DoF3=(len(hicurveATD3_Data[0][0])-1)*4

hicurveAtest1_f,hicurveADoF1,hicurveAeffPC1,hicurveAeffV1=ANOVA(hicurveATD1_Data,hicurveAt1DoF3)
hicurveAtest2_f,hicurveADoF2,hicurveAeffPC2,hicurveAeffV2=ANOVA(hicurveATD2_Data,hicurveAt2DoF3)
hicurveAtest3_f,hicurveADoF3,hicurveAeffPC3,hicurveAeffV3=ANOVA(hicurveATD3_Data,hicurveAt3DoF3)

AnovagroupA=[ATD1_Data,ATD2_Data,ATD3_Data,vertATD1_Data,vertATD2_Data,vertATD3_Data,lowcurveATD1_Data,lowcurveATD2_Data,lowcurveATD3_Data,medcurveATD1_Data,medcurveATD2_Data,medcurveATD3_Data,hicurveATD1_Data,hicurveATD2_Data,hicurveATD3_Data]
    
ATD_csv_data=[[ATD1_Data[0][0],ATD1_Data[0][1],ATD1_Data[1][0],ATD1_Data[1][1]],[ATD2_Data[0][0],ATD2_Data[0][1],ATD2_Data[1][0],ATD2_Data[1][1]],[ATD3_Data[0][0],ATD3_Data[0][1],ATD3_Data[1][0],ATD3_Data[1][1]],[vertATD1_Data[0][0],vertATD1_Data[0][1],vertATD1_Data[1][0],vertATD1_Data[1][1]],[vertATD2_Data[0][0],vertATD2_Data[0][1],vertATD2_Data[1][0],vertATD2_Data[1][1]],[vertATD3_Data[0][0],vertATD3_Data[0][1],vertATD3_Data[1][0],vertATD3_Data[1][1]],[lowcurveATD1_Data[0][0],lowcurveATD1_Data[0][1],lowcurveATD1_Data[1][0],lowcurveATD1_Data[1][1]],[lowcurveATD2_Data[0][0],lowcurveATD2_Data[0][1],lowcurveATD2_Data[1][0],lowcurveATD2_Data[1][1]],[lowcurveATD3_Data[0][0],lowcurveATD3_Data[0][1],lowcurveATD3_Data[1][0],lowcurveATD3_Data[1][1]],[medcurveATD1_Data[0][0],medcurveATD1_Data[0][1],medcurveATD1_Data[1][0],medcurveATD1_Data[1][1]],[medcurveATD2_Data[0][0],medcurveATD2_Data[0][1],medcurveATD2_Data[1][0],medcurveATD2_Data[1][1]],[medcurveATD3_Data[0][0],medcurveATD3_Data[0][1],medcurveATD3_Data[1][0],medcurveATD3_Data[1][1]],[hicurveATD1_Data[0][0],hicurveATD1_Data[0][1],hicurveATD1_Data[1][0],hicurveATD1_Data[1][1]],[hicurveATD2_Data[0][0],hicurveATD2_Data[0][1],hicurveATD2_Data[1][0],hicurveATD2_Data[1][1]],[hicurveATD3_Data[0][0],hicurveATD3_Data[0][1],hicurveATD3_Data[1][0],hicurveATD3_Data[1][1]]]

for i in xrange(0,len(csv_names)):
    for j in xrange(0,len(ATD_csv_data[i])):
        csvfile="/home/cuebong/git/cri4/MTD data/ATD_data"+csv_names[i]+str(j+1)+".csv"
        with open(csvfile,"w") as output:
            writer=csv.writer(output,lineterminator='\n')
            for val in ATD_csv_data[i][j]:
                writer.writerow([val])
"""
