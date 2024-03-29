from scipy import interpolate
import matplotlib.pyplot as plt

def perform_spline(MPX,MPY):
    time=range(0,len(MPX))
    xinterp=interpolate.UnivariateSpline(time,MPX,s=0.0001)(time)
    yinterp=interpolate.UnivariateSpline(time,MPY,s=0.0001)(time)
    xline=plt.plot(time,xinterp)
    yline=plt.plot(time,yinterp)
    xvalues=xline[0].get_ydata()
    yvalues=yline[0].get_ydata()

    return time,xinterp,yinterp,xvalues,yvalues

def perform_spline2(vel):
    time=range(0,len(vel))
    velinterp=interpolate.UnivariateSpline(time,vel,s=0.0001)(time)
    velline=plt.plot(time,velinterp)
    velval=velline[0].get_ydata()
    
    return velinterp,velval
