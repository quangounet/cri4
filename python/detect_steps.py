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
from collections import defaultdict
import csv 

def peakdet(v, delta, x = None):
    maxtab = []
    mintab = []
    if x is None:
        x = arange(len(v))
    v = asarray(v)
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    lookformax = True
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True
 
    return array(maxtab), array(mintab) 

with open("/home/cuebong/git/cri4/AllData/Post_processedCSV/P08/P08_C4S_L_bleu_BF_02.csv") as f:
    n=defaultdict(list) #appending each value of each column into list
    reader=csv.reader(f)
    for row in reader: #running through each row in csv file
        for (i,v) in enumerate(row):
            a=Decimal(v) #converts string to decimal
            n[i].append(a) #appends each value to corresponding column list

RShouX=n[15]
RShouY=n[16]
RShouZ=n[17]
LShouX=n[18]
LShouY=n[19]
LShouZ=n[20]
RheelX=n[30]
RheelY=n[31]
RheelZ=n[32]
LheelX=n[24]
LheelY=n[25]
LheelZ=n[26]
time=[]

length=xrange(0,len(RheelZ))
for i in length:
    time.append(Decimal(i)/120)
plt.figure()
plt.plot(time,RheelZ,time,LheelZ)
#plt.plot(time,RheelX,time,RheelY,time,LheelX,time,LheelY)

traj_time,Rheelpeaks=deriv_vel(RheelZ)

NoiseRZ=[]
filteredRheel=[]
for i in xrange(0,len(Rheelpeaks)):
    NoiseRZ.append(float(Rheelpeaks[i]))
filteredRheel.append(butter_lowpass_filter(NoiseRZ,6,120,order=2))
act_time=[]
for i in xrange(0,len(filteredRheel[0])):
    act_time.append(Decimal(i)/120)
plt.plot(act_time,filteredRheel[0])

