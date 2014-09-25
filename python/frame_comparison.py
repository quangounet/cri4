def compare(time1,time2,time3):

    if len(time1)<len(time2) and len(time1)<len(time3):
        nf=len(time1)
    elif len(time2)<len(time1) and len(time2)<len(time1):
        nf=len(time2)
    else:
        nf=len(time3)

    return nf
