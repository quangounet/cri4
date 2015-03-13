from numpy import *
from matplotlib.patches import Ellipse
from pylab import *

def variance_ellipse(sample,x1,x2,x3,y1,y2,y3):
    variability=[]

    for j in xrange(0,len(sample)):
        data=array([[x1[j],y1[j]],[x2[j],y2[j]],[x3[j],y3[j]]])
        data2=array(data)

        meanx=mean(data[:,0])
        meany=mean(data[:,1])
    
        for l in range(data.shape[0]):
            data2[l,0]=data[l,0]-meanx
            data2[l,1]=data[l,1]-meany

        ax=gca()

        xy=(meanx,meany)
        u,d,v=linalg.svd(data2)

        width=d[0]
        height=d[1]

        angle=arctan2(v[0,1],v[0,0])*180/pi
        variability.append(sqrt(width*width+height*height))

        ellipse=Ellipse(xy,width,height,angle,edgecolor='c',fc='none',lw=1)
        ax.add_patch(ellipse)

    return variability
