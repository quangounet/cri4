from numpy import *
from matplotlib.patches import Ellipse
from pylab import *
import matplotlib.pyplot as plt
plt.figure()
xy1=(1,1)
xy2=(1,2)
xy3=(2,1)
xy4=(2,2)
xy5=(2,2)

xy6=(1,3)
xy7=(3,1)
xy8=(2,3)
xy9=(3,2)
xy10=(3,3)



ax=gca()

ellipse1=Ellipse(xy1,4,5,10,edgecolor='none',fc='c',lw=1,alpha=0.05)
ellipse2=Ellipse(xy2,4,5,10,edgecolor='none',fc='c',lw=1,alpha=0.01)
ellipse3=Ellipse(xy3,4,5,10,edgecolor='none',fc='c',lw=1,alpha=0.01)
ellipse4=Ellipse(xy4,4,5,10,edgecolor='r',fc='r',lw=1,alpha=0.05)
ellipse5=Ellipse(xy5,4,5,10,edgecolor='r',fc='r',lw=1,alpha=0.01)
ellipse6=Ellipse(xy6,4,5,10,edgecolor='r',fc='r',lw=1,alpha=0.01)
ellipse7=Ellipse(xy7,4,5,10,edgecolor='r',fc='r',lw=1,alpha=0.05)
ellipse8=Ellipse(xy8,4,5,10,edgecolor='r',fc='r',lw=1,alpha=0.01)
ellipse9=Ellipse(xy9,4,5,10,edgecolor='none',fc='c',lw=1,alpha=0.01)
ellipse10=Ellipse(xy10,4,5,10,edgecolor='none',fc='c',lw=1,alpha=0.5)


ax.add_patch(ellipse1)
ax.add_patch(ellipse2)
ax.add_patch(ellipse3)
ax.add_patch(ellipse4)
ax.add_patch(ellipse5)
ax.add_patch(ellipse6)
ax.add_patch(ellipse7)
ax.add_patch(ellipse8)
ax.add_patch(ellipse9)
ax.add_patch(ellipse10)

plt.xlim(-10,10)
plt.ylim(-10,10)

plt.show()
