import os

class ReadTrFile:

    def __init__(self,filename):
       
        #Index of all data tuples
        self.D = []
        #Parse the input file and store as dictionary
        self.dictfile ={}
        #Key is attribute, value is the set of values that an attribute can take
        #self.attributelist = set()

        self.attributedict = {}
        #key is label, value if number of occurences of label
        self.labeldict = {}
        
        #AVC dictionary
        self.avcdict = {}

        self.parsefile(filename)

    def parsefile(self,filename):

        fn  = open(os.path.abspath(filename), "r")
        trlines = fn.readlines()
        fn.close()
        #Key is index, value is 2 element list, first element is label, second element is dictinary with attribute, value pairs
        m = 0
        for line in trlines:           
            temp = line.rstrip().split(" ")
            vallist = []
            atval = {}
            for x in range(0,len(temp)):
                if x == 0:  
                    temp0int = int(temp[0])                
                    vallist.append(temp0int)
                    vallabel = self.labeldict.get(temp0int, 0)                    
                    self.labeldict[temp0int] = vallabel + 1
                else:
                    attrsplit = temp[x].split(":")
                    attrsplit0int = int(attrsplit[0])
                    attrsplit1int = int(attrsplit[1])
                    atval[attrsplit0int] = attrsplit1int

                    val = self.attributedict.get(attrsplit0int,dict())
                    valval = val.get(attrsplit1int,0)                    
                    val[attrsplit1int] = valval + 1 
                    self.attributedict[attrsplit0int] = val

                    #Construct AVC for each Attribute, Value, label
                    avctemp =[]
                    avctemp.append(attrsplit0int)
                    avctemp.append(attrsplit1int)
                    avctemp.append(temp0int)
                    avctup = tuple(avctemp)
                    avcdictval = self.avcdict.get(avctup,0)                    
                    self.avcdict[avctup] = avcdictval + 1

            vallist.append(atval)
            self.dictfile[m] = vallist
            self.D.append(m)
            m = m + 1