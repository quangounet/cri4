import csv
from collections import defaultdict
from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6

def data(m):
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
    g=[]
    h=[]
    j=[]
    for i in xrange(1,len(RShouX)): #Calculating midpoint values for each row
        g.append((RShouX[i]+LShouX[i])/2)
        h.append((RShouY[i]+LShouY[i])/2)
        j.append((RShouZ[i]+LShouZ[i])/2)

    return g,h,j
