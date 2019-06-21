
import os
import copy
import random

'''Generalized Class that contains training related functions for DecisionTree '''
class Training:

    def __init__(self, ht= 4, D = [], dictf = {}, attdict = {}, labeldict = {},  avcdict = {}):
       
        #Index of all data tuples
        self.D = D
        #Parse the input file and store as dictionary
        self.dictfile = dictf
        #Key is attribute, "value" is a dictionary. Key of "value" dictionary is attribute value and value is number of occurences of an "attribute value" 
        self.attributedict = attdict
        #key is label, value if number of occurences of label
        self.labeldict = labeldict
        self.treeht = ht
        #AVC dictionary
        self.avcdict = avcdict
        

    '''Node class representing nodes of a Decision Tree'''
    class dtnode:
        def __init__(self):
            #Arrtribute used for split
            self.attribute = None
            #Two types of nodes, internal is 1, leaf is 0. By default all nodes are considered internal
            self.type = 1
            #Pointers to child nodes, where is key is attribute value and value is pointer to childnode 
            self.childnodes = {}
            # Label is assigned only for leaf nodes
            self.label = None
            #Keep track of total tuples at this node
            self.totaltuples = 0
            #Depth at which node is formed
            self.depth = None
            

        #Function to set a node to be leaf and assign a type
        def setleaf(self,label):
            self.type = 0
            self.label = label
    
        #Assign the child nodes
        def setchild(self, attrival, node):
            self.childnodes[attrival] = node
    
    #Function to call the recursive version of Decision Tree generator
    def GenDT(self):
        DThead = self.generatetree(self.D,self.attributedict, self.labeldict,self.avcdict,0)
        return self.labeldict, DThead

    #Single Decsion Tree generator, Recursive function
    def generatetree(self,D,al,cl,avc,depth):
        N = self.dtnode()
        N.totaltuples = len(D)
        N.depth = depth
         
        al = copy.deepcopy(al) 
        
        #If tuples are of same class       
        if len(cl) == 1:
            for key in cl.keys(): 
                temp = key              
            N.setleaf(temp) 
            return N

        #If attribute list is empty or depth is achieved, majority voting for leaf node
        if len(al) == 0 or self.treeht == depth:
            label = max(cl,key = cl.get)
            N.setleaf(label)            
            return N
       

        #Select an attribute
        attribute = self.AttributeSelection(D,al,cl,avc) 
        #Set the attribute used for split in node
        N.attribute = attribute
        #Delete the attribute from overall attribute list
        del al[attribute]
        #Create a branch for each attribute value
        for attributeval in self.attributedict[attribute]:
            Dj = []
            clj = {}
            alj = {}
            avcdictj = {}
            for Dval in D:
                val = self.dictfile[Dval]
                attdict = val[1]
                #Need a check to verify if attribute exists in attdict
                if attribute in attdict and attdict[attribute] == attributeval:
                    Dj.append(Dval)
                    cljval = clj.get(val[0], 0)                    
                    clj[val[0]] = cljval + 1
                    #Build local AVC and AL for the subset of data
                    for attdictkey,attdictval in attdict.items():
                        if attdictkey in al: 
                            aljval = alj.get(attdictkey,dict())
                            aljvalval = aljval.get(attdictval,0)                            
                            aljval[attdictval] = aljvalval + 1
                            alj[attdictkey] = aljval
                            avctemp =[]
                            avctemp.append(attdictkey)
                            avctemp.append(attdictval)
                            avctemp.append(val[0])
                            avctemptup = tuple(avctemp)
                            avcval = avcdictj.get(avctemptup,0)                           
                            avcdictj[avctemptup] = avcval + 1
            #If number of tuples is zero in a branch, create a leaf and assign majority class as label
            if len(Dj) == 0:
                label = max(cl,key = cl.get)                 
                N1 = self.dtnode()
                N1.depth = depth
                N1.setleaf(label)                
                N.childnodes[attributeval] = N1
                N1.parent = N.attribute
                N1.parentval = attributeval
                N1.totaltuples = 0
            else:
                N1= self.generatetree(Dj,alj,clj,avcdictj,depth+1)               
                N.childnodes[attributeval] = N1
                N1.parent = N.attribute
                N1.parentval = attributeval
        return N
    
    #Function to calculate Gindex of given attributes in al and return one attribute with minimum gindex
    def AttributeSelection(self,D,al,cl,avc):
        attgindex ={}     
        total = len(D)  
        for attribute,values in al.items():
            temp = []
            temp.append(attribute)
            agsum = 0            
            for attributeval,valcnt in values.items():
                temp.append(attributeval)
                ginisum = 0                
                for label in cl.keys():
                    temp.append(label)
                    temptup = tuple(temp)                    
                    avcval = avc.get(temptup,0)
                    #calculating Gini(D1)
                    ginisum = ginisum + (avcval/valcnt)**2
                    temp.remove(label)
                tempgindex = 1 - ginisum                
                agsum = agsum + (valcnt/total) * tempgindex
                temp.remove(attributeval)
            #store gindex 
            attgindex[attribute] = agsum
           
        #minatt = min(attgindex,key=attgindex.get)
        minval = min(attgindex.values())
        mklist = []
        for k,v in attgindex.items():
            if v == minval:
                mklist.append(k)
        #minatt = mklist[random.randint(0,len(mklist)-1)]
        #minatt = mklist[len(mklist)-1]
        minatt = random.choice(mklist)
        return minatt
    
     
    def GenDTRF(self,numatt = 3):
        self.numatt = numatt
        ldict = self.generateinputs()
        DThead = self.generatetreeRF(self.D,ldict,0)
        return DThead

    #Generate local label dict of a  given data set
    def generateinputs(self):
        cld = {}    
        for Dval in self.D:
            val = self.dictfile[Dval]            
            cldval = cld.get(val[0], 0)                    
            cld[val[0]] = cldval + 1
        return cld

    #Single Decsioon Tree generator for Random Forest,, Recursive function
    def generatetreeRF(self,D,cl,depth):
        N = self.dtnode()
        N.totaltuples = len(D)
        N.depth = depth
        #If tuples are of same class 
             
        if len(cl) == 1:
            for key in cl.keys(): 
                temp = key              
            N.setleaf(temp) 
                       
            return N
        
        #depth limited tree
        if self.treeht == depth:
            label = max(cl,key = cl.get)            
            N.setleaf(label)
            return N


        attribute = self.AttributeSelectionRF(D,cl)         
        N.attribute = attribute
        #For each attrubute value, create a branch
        for attributeval in self.attributedict[attribute]:
            Dj = []
            clj = {}
           
            for Dval in D:
                val = self.dictfile[Dval]
                attdict = val[1]
                #Need a check to verify if attribute exists in attdict
                if attribute in attdict and attdict[attribute] == attributeval:
                    Dj.append(Dval)
                    cljval = clj.get(val[0], 0)                    
                    clj[val[0]] = cljval + 1                    
            if len(Dj) == 0:
                label = max(cl,key = cl.get)                
                N1 = self.dtnode()
                N1.depth = depth
                N1.setleaf(label)
                N.childnodes[attributeval] = N1
                N1.parent = N.attribute
                N1.parentval = attributeval
                N1.totaltuples = 0
               
                
            else:
                N1= self.generatetreeRF(Dj,clj,depth+1)               
                N.childnodes[attributeval] = N1
                N1.parent = N.attribute
                N1.parentval = attributeval
        return N

    def AttributeSelectionRF(self,D,cl):
        attgindex ={}
        altemp = []
        

        #Pick self.numatt attributes at random
        for x in range(0,self.numatt):
            rkey = random.choice(list(self.attributedict))
            altemp.append(rkey)
        
        
        #Build local AVC and AL dictionary
        avc = {}
        al = {}
        for Dval in D:
            val = self.dictfile[Dval]
            attdict = val[1]
            for attdictkey,attdictval in attdict.items():
                if attdictkey in altemp:  
                    alval = al.get(attdictkey,dict())
                    alvalval = alval.get(attdictval,0)                            
                    alval[attdictval] = alvalval + 1
                    al[attdictkey] = alval                   
                    avctemp =[]
                    avctemp.append(attdictkey)
                    avctemp.append(attdictval)
                    avctemp.append(val[0])
                    avctemptup = tuple(avctemp)
                    avcval = avc.get(avctemptup,0)                           
                    avc[avctemptup] = avcval + 1



        #Choose an attribute for split based on Giniindex
        total = len(D)
        for attribute,values in al.items():
            temp = []
            temp.append(attribute)
            agsum = 0
            
            for attributeval,valcnt in values.items():
                temp.append(attributeval)
                ginisum = 0                
                for label in cl.keys():
                    temp.append(label)
                    temptup = tuple(temp)                    
                    avcval = avc.get(temptup,0)
                    #calculating Gini(D1)
                    ginisum = ginisum + (avcval/valcnt)**2
                    temp.remove(label)
                tempgindex = 1 - ginisum                
                agsum = agsum + (valcnt/total) * tempgindex
                temp.remove(attributeval)
            #store gindex 
            attgindex[attribute] = agsum
        
        #Find minimum gindex and return it    
        #minatt = min(attgindex,key=attgindex.get)
        minval = min(attgindex.values())
        mklist = []
        for k,v in attgindex.items():
            if v == minval:
                mklist.append(k)
        #minatt = mklist[len(mklist)-1]
        minatt = random.choice(mklist)
        return minatt


    #Helper function for debug
    def printDT(self, head):
        print("Print DT")
        qnodes = []
        qnodes.append(head)
        depthcount = {}
        globalcnt = 0

        while(qnodes):
            n1 = qnodes.pop(0)
            #print(n1.attribute,n1.type,n1.label,n1.parent,n1.parentval,n1.totaltuples,n1.childnodes.keys())
            #print(n1.attribute,n1.type,n1.label,n1.depth,n1.totaltuples)
            count = depthcount.get(n1.depth,0)
            depthcount[n1.depth] =  count + n1.totaltuples
            if n1.type == 0 :
                globalcnt = globalcnt + n1.totaltuples
            #print(n1.attribute,n1.type,n1.label, n1.depth)
            for key, val in n1.childnodes.items():
                qnodes.append(val)

        #print("debug")
        for key,val in depthcount.items():
            print(key,val)

        print("globalcnt = ",globalcnt)

    

    #Helper function for debug
    def printfile(self):
        print("AttributeList = ", self.attributedict)
        print("LabelList = ", self.labeldict)
        print("Indexlist = ", self.D)
        print("avcdict = ", self.avcdict)
        print("Dictfile")
        for key, val in self.dictfile.items():
            print(key,val)

    







    







        









