from decimal import *
getcontext().prec=6
import matplotlib.pyplot as plt

def normalize(a):
    t=range(0,len(a))
    tnew=[]
    for i in xrange(0,len(a)):
        tnew.append(Decimal(t[i])/Decimal(len(a)))
    plt.plot(tnew,a)

