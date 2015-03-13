def T_test(patient, control):
    difference=[]
    dsquare=[]
    for i in xrange(0,len(patient)):
        difference.append(patient[i]-control[i])
        dsquare.append(difference[i]**2)
    sum_list=[]
    sum_list.append(sum(patient))
    sum_list.append(sum(control))
    sum_list.append(sum(difference))
    sum_list.append(sum(dsquare))
    mean_list=[]
    mean_list.append(float(sum_list[0]/len(patient)))
    mean_list.append(float(sum_list[1]/len(control)))
    mean_list.append(float(sum_list[2]/len(difference)))
    mean_list.append(float(sum_list[3]/len(dsquare)))
    
    n=len(patient)
    t_value=sum_list[2]/(((n*sum_list[3])-(sum_list[2])**2)/(n-1))**(0.5)
    DoF=n-1

    return t_value, DoF
    
