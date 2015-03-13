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

fs=120
lowcut=1

#_________________________Data Extraction________________________#

plt.ion()
subjects=['C01','C03','C04','C05','C07','C06','C08','C09','C10','C11','P01','P02','P03','P04','P05','P06','P07','P08','P09','P10']
#subjects=['C01', 'C04','P01','P03']
target_list=['C4E_L_bleu','C4N_L_bleu','C4S_L_bleu','C4W_L_bleu','C5E_L_bleu','C5N_L_bleu','C5S_L_bleu','C5W_L_bleu','C4E_R_rouge','C4N_R_rouge','C4S_R_rouge','C4W_R_rouge','C5E_R_rouge','C5N_R_rouge','C5S_R_rouge','C5W_R_rouge','C1N_S_vert','C2N_S_vert','C3N_S_vert']
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
    
    velinterp=[]
    velvalue=[]
    for j in xrange(0,len(file_paths)):
        velinterp.append([])
        velvalue.append([])
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
                    m=len(time_vel[j][k])-l-1
                    n=vel[j][k][m]
                    if n>0.4:
                        break
                vel[j][k]=np.delete(vel[j][k],xrange(m,len(vel[j][k])))
                time_vel[j][k]=np.delete(time_vel[j][k],xrange(m,len(time_vel[j][k])))
                x[i][j][k]=np.delete(x[i][j][k],xrange(m,len(x[i][j][k])))
                y[i][j][k]=np.delete(y[i][j][k],xrange(m,len(y[i][j][k])))
                xvalues[i][j][k]=np.delete(xvalues[i][j][k],xrange(m,len(x[i][j][k])))
                yvalues[i][j][k]=np.delete(yvalues[i][j][k],xrange(m,len(y[i][j][k])))
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
            g,h,m,n,o=mean_calc2(velnf,velinterp[j][0],velinterp[j][1],velinterp[j][2],velvalue[j][0],velvalue[j][1],velvalue[j][2])
            meanvel[i].append(h)
            velsample[i].append(g)
            velax[i][j].append(m)
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
                    m=len(time_vel[j][k])-l-1
                    n=vel[j][k][m]
                    if n>0.4:
                        break
                vel[j][k]=np.delete(vel[j][k],xrange(m,len(vel[j][k])))
                time_vel[j][k]=np.delete(time_vel[j][k],xrange(m,len(time_vel[j][k])))
                x[i][j][k]=np.delete(x[i][j][k],xrange(m,len(x[i][j][k])))
                y[i][j][k]=np.delete(y[i][j][k],xrange(m,len(y[i][j][k])))
                xvalues[i][j][k]=np.delete(xvalues[i][j][k],xrange(m,len(x[i][j][k])))
                yvalues[i][j][k]=np.delete(yvalues[i][j][k],xrange(m,len(y[i][j][k])))
                fX[j][k]=np.delete(fX[j][k],xrange(m,len(fX[j][k])))
                fY[j][k]=np.delete(fY[j][k],xrange(m,len(fY[j][k])))

                e,f=perform_spline2(vel[j][k])
                velinterp[j].append(e)
                velvalue[j].append(f)

            if len(time_vel[j][0])<len(time_vel[j][1]):
                velnf=len(time_vel[j][0])
            else:
                velnf=len(time_vel[j][1])
            g,h,m,n=[],[],[],[]
            for r in xrange(0,velnf):
                g.append(Decimal(r)/velnf)
                m.append(velvalue[j][0][g[r]*len(velinterp[j][0])])
                n.append(velvalue[j][1][g[r]*len(velinterp[j][1])])
                h.append(Decimal(m[r]+n[r])/2)
            meanvel[i].append(h)
            velsample[i].append(g)
            velax[i][j].append(m)
            velax[i][j].append(n)

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

print("beginning mean trajectory calculations")
target_order=[0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27,32,34,36,4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31,33,35,37]

#______________Global mean calculations_______________#

globalmeansample,globalmeanX,globalmeanY=[],[],[]

for i in xrange(0,38):
    globalmeansample.append([])
    globalmeanX.append([])
    globalmeanY.append([])

for j in target_order:
    globalnf=10000
    meanX_axis=[]
    meanY_axis=[]
    meanx=[]
    meany=[]
    meanxval=[]
    meanyval=[]
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
        for i in xrange(0,20):
            meanX_axis[t].append(meanxval[i][globalmeansample[j][t]*len(meanx[i])])
            meanY_axis[t].append(meanyval[i][globalmeansample[j][t]*len(meany[i])])
        globalmeanX[j].append(sum(meanX_axis[t])/20)
        globalmeanY[j].append(sum(meanY_axis[t])/20)

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
    
csv_names=['all','hem','non-hem','straight-all','straight-hem','straight-non-hem','curved-all','curved-hem','curved-non-hem','uturn-all','uturn-hem','uturn-non-hem']
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
