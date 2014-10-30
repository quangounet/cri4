import numpy as np
from decimal import *
getcontext().prec=6

def deriv_vel(val):
    limit=(Decimal(len(val))/120)
    step=Decimal(1)/120
    time=np.arange(0,limit,step)
    time=np.array(time,dtype=np.float32).transpose()
    val=np.array(val,dtype=np.float32).transpose()
    interval=np.gradient(time)[0]
    derivative=np.gradient(val,interval)
    
    return time, derivative

def deriv_accel(val):
    time=range(0,len(val))
    time=np.array(time,dtype=np.float32).transpose()
    val=np.array(val,dtype=np.float32).transpose()
    interval=np.gradient(time)[0]
    derivative=np.gradient(val,interval)

    return time, derivative
