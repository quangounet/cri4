from numpy import *
from matplotlib.patches import Ellipse
from pylab import *

def variance_ellipse(sample,x1,x2,x3,y1,y2,y3,xcount,ycount,plotname,vbf,alphaval):
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

        if vbf==1:
            edgecolour='r'
            facecolour='r'
        elif vbf==2:
            edgecolour='k'
            facecolour='k'
            
        ellipse=Ellipse(xy,width,height,angle,edgecolor=edgecolour,fc='none',lw=1,alpha=alphaval)
        plotname[xcount,ycount].add_patch(ellipse)
    
    return variability
    #return ellipse

def variance_ellipse2(sample,y1,y2,y3,xcount,ycount,plotname,vbf):
    variability=[]

    for j in xrange(0,len(sample)):
        data=array([[float(sample[j]),y1[j]],[float(sample[j]),y2[j]],[float(sample[j]),y3[j]]])
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

        if vbf==1:
            edgecolour='r'
            faceolour='r'
        elif vbf==2:
            edgecolour='k'
            facecolour='k'
        ellipse=Ellipse(xy,width,height,angle,edgecolor=edgecolour,fc='none',lw=1,alpha=0.05)
        plotname[xcount,ycount].add_patch(ellipse)

    
    return variability

def variance_ellipse_2(sample,x1,x2,y1,y2,xcount,ycount,plotname,vbf,alphaval):
    variability=[]

    for j in xrange(0,len(sample)):
        data=array([[x1[j],y1[j]],[x2[j],y2[j]]])
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

        if vbf==1:
            edgecolour='r'
        elif vbf==2:
            edgecolour='k'
        ellipse=Ellipse(xy,width,height,angle,edgecolor=edgecolour,fc='none',lw=1,alpha=alphaval)
        plotname[xcount,ycount].add_patch(ellipse)
    
    return variability
    #return ellipse

def variance_ellipse2_2(sample,y1,y2,xcount,ycount,plotname,vbf):
    variability=[]

    for j in xrange(0,len(sample)):
        data=array([[float(sample[j]),y1[j]],[float(sample[j]),y2[j]]])
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

        if vbf==1:
            edgecolour='r'
            facecolour='r'
        elif vbf==2:
            edgecolour='k'
            facecolour='k'
        ellipse=Ellipse(xy,width,height,angle,edgecolor=edgecolour,fc='none',lw=1,alpha=0.05)
        plotname[xcount,ycount].add_patch(ellipse)
    
    return variability
