from decimal import * #importing decimal fixed point arithmetic
getcontext().prec=6 #specifying decimal places to 6

def mean_calc(nf,x1,x2,x3,y1,y2,y3,xval1,xval2,xval3,yval1,yval2,yval3):
    sample,meanX,meanY=[],[],[]
    X_axis1,X_axis2,X_axis3,Y_axis1,Y_axis2,Y_axis3=[],[],[],[],[],[]
    for i in xrange(0,nf):
    	sample.append(Decimal(i)/nf)
    	X_axis1.append(xval1[sample[i]*len(x1)])
    	Y_axis1.append(yval1[sample[i]*len(y1)])       
    	X_axis2.append(xval2[sample[i]*len(x2)])
    	Y_axis2.append(yval2[sample[i]*len(y2)])    
    	X_axis3.append(xval3[sample[i]*len(x3)])
    	Y_axis3.append(yval3[sample[i]*len(y3)]) 
    	meanX.append(Decimal((X_axis1[i]+X_axis2[i]+X_axis3[i]))/3)
    	meanY.append(Decimal((Y_axis1[i]+Y_axis2[i]+Y_axis3[i]))/3)
	
    return meanX,meanY,sample,X_axis1,X_axis2,X_axis3,Y_axis1,Y_axis2,Y_axis3

