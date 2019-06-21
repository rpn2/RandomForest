import os
import random
'''Class for generating labels for test set '''
class Testing:

    def __init__(self,headtr,testdictf, prlabel = {}):
        
        self.dth = headtr        
        #Preditced label, key is linenum, value is another dictionary. The inner dictionary has key as predicted value and value as number of times that the prediction happened in the past
        self.prlabel = prlabel
        self.ttdict = testdictf

    def parsetestfile(self):
        xp = 0
        
        for key, val in self.ttdict.items():
            xp = xp + 1   
            attval = val[1]
            node = self.dth
            #For each test case, traverse the tree until leaf node is reached
            while(node.type != 0): 
                #Attribute is missing from test set, choose random child 
                if node.attribute not in attval:
                    #pick a random child
                    rkey = random.choice(list(node.childnodes))
                    nextnode = node.childnodes[rkey]                    
                #Attribute value in test set is unseen, choose random child
                elif attval[node.attribute] not in node.childnodes.keys():
                    #pick a random child
                    rkey = random.choice(list(node.childnodes))
                    nextnode = node.childnodes[rkey]                    
                else:
                    nextnode = node.childnodes[attval[node.attribute]]

                node = nextnode
            
            prlkdict = self.prlabel.get(key, dict())
            prlkdictval = prlkdict.get(node.label,0)
            prlkdict[node.label] = prlkdictval + 1            
            self.prlabel[key] = prlkdict 

        return self.prlabel

            


    

    




















                 









