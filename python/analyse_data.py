import os
import csv
from collections import defaultdict
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6
import matplotlib.pyplot as plt
from read_filenames import get_filepaths
from extract_midpoint import data

plt.ion() #turns on interactive mode
fig=plt.figure()

#Obtaining filepaths for all files in data directory
full_file_paths=get_filepaths("/home/cuebong/git/cri4/data_5_9_14/C01")
for i in xrange(0,len(full_file_paths)): #Accessing each file in turn for analysing
    MPX=[]
    MPY=[]
    MPZ=[]
    print(i,'of',len(full_file_paths)-1)
    with open(full_file_paths[i]) as f:
        data(f, MPX,MPY,MPZ,) #Obtains midpoint values for corresponding file
        plt.plot(MPX,MPY) #plots midpoint trajectory for current file

fig.suptitle('Midpoint Trajectories')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
plt.axis("equal")
