from decimal import *
getcontext().prec=6

def traj_dev(Xtraj,Ytraj,Xmean,Ymean):
    sum=0
    for i in xrange(0,len(Xmean)):
        x_term=Decimal(Xtraj[i])-Xmean[i]
        y_term=Decimal(Ytraj[i])-Ymean[i]
        x_sq=x_term*x_term
        y_sq=y_term*y_term
        sum=Decimal(sum)+x_sq+y_sq
    TD=Decimal(sum/len(Xmean)).sqrt()
