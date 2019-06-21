'''Class to calculate Quality metrics'''

class QualityCalc:
    def __init__(self, cm):
        self.cm = cm
        self.labelcnt = {}
        self.labeltp = {}
        self.labelfn = {}   
        self.labelqual = {}
        self.labelfp = {}
        self.labeltn = {}
        x = 1   
        self.total = 0

        for row in self.cm:
            self.labelcnt[x] = sum(row)
            x = x + 1
            self.total = self.total + sum(row)
        truecnt = 0
        for i in range(0,len(self.labelcnt)):
            fncnt = 0
            for j in range(0,len(self.labelcnt)):
                if (i == j):                    
                    self.labeltp[i+1] = self.cm[i][j]
                    truecnt = truecnt + self.cm[i][j]
                else:
                    fncnt = fncnt + self.cm[i][j]
                    fpcnt = self.labelfp.get(j+1, 0)
                    self.labelfp[j+1] = fpcnt + self.cm[i][j]
            self.labelfn[i+1] = fncnt

          
        
        OverallAccuracy = truecnt/self.total

        print("Total = ", self.total)
        
        #Calculate True Negative for each class
        for key in self.labelcnt.keys():
            self.labeltn[key] = self.total -  self.labeltp[key] - self.labelfn[key] - self.labelfp[key]

        print("Overall Accuracy = ", OverallAccuracy)

        print("Debug")
        for key in self.labelcnt.keys():
            print("class = ", key)
            print(self.labeltp[key], self.labelfn[key])
            print(self.labelfp[key], self.labeltn[key])


        #For each class get results
        for key in self.labelcnt.keys():
            qual = []
            #Accuracy of each class : percentage of each class elements correctly identified : TP + TN/(TP+FN+FP+TN)
            acc = (self.labeltp[key] + self.labeltn[key])/(self.total)
            qual.append(acc)
            

            #Specificity = True Negative Rate: TN/(TN+FP)
            if (self.labeltn[key] + self.labelfp[key] != 0):
                spec = self.labeltn[key]/(self.labeltn[key] + self.labelfp[key])
                qual.append(spec)
            else:
                qual.append("NA")

            

            #Precision = TP/(TP+FP)
            if ((self.labeltp[key] + self.labelfp[key]) !=0 ):
                prec = self.labeltp[key]/(self.labeltp[key] + self.labelfp[key])
                qual.append(prec)
            else:
                qual.append("NA")
                prec = 0

            

            #Recall = TP/(TP+FN)
            if ((self.labeltp[key] + self.labelfn[key]) !=0 ):
                recall = self.labeltp[key]/(self.labeltp[key] + self.labelfn[key])
                qual.append(recall)
            else:
                qual.append("NA")
                recall = 0
            

            #F1 score 
            if(prec + recall != 0):
                f1score = (2*prec*recall)/(prec + recall)
                qual.append(f1score)

                #F-Beta 0.5 score
                beta1 = 0.5 * 0.5
                fbeta1= ((1+beta1)*prec*recall)/(beta1*prec + recall)
                qual.append(fbeta1)

                #F-Beta 2 score
                beta2 = 2 * 2
                fbeta2= ((1+beta2)*prec*recall)/(beta2*prec + recall)
                qual.append(fbeta2)
            else:
                qual.append("NA")
                qual.append("NA")
                qual.append("NA")


            self.labelqual[key] = qual

            print("Class = ", key)
            print("acc,spec,prec,recall,f1,f1b0.5,f1b2")
            print(qual)
















