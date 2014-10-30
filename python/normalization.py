import csv
from collections import defaultdict
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
import matplotlib.pyplot as plt
from extract_midpoint import data
from normalize import normalize

plt.ion() #turns on interactive mode
fig=plt.figure()

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_VF_01.csv') as f:
    MPX=[]
    MPY=[]
    MPZ=[]
    data(f,MPX,MPY,MPZ) #Obtains midpoint values for corresponding file
    Nf=len(MPX)
    normalize(MPX)
    
with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_VF_02.csv') as f:
    MPX1=[]
    MPY1=[]
    MPZ1=[]
    data(f,MPX1,MPY1,MPZ1)
    Nf1=len(MPX1)
    normalize(MPX1)

with open('/home/cuebong/git/cri4/data_5_9_14/C02/C02_C1N_S_vert_VF_03.csv') as f:
    MPX2=[]
    MPY2=[]
    MPZ2=[]
    data(f,MPX2,MPY2,MPZ2)
    Nf2=len(MPX2)
    normalize(MPX2,)

if Nf>Nf1 and Nf>Nf2:
    samples=Nf
elif Nf1>Nf and Nf1>Nf2:
    samples=Nf
else samples=Nf2

for i in xrange(0,samples):
    print(MPX[i])

fig.suptitle('Midpoint Trajectories')
plt.xlabel('normalised time')
plt.ylabel('X-axis')
plt.show()
