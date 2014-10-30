from numpy import *
from pylab import *
from matplotlib.patches import Ellipse

ion()

data = array([[0.5,1], [-0.5,-1], [-0.2,-1], [0.2,0.8 ]])
data2 = array(data)

meanx = mean(data[:,0])
meany = mean(data[:,1])

for i in range(data.shape[0]):
    data2[i,0] = data[i,0] - meanx
    data2[i,1] = data[i,1] - meany


clf()
plot(data[:,0],data[:,1],"ro",markersize=5)
axis([-2,2,-2,2])


ax = gca()

xy = (meanx,meany)
u,d,v = linalg.svd(data2)
width = 2*d[0]
height = 2*d[1]
angle = arctan2(v[0,1],v[0,0])*180/pi

ellipse = Ellipse(xy, width, height, angle, edgecolor='r', fc='None', lw=2)
ax.add_patch(ellipse)


