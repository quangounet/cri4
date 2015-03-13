def ANOVA(data,DoF3in):
    mean=[]
    mean.append(float(sum(data[0][0]))/len(data[0][0]))
    mean.append(float(sum(data[0][1]))/len(data[0][1]))
    mean.append(float(sum(data[1][0]))/len(data[1][0]))
    mean.append(float(sum(data[1][1]))/len(data[1][1]))
    mean.append(float(mean[0]+mean[1])/2)
    mean.append(float(mean[2]+mean[3])/2)
    mean.append(float(mean[0]+mean[2])/2)
    mean.append(float(mean[1]+mean[3])/2)
    mean.append(float(mean[4]+mean[5])/2)
    #print(mean)
    SS=[]
    SS1patient=(len(data[0][0])+len(data[0][1]))*(float(mean[4]-mean[8])**2)
    SS1control=(len(data[1][0])+len(data[1][1]))*(float(mean[5]-mean[8])**2)
    SS.append(SS1patient+SS1control)
    #print(SS1patient,SS1control)

    #Cohen difference calculations
    Psummer=0
    Csummer=0
    VFsummer=0
    BFsummer=0
    patientdata=[]
    controldata=[]
    VFdata=[]
    BFdata=[]
    for i in xrange(0,len(data[0][0])):
        patientdata.append(data[0][0][i])
        patientdata.append(data[0][1][i])
        controldata.append(data[1][0][i])
        controldata.append(data[1][1][i])
        VFdata.append(data[0][0][i])
        VFdata.append(data[1][0][i])
        BFdata.append(data[0][1][i])
        BFdata.append(data[1][1][i])
    for i in xrange(0,len(patientdata)):
        Psummer=Psummer+(patientdata[i]-mean[4])**2
        Csummer=Csummer+(controldata[i]-mean[5])**2
        VFsummer=VFsummer+(VFdata[i]-mean[6])**2
        BFsummer=BFsummer+(BFdata[i]-mean[7])**2
    NumP=len(patientdata)-1
    NumC=len(controldata)-1
    NumVF=len(VFdata)-1
    NumBF=len(BFdata)-1
    Ps_sq=(float(1)/NumP)*Psummer
    Cs_sq=(float(1)/NumC)*Csummer
    VFs_sq=(float(1)/NumVF)*VFsummer
    BFs_sq=(float(1)/NumBF)*BFsummer
    pooledS_PC=((NumP*Ps_sq+NumC*Cs_sq)/(float(len(patientdata)+len(controldata))-2))**0.5
    pooledS_VFBF=((NumVF*VFs_sq+NumBF*BFs_sq)/(float(len(VFdata)+len(BFdata))-2))**0.5
    diffPC=(mean[4]-mean[5])/pooledS_PC
    diffVFBF=(mean[6]-mean[7])/pooledS_VFBF
    print(Ps_sq,Cs_sq,VFs_sq,BFs_sq, pooledS_PC,pooledS_VFBF)
    print(diffPC, diffVFBF)

    SS2patient=len(data[0][0])*((mean[6]-mean[8])**2)+len(data[0][1])*(float(mean[7]-mean[8])**2)
    SS2control=len(data[1][0])*((mean[6]-mean[8])**2)+len(data[1][1])*(float(mean[7]-mean[8])**2)
    SS.append(SS2patient+SS2control)
    #print(SS2patient,SS2control)

    SS3patient=0
    for i in range(0,len(data[0][0])):
        SS3patient=SS3patient+(float(data[0][0][i]-mean[0])**2)+(float(data[0][1][i]-mean[1])**2)
    #print(SS3patient)
        
    SS3control=0
    for i in range(0,len(data[1][0])):
        SS3control=SS3control+(float(data[1][0][i]-mean[2])**2)+(float(data[1][1][i]-mean[3])**2)
    #print(SS3control)

    SS.append(SS3patient+SS3control)

    SStot=0
    for i in range(0,len(data[0][0])):
        SStot=SStot+(float(data[0][0][i]-mean[8])**2)+(float(data[0][1][i]-mean[8])**2)+(float(data[1][0][i]-mean[8])**2)+(float(data[1][1][i]-mean[8])**2)

    SS4=SStot-(SS[0]+SS[1]+SS[2])

    SS.append(SS4)
    SS.append(SStot)
    DoF1=1
    DoF2=1
    DoF3=DoF3in
    DoF4=DoF1*DoF2
    DoF5=DoF1+DoF2+DoF3+DoF4
    DoF=[DoF1,DoF2,DoF3,DoF4,DoF5]

    MeanSq=[]
    MeanSq.append(float(SS[0]/DoF[0]))
    MeanSq.append(float(SS[1]/DoF[1]))
    MeanSq.append(float(SS[2]/DoF[2]))
    MeanSq.append(float(SS[3]/DoF[3]))

    Fscore=[]
    Fscore.append(float(MeanSq[0]/MeanSq[2]))
    Fscore.append(float(MeanSq[1]/MeanSq[2]))
    Fscore.append(float(MeanSq[3]/MeanSq[2]))

    return Fscore,DoF,diffPC,diffVFBF
