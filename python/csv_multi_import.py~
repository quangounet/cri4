import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
MPX1=[]
MPY1=[]
MPZ1=[]
MPX2=[]
MPY2=[]
MPZ2=[]
MPX3=[]
MPY3=[]
MPZ3=[]
MPX4=[]
MPY4=[]
MPZ4=[]
MPX5=[]
MPY5=[]
MPZ5=[]
MPX6=[]
MPY6=[]
MPZ6=[]
MPX7=[]
MPY7=[]
MPZ7=[]
MPX8=[]
MPY8=[]
MPZ8=[]
MPX9=[]
MPY9=[]
MPZ9=[]
MPX10=[]
MPY10=[]
MPZ10=[]
MPX11=[]
MPY11=[]
MPZ11=[]
MPX12=[]
MPY12=[]
MPZ12=[]
MPX13=[]
MPY13=[]
MPZ13=[]
MPX14=[]
MPY14=[]
MPZ14=[]
MPX15=[]
MPY15=[]
MPZ15=[]

def data(m,g,h,j):
    n=defaultdict(list) #appends each value of each column into list
    reader=csv.reader(m)
    for row in reader: #runs through each row in csv file
        for (i,v) in enumerate(row):
            a=Decimal(v) #converts string to decimal
            n[i].append(a) #appends each value to its corresponding column list
    RShouX=n[12]
    RShouY=n[13]
    RShouZ=n[14]
    LShouX=n[15]
    LShouY=n[16]
    LShouZ=n[17]
    for i in xrange(1,len(RShouX)): 
        g.append((RShouX[i]+LShouX[i])/2)
        h.append((RShouY[i]+LShouY[i])/2)
        j.append((RShouZ[i]+LShouZ[i])/2)
    
with open('/home/cuebong/Downloads/Data_csv/C01_C4N_L_bleu_BF_02.csv') as f:
    data(f,MPX1,MPY1,MPZ1)

with open('/home/cuebong/Downloads/Data_csv/C01_C5N_L_bleu_BF_02.csv') as f:
    data(f,MPX2,MPY2,MPZ2)

with open('/home/cuebong/Downloads/Data_csv/C02_C3N_S_vert_VF_01.csv') as f:
    data(f,MPX3,MPY3,MPZ3)
    
with open('/home/cuebong/Downloads/Data_csv/C02_C5E_L_bleu_VF_01.csv') as f:
    data(f,MPX4,MPY4,MPZ4)

with open('/home/cuebong/Downloads/Data_csv/P01_C4N_L_bleu_VF_02.csv') as f:
    data(f,MPX5,MPY5,MPZ5)

with open('/home/cuebong/Downloads/Data_csv/P01_C4N_R_rouge_VF_01.csv') as f:
    data(f,MPX6,MPY6,MPZ6)

with open('/home/cuebong/Downloads/Data_csv/P01_C4N_R_rouge_VF_02.csv') as f:
    data(f,MPX7,MPY7,MPZ7)

with open('/home/cuebong/Downloads/Data_csv/P01_C5E_L_bleu_BF_02.csv') as f:
    data(f,MPX8,MPY8,MPZ8)

with open('/home/cuebong/Downloads/Data_csv/P01_C5W_R_rouge_BF_02.csv') as f:
    data(f,MPX9,MPY9,MPZ9)

with open('/home/cuebong/Downloads/Data_csv/P02_C3N_S_vert_BF_02.csv') as f:
    data(f,MPX10,MPY10,MPZ10)

with open('/home/cuebong/Downloads/Data_csv/P02_C3N_S_vert_VF_03.csv') as f:
    data(f,MPX11,MPY11,MPZ11)
    
with open('/home/cuebong/Downloads/Data_csv/P02_C4E_L_bleu_VF_01.csv') as f:
    data(f,MPX12,MPY12,MPZ12)

with open('/home/cuebong/Downloads/Data_csv/P02_C5E_L_bleu_BF_03.csv') as f:
    data(f,MPX13,MPY13,MPZ13)

with open('/home/cuebong/Downloads/Data_csv/P02_C5S_R_rouge_VF_02.csv') as f:
    data(f,MPX14,MPY14,MPZ14)

with open('/home/cuebong/Downloads/Data_csv/P02_C5W_R_rouge_VF_03.csv') as f:
    data(f,MPX15,MPY15,MPZ15)
    
plt.ion()

fig=plt.figure()
plt.plot(MPX1,MPY1)
plt.plot(MPX2,MPY2)
plt.plot(MPX3,MPY3)
plt.plot(MPX4,MPY4)
plt.plot(MPX5,MPY5)
plt.plot(MPX6,MPY6)
plt.plot(MPX7,MPY7)
plt.plot(MPX8,MPY8)
plt.plot(MPX9,MPY9)
plt.plot(MPX10,MPY10)
plt.plot(MPX11,MPY11)
plt.plot(MPX12,MPY12)
plt.plot(MPX13,MPY13)
plt.plot(MPX14,MPY14)
plt.plot(MPX15,MPY15)
fig.suptitle('Midpoint Trajectories')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
plt.axis("equal")
