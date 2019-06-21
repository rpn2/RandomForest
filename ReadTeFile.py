import os

class ReadTeFile:

    def __init__(self,filename):
       
        
        #Parse the input file and store as dictionary, key is line number and value is file contents
        self.dictfile ={}          
        
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
                    
                else:
                    attrsplit = temp[x].split(":")
                    attrsplit0int = int(attrsplit[0])
                    attrsplit1int = int(attrsplit[1])
                    atval[attrsplit0int] = attrsplit1int
            vallist.append(atval)
            self.dictfile[m] = vallist            
            m = m + 1


    def printtestfile(self):
        for key, val in self.dictfile.items():
            print(key, val)