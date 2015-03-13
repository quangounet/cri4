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
from butter_filter import butter_lowpass, butter_lowpass_filter

fs=120
lowcut=1

#_________________________Data Extraction________________________#

plt.ion()
#subjects=['C01','C03','C04','C05','C07','C06','C08','C09','C10','C11','P01','P02','P03','P04','P05','P06','P07','P08','P09','P10']
subjects=['C01', 'C04','P01','P03']
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
eliminate_list=[]
Xax=[]
Yax=[]

for i in xrange(0,4):###
    target_list=[]
    subject=subjects[i]
    file_paths=[]
    title_list=[]
    use_files,nf=[],[]
    meanX.append([])
    meanY.append([])
    sample.append([])
    meanvel.append([])
    velsample.append([])
    Xax.append([])
    Yax.append([])
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
        target_list.append(target)

        MPX.append([])
        MPY.append([])
        MPZ.append([])
        time.append([])
        x.append([])
        y.append([])
        xvalues.append([])
        yvalues.append([])
        Xax[i].append([])
        Yax[i].append([])
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
    
    velinterp=[]
    velvalue=[]
    for j in xrange(0,len(file_paths)):
        velinterp.append([])
        velvalue.append([])
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
                yvalues[j][k]=np.delete(yvalues[j][k],xrange(m,len(y[j][k])))
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
                velinterp[j].append(e)
                velvalue[j].append(f)
            
            velnf=compare(time_vel[j][0],time_vel[j][1],time_vel[j][2])
            g,h=mean_calc2(velnf,velinterp[j][0],velinterp[j][1],velinterp[j][2],velvalue[j][0],velvalue[j][1],velvalue[j][2])
            meanvel[i].append(h)
            velsample[i].append(g)
        else:
            meanvel[i].append(0)
            velsample[i].append(0)
            
                

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
            meanX[i].append(0)
            meanY[i].append(0)
            sample[i].append(0)
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
for j in xrange(0,38):####
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
        if meanX[i][j]!=0:
            targetplots[x_count,y_count].plot(meanX[i][j],meanY[i][j])
            targetplots[x_count,y_count].set_title(subjects[i])
            a=variance_ellipse(sample[i][j],Xax[i][j][0],Xax[i][j][1],Xax[i][j][2],Yax[i][j][0],Yax[i][j][1],Yax[i][j][2],x_count,y_count,targetplots)
        else:
            targetplots[x_count,y_count].plot(0,0)
            targetplots[x_count,y_count].set_title(subjects[i])
        if i in xrange(0,10):###
           x_count1=x_count1+1
        elif i in xrange(10,20):###
            x_count2=x_count2+1
        targetplots[x_count,y_count].set_xlim(0,4.5)
        targetplots[x_count,y_count].set_ylim(0,6)
        targetplots[x_count,y_count].set_aspect('equal')
    f1.savefig("/home/cuebong/git/cri4/Trajectory_Plots/Combined/trajectory_plots_"+target_list[j])
    plt.close()

for j in xrange(0,38):####
    x_count1=0
    x_count2=0
    f2,velplots=plt.subplots(10,2,figsize=(15,60))###
    for i in xrange(0,20):###
        if i in xrange(0,10):###
            y_count=0
            x_count=x_count1
        elif i in xrange(10,20):###
            y_count=1
            x_count=x_count2
        if meanX[i][j]!=0:
            velplots[x_count,y_count].plot(velsample[i][j],meanvel[i][j])
            velplots[x_count,y_count].set_title(subjects[i])
            #targetplots[x_count,y_count].add_patch(a)
        else:
            velplots[x_count,y_count].plot(0,0)
            velplots[x_count,y_count].set_title(subjects[i])
        if i in xrange(0,10):###
           x_count1=x_count1+1
        elif i in xrange(10,20):###
            x_count2=x_count2+1
        velplots[x_count,y_count].set_xlim(0,1)
        velplots[x_count,y_count].set_ylim(0,1.5)
        velplots[x_count,y_count].set_aspect('equal')
    f2.savefig("/home/cuebong/git/cri4/Trajectory_Plots/Velocity_Plots/velocity_profiles_"+target_list[j])
    plt.close()
