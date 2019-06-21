''' File that has utilities for Confusion matrix calculation'''
def CalcConMat(ttdict,prlabel,trlabeldict):
 
    #dictionary with key as (truelabel, predicted label), value is count
    trpr = {}

    for key,val in ttdict.items():
        #ldict is a dictionary of labels assigned to a test case with its associated count
        
        
        truelabel = val[0]
        ldict = prlabel[key]
        #majority voting for labels
        assignedlabel = max(ldict,key = ldict.get) 
        temp =[]
        temp.append(truelabel)
        temp.append(assignedlabel)
        temptup = tuple(temp)

        #trpr
        trprval = trpr.get(temptup,0)
        trpr[temptup] = trprval + 1


    #BuildCM 
    labels = sorted(trlabeldict.keys())
    cm = []
    for x in range(0, len(labels)):
        temp = []
        for y in range(0,len(labels)):
            index = []
            index.append(labels[x])
            index.append(labels[y])
            tupindex = tuple(index)
            temp.append(trpr.get(tupindex,0))
        cm.append(temp)

    for row in cm:
        print(*row)

    return cm












