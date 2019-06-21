import Training 
import sys
import time
import Testing
import QualityCalc
import random
import ReadTrFile
import ReadTeFile
import utilities


def RTfunc(arg1,arg2,arg3=None):
    

    #encode num-trees
    if "balance.scale" in arg1:
        numtrees = 150 
        numatt = 2 
        depth = 2 
        databag = 1     
    if "nursery" in arg1:
        numtrees = 100
        numatt = 8
        depth = 7
        databag = 1
    if "led" in arg1:
        numtrees = 65
        numatt = 7
        depth = 7
        databag = 1
    if "synthetic.social" in arg1:
        numtrees = 135
        numatt = 12
        depth = 8
        databag = 1

    #Read Training file
    Rf = ReadTrFile.ReadTrFile(arg1)

    #Read Testing file
    Tf = ReadTeFile.ReadTeFile(arg2)

    #Build DT's and test them 
    prlabel = {}
    for x in range(0,numtrees):
        Dr = []
        size = len(Rf.D)
        for y in range(0,size):
            #Sampling with replacement
            if databag == 1:
                index = random.randint(0,size-1)
            else:
                index = y
            Dr.append(Rf.D[index])
        Train = Training.Training(depth,Dr,Rf.dictfile,Rf.attributedict)
        dtroot = Train.GenDTRF(numatt)
        Test = Testing.Testing(dtroot,Tf.dictfile,prlabel)
        prlabel = Test.parsetestfile()
    

    #Calculate Confusion Matrix for Random forest results
    cm =  utilities.CalcConMat(Tf.dictfile,prlabel,Rf.labeldict)      

    #Calculate quality
    if arg3 == True:
        QualityCalc.QualityCalc(cm)





if __name__ == "__main__":
    start = time.time() 
    if len(sys.argv)==4 and sys.argv[3] == '1':  
        RTfunc(sys.argv[1],sys.argv[2], True)
    else:
        RTfunc(sys.argv[1],sys.argv[2])
    end = time.time() - start
    #print("Training Time = " , end)