"""
def variance_ellipse_mean(Cnormalisedtime, CsamplemeanX,CsamplemeanY):
    for n in xrange(0,len(Cnormalisedtime)):
        data=[]
        for i in xrange(CsamplemeanX[n]):
            data.append([])
            data[i].append(CsamplemeanX[n][i])
            data[i].append(CsamplemeanY[n][i])
        dataarray=array(data)
        dataarray2=array(dataarray)
        
        meanx=mean(dataarray[:,0])
        meany=mean(dataarray[:,1])
        
        for m in range(dataarray.shape[0]):
            dataarray2[m,0]=dataarray[m,0]-meanx
            dataarray2[m,0]=dataarray[m,0]-meany
            
        ax=gca()
        
        xy=(meanx,meany)
        u,d,v=linealg.svg(dataarray2)
        width=d[0]
        height=d[1]
        angle=arctan2(v[0,1],v[0,0])*180/pi
        variability.append(sqrt(width*width+height*height))
        ellipse=Ellipse(xy,width,height,angle,edgecolor='c',fc='c',lw=1)
        return ellipse

for j in xrange(0,38):
    Ctime=[]
    CmeanXinterp=[]
    CmeanYinterp=[]
    CmeanXval=[]
    CmeanYval=[]
    Ctimehem=[]
    CmeanXinterphem=[]
    CmeanYinterphem=[]
    CmeanXvalhem=[]
    CmeanYvalhem=[]
    Ctimenh=[]
    CmeanXinterpnh=[]
    CmeanYinterpnh=[]
    CmeanXvalnh=[]
    CmeanYvalnh=[]
    Ptime=[]
    PmeanXinterp=[]
    PmeanYinterp=[]
    PmeanXval=[]
    PmeanYval=[]
    Ptimehem=[]
    PmeanXinterphem=[]
    PmeanYinterphem=[]
    PmeanXvalhem=[]
    PmeanYvalhem=[]
    Ptimenh=[]
    PmeanXinterpnh=[]
    PmeanYinterpnh=[]
    PmeanXvalnh=[]
    PmeanYvalnh=[]
    Csample=10000
    Psample=10000
    Csamplehem=10000
    Psamplehem=10000
    Csamplenh=10000
    Psamplenh=10000
    #hem_subjects=[2,3,6,7,8,12,13,16,17,18]
    hem_subjects=[1,3]
    for i in xrange(0,4):#####
        if meanX[i][j]!=0:
            a,b,c,d,e=perform_spline(meanX[i][j],meanY[i][j])
            if i in xrange(0,2):#####
                Ctime.append(a)
                CmeanXinterp.append(b)
                CmeanYinterp.append(c)
                CmeanXval.append(d)
                CmeanYval.append(e)
                if i in hem_subjects:
                      Ctimehem.append(a)
                      CmeanXinterphem.append(b)
                      CmeanYinterphem.append(c)
                      CmeanXvalhem.append(d)
                      CmeanYvalhem.append(e)
                      Ctimenh.append(0)
                      CmeanXinterpnh.append(0)
                      CmeanYinterpnh.append(0)
                      CmeanXvalnh.append(0)
                      CmeanYvalnh.append(0) 
                else:
                      Ctimenh.append(a)
                      CmeanXinterpnh.append(b)
                      CmeanYinterpnh.append(c)
                      CmeanXvalnh.append(d)
                      CmeanYvalnh.append(e)
                      Ctimehem.append(0)
                      CmeanXinterphem.append(0)
                      CmeanYinterphem.append(0)
                      CmeanXvalhem.append(0)
                      CmeanYvalhem.append(0)
            elif i in xrange(2,4):#####
                Ptime.append(a)
                PmeanXinterp.append(b)
                PmeanYinterp.append(c)
                PmeanXval.append(d)
                PmeanYval.append(e)
                if i in hem_subjects:
                    Ptimehem.append(a)
                    PmeanXinterphem.append(b)
                    PmeanYinterphem.append(c)
                    PmeanXvalhem.append(d)
                    PmeanYvalhem.append(e)   
                    Ptimenh.append(0)
                    PmeanXinterpnh.append(0)
                    PmeanYinterpnh.append(0)
                    PmeanXvalnh.append(0)
                    PmeanYvalnh.append(0)
     
                else:
                    Ptimenh.append(a)
                    PmeanXinterpnh.append(b)
                    PmeanYinterpnh.append(c)
                    PmeanXvalnh.append(d)
                    PmeanYvalnh.append(e)     
                    Ptimehem.append(0)
                    PmeanXinterphem.append(0)
                    PmeanYinterphem.append(0)
                    PmeanXvalhem.append(0)
                    PmeanYvalhem.append(0)
        elif meanX[i][j]==0:
            if i in xrange(0,2):######
                Ctime.append(0)
                if i in hem_subjects:
                    Ctimehem.append(0)
                else:
                    Ctimenh.append(0)
            elif i in xrange(2,4):######
                Ptime.append(0)
                if i in hem_subjects:
                    Ptimehem.append(0)
                else:
                    Ptimenh.append(0)
        if i in xrange(0,2):##########
            if Ctime[i]!=0:
                if len(Ctime[i])<Csample:
                    Csample=int(len(Ctime[i]))
            if i in hem_subjects:
                if Ctimehem[i]!=0:
                    if len(Ctimehem[i])<Csamplehem:
                        Csamplehem=int(len(Ctimehem[i]))
            else:
                if Ctimenh[i]!=0:
                    if len(Ctimenh[i])<Csamplenh:
                        Csamplenh=int(len(Ctimenh[i]))
        elif i in xrange(2,4):########
            if Ptime[i-2]!=0:#########
                if len(Ptime[i-2])<Psample:######
                    Psample=int(len(Ptime[i-2]))#####
            if i in hem_subjects:
                if Ptimehem[i-2]!=0:##########
                    if len(Ptimehem[i-2])<Psamplehem:######
                        Psamplehem=int(len(Ptimehem[i-2]))#####
            else:
                if Ptimenh[i-2]!=0:##########
                    if len(Ptimenh[i-2])<Psamplenh:######
                        Psamplenh=int(len(Ptimenh[i-2]))######

#_____Calculating mean trajectory for all hem and non-hem subjects_____#
    CsamplemeanX,CsamplemeanY,Cnormalisedtime,CmeanX,CmeanY=[],[],[],[],[]
    for n in xrange(0,Csample):
        CsamplemeanX.append([])
        CsamplemeanY.append([])
        Cnormalisedtime.append(Decimal(n)/Csample)
        for i in xrange(0,len(CmeanXinterp)):
            if all(CmeanXval[i])!=0:
                CsamplemeanX[n].append(CmeanXval[i][Cnormalisedtime[n]*len(CmeanXinterp[i])])
                CsamplemeanY[n].append(CmeanYval[i][Cnormalisedtime[n]*len(CmeanYinterp[i])])
        CmeanX.append(Decimal(sum(CsamplemeanX[n]))/len(CmeanXinterp))
        CmeanY.append(Decimal(sum(CsamplemeanY[n]))/len(CmeanYinterp))

    PsamplemeanX,PsamplemeanY,Pnormalisedtime,PmeanX,PmeanY=[],[],[],[],[]
    for n in xrange(0,Psample):
        PsamplemeanX.append([])
        PsamplemeanY.append([])
        Pnormalisedtime.append(Decimal(n)/Psample)
        for i in xrange(0,len(PmeanXinterp)):
            if all(PmeanXval[i])!=0:
                PsamplemeanX[n].append(PmeanXval[i][Pnormalisedtime[n]*len(PmeanXinterp[i])])
                PsamplemeanY[n].append(PmeanYval[i][Pnormalisedtime[n]*len(PmeanYinterp[i])])
        PmeanX.append(Decimal(sum(PsamplemeanX[n]))/len(PmeanXinterp))
        PmeanY.append(Decimal(sum(PsamplemeanY[n]))/len(PmeanYinterp))

#____Calculating for hem subjects_______#
    CsamplemeanXhem,CsamplemeanYhem,Cnormalisedtimehem,CmeanXhem,CmeanYhem=[],[],[],[],[]
    for n in xrange(0,Csamplehem):
        CsamplemeanXhem.append([])
        CsamplemeanYhem.append([])
        Cnormalisedtimehem.append(Decimal(n)/Csamplehem)
        for i in xrange(0,len(CmeanXinterphem)):
            if all(CmeanXvalhem[i])!=0:
                CsamplemeanXhem[n].append(CmeanXvalhem[i][Cnormalisedtimehem[n]*len(CmeanXinterphem[i])])
                CsamplemeanYhem[n].append(CmeanYvalhem[i][Cnormalisedtimehem[n]*len(CmeanYinterphem[i])])
        CmeanXhem.append(Decimal(sum(CsamplemeanXhem[n]))/len(CmeanXinterphem))
        CmeanYhem.append(Decimal(sum(CsamplemeanYhem[n]))/len(CmeanYinterphem))

    PsamplemeanXhem,PsamplemeanYhem,Pnormalisedtimehem,PmeanXhem,PmeanYhem=[],[],[],[],[]
    for n in xrange(0,Psamplehem):
        PsamplemeanXhem.append([])
        PsamplemeanYhem.append([])
        Pnormalisedtimehem.append(Decimal(n)/Psamplehem)
        for i in xrange(0,len(PmeanXinterphem)):
            if all(PmeanXvalhem[i])!=0:
                PsamplemeanXhem[n].append(PmeanXvalhem[i][Pnormalisedtimehem[n]*len(PmeanXinterphem[i])])
                PsamplemeanYhem[n].append(PmeanYvalhem[i][Pnormalisedtimehem[n]*len(PmeanYinterphem[i])])
        PmeanXhem.append(Decimal(sum(PsamplemeanXhem[n]))/len(PmeanXinterphem))
        PmeanYhem.append(Decimal(sum(PsamplemeanYhem[n]))/len(PmeanYinterphem))

#_____Calculating for non-hem subjects_____#
    CsamplemeanXnh,CsamplemeanYnh,Cnormalisedtimenh,CmeanXnh,CmeanYnh=[],[],[],[],[]
    for n in xrange(0,Csamplenh):
        CsamplemeanXnh.append([])
        CsamplemeanYnh.append([])
        Cnormalisedtimenh.append(Decimal(n)/Csamplenh)
        for i in xrange(0,len(CmeanXinterpnh)):
            if all(CmeanXvalnh[i])!=0:
                CsamplemeanXnh[n].append(CmeanXvalnh[i][Cnormalisedtimenh[n]*len(CmeanXinterpnh[i])])
                CsamplemeanYnh[n].append(CmeanYvalnh[i][Cnormalisedtimenh[n]*len(CmeanYinterpnh[i])])
        CmeanXnh.append(Decimal(sum(CsamplemeanXnh[n]))/len(CmeanXinterpnh))
        CmeanYnh.append(Decimal(sum(CsamplemeanYnh[n]))/len(CmeanYinterpnh))

    PsamplemeanXnh,PsamplemeanYnh,Pnormalisedtimenh,PmeanXnh,PmeanYnh=[],[],[],[],[]
    for n in xrange(0,Psamplenh):
        PsamplemeanXnh.append([])
        PsamplemeanYnh.append([])
        Pnormalisedtimenh.append(Decimal(n)/Psamplenh)
        for i in xrange(0,len(PmeanXinterpnh)):
            if all(PmeanXvalnh[i])!=0:
                PsamplemeanXnh[n].append(PmeanXvalnh[i][Pnormalisedtimenh[n]*len(PmeanXinterpnh[i])])
                PsamplemeanYnh[n].append(PmeanYvalnh[i][Pnormalisedtimenh[n]*len(PmeanYinterpnh[i])])
        PmeanXnh.append(Decimal(sum(PsamplemeanXnh[n]))/len(PmeanXinterpnh))
        PmeanYnh.append(Decimal(sum(PsamplemeanYnh[n]))/len(PmeanYinterpnh))

    f, trajmeanplot=plt.subplots(3,2,figsize=(10,10))
    trajmeanplot[0,0].plot(CmeanX,CmeanY)
    trajmeanplot[0,0].set_title('Control All')
    a=variance_ellipse_mean(Cnormalisedtime,CsamplemeanX,CsamplemeanY)
    trajmeanplot[0,0].add_patch(a)
    trajmeanplot[0,0].set_xlim(0,4.5)
    trajmeanplot[0,0].set_ylim(0,6)
    trajmeanplot[0,0].set_aspect('equal')

    trajmeanplot[0,1].plot(PmeanX,PmeanY)
    trajmeanplot[0,1].set_title('Patient All')
    b=variance_ellipse_mean(Pnormalisedtime,PsamplemeanX,PsamplemeanY)
    trajmeanplot[0,1].add_patch(b)
    trajmeanplot[0,1].set_xlim(0,4.5)
    trajmeanplot[0,1].set_ylim(0,6)
    trajmeanplot[0,1].set_aspect('equal')

    trajmeanplot[0,0].plot(CmeanXhem,CmeanYhem)
    trajmeanplot[0,0].set_title('Control Hemi')
    c=variance_ellipse_mean(Cnormalisedtimehem,CsamplemeanXhem,CsamplemeanYhem)
    trajmeanplot[0,0].add_patch(c)
    trajmeanplot[0,0].set_xlim(0,4.5)
    trajmeanplot[0,0].set_ylim(0,6)
    trajmeanplot[0,0].set_aspect('equal')

    trajmeanplot[0,0].plot(PmeanXhem,PmeanYhem)
    trajmeanplot[0,0].set_title('Patient Hemi')
    d=variance_ellipse_mean(Pnormalisedtimehem,PsamplemeanXhem,PsamplemeanYhem)
    trajmeanplot[0,0].add_patch(d)
    trajmeanplot[0,0].set_xlim(0,4.5)
    trajmeanplot[0,0].set_ylim(0,6)
    trajmeanplot[0,0].set_aspect('equal')

    trajmeanplot[0,0].plot(CmeanXnh,CmeanYnh)
    trajmeanplot[0,0].set_title('Control Non-Hemi')
    e=variance_ellipse_mean(Cnormalisedtimenh,CsamplemeanXnh,CsamplemeanYnh)
    trajmeanplot[0,0].add_patch(e)
    trajmeanplot[0,0].set_xlim(0,4.5)
    trajmeanplot[0,0].set_ylim(0,6)
    trajmeanplot[0,0].set_aspect('equal')

    trajmeanplot[0,0].plot(PmeanXnh,PmeanYnh)
    trajmeanplot[0,0].set_title('Patient Non-Hemi')
    f=variance_ellipse_mean(Pnormalisedtimenh,PsamplemeanXnh,PsamplemeanYnh)
    trajmeanplot[0,0].add_patch(f)
    trajmeanplot[0,0].set_xlim(0,4.5)
    trajmeanplot[0,0].set_ylim(0,6)
    trajmeanplot[0,0].set_aspect('equal')

    f.savefig("/home/cuebong/git/cri4/Trajectory_Plots/Subject group mean plots/"+target_list[j])

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
