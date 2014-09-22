import numpy as np

def deriv(val):
    time=range(0,len(val))
    time=np.array(time,dtype=np.float32).transpose()
    val=np.array(val,dtype=np.float32).transpose()
    interval=np.gradient(time)[0]
    derivative=np.gradient(val,interval)
    
    return time, derivative
