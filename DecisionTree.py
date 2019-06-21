import Training 
import sys
import time
import Testing
import QualityCalc
import ReadTrFile
import ReadTeFile
import utilities

def DTfunc(arg1,arg2,arg3=None):
    #encode tree-depths
    if "balance.scale" in arg1:
        depth = 3
    if "nursery" in arg1:
        depth = 7
    if "led" in arg1:
        depth = 7
    if "synthetic.social" in arg1:
        depth = 8
    #Read training file
    Rf = ReadTrFile.ReadTrFile(arg1)
    #Read Testing file
    Tf = ReadTeFile.ReadTeFile(arg2)

    #Initializer the Trainer class    
    Train = Training.Training(depth,Rf.D,Rf.dictfile,Rf.attributedict,Rf.labeldict,Rf.avcdict)
    #Generate Decision Tree
    trlabeldict, dtroot = Train.GenDT()
    #Initialize Tester
    Test = Testing.Testing(dtroot,Tf.dictfile)
    #Perform Decision Tree based Testing 
    prlabel = Test.parsetestfile()
     
    #Calculate and Print Confusion Matrix 
    cm =  utilities.CalcConMat(Tf.dictfile,prlabel,Rf.labeldict)    

    #Calculate quality of classifer for report
    if arg3 == True:
        QualityCalc.QualityCalc(cm)



if __name__ == "__main__":
    start = time.time() 
    if len(sys.argv)==4 and sys.argv[3] == '1':  
        DTfunc(sys.argv[1],sys.argv[2], True)
    else:
        DTfunc(sys.argv[1],sys.argv[2])
    end = time.time() - start
    #print("Training Time = " , end)


    
    








