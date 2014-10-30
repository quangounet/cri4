import os

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths=[] #Defining list for storing filpaths
    # Walk through the tree
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Joining the two strings to form full filepath
            filepath=os.path.join(root,filename)
            file_paths.append(filepath)

    return file_paths
#__________________________________________________________________#
import csv
from collections import defaultdict
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6

def data(m,g,h,j):
    """
    This function accesses the specified csv file and reads
    each row in every filled column, appending the values
    into lists. The desired shoulder marker data is extracted
    and used to calculate the midpoint values, which are then
    saved into the corresponding variables.
    """
    n=defaultdict(list) #appending each value of each column into list
    reader=csv.reader(m)
    for row in reader: #running through each row in csv file
        for (i,v) in enumerate(row):
            a=Decimal(v) #converts string to decimal
            n[i].append(a) #appends each value to corresponding column list
    #Extracting shoulder marker columns
    RShouX=n[15]
    RShouY=n[16]
    RShouZ=n[17]
    LShouX=n[18]
    LShouY=n[19]
    LShouZ=n[20]
    for i in xrange(1,len(RShouX)): #Calculating midpoint values for each row
        g.append((RShouX[i]+LShouX[i])/2)
        h.append((RShouY[i]+LShouY[i])/2)
        j.append((RShouZ[i]+LShouZ[i])/2)
#__________________________________________________________________#
import matplotlib.pyplot as plt

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
