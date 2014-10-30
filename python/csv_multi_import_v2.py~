import os

def get_filepaths(directory):
    file_paths=[]
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath=os.path.join(root,filename)
            file_paths.append(filepath)

    return file_paths
#__________________________________________________________________#
import csv
from collections import defaultdict
from decimal import *
getcontext().prec=6

def data(m,g,h,j):
    n=defaultdict(list)
    reader=csv.reader(m)
    for row in reader:
        for (i,v) in enumerate(row):
            a=Decimal(v)
            n[i].append(a)
    RShouX=n[15]
    RShouY=n[16]
    RShouZ=n[17]
    LShouX=n[18]
    LShouY=n[19]
    LShouZ=n[20]
    for i in xrange(1,len(RShouX)): 
        g.append((RShouX[i]+LShouX[i])/2)
        h.append((RShouY[i]+LShouY[i])/2)
        j.append((RShouZ[i]+LShouZ[i])/2)
#__________________________________________________________________#
import matplotlib.pyplot as plt

plt.ion()
fig=plt.figure()

full_file_paths=get_filepaths("/home/cuebong/git/cri4/data_5_9_14")

for i in xrange(0,100):
    MPX=[]
    MPY=[]
    MPZ=[]
    print(i)
    with open(full_file_paths[i]) as f:
        data(f, MPX,MPY,MPZ,)
        plt.plot(MPX,MPY)

fig.suptitle('Midpoint Trajectories')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
plt.axis("equal")
