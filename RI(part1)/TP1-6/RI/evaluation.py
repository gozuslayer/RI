import indexation
import numpy as np
import porter
from TextRepresenter import PorterStemmer
from ParserCACM import ParserCACM
import pickle as pkl
import os
from Document import Document
from modeles import *
import collections


class QueryParser(ParserCACM):
	def __init__(self):
		ParserCACM.__init__(self)

	def initFile_query(self,filename):
		self.file=open(filename,"rb")

	def initFile_jugement(self,filename):
		self.file_jugement=open(filename,"rb")
        
	def __del__(self):
		if(self.file is not None):
           		 #print self.file.closed
			self.file.close()
          		 #print str(self.file.closed)

	def nextQuery():
		raise NotImplementedError

class CACM_QueryParser(QueryParser,ParserCACM):
#  * 
#  * Format of input files :
#  * .I <id>
#  * .W
#  * <Text>
#  * .N
#  * <Auteur> 
#  *
#  */
	def __init__(self):
		ParserCACM.__init__(self)

	def initFile_jugement(self,filename):
		self.file_jugement=open(filename,"rb")
		self.getRelevants()

	

	def nextQuery(self):
		#if((self.file is None) or (self.file.closed())):
        	#    return None
        	d=None
        	ligne=""
	        ok=False;
        	while(not ok):
	            st=""
	            read=False;
	            start=0;
	            nbBytes=0;       
	            while(True):
	                curOff=self.file.tell();
	               
	                ligne=self.file.readline();
	                #self.file.seek(curOff,0)
	                #print ligne
		               
                
	                if(len(ligne)==0):
	                    if((len(self.end)==0) and read):
	                        #print ok
	                        nbBytes=curOff-start;
	                        read=False
	                        ok=True
	                    break
	                if(ligne.startswith(self.begin)):
	                    if((len(self.end)==0) and read):
	                        nbBytes=curOff-start;
	                        read=False;
	                        ok=True;
	                        
	                        self.file.seek(curOff)
	                        
	                        break;
	                    else:
	                        read=True
	                        start=curOff                      
	                if(read):
	                    st+=(ligne)
	                if((len(self.end)>0) and (ligne.startswith(self.end))):
	                    read=False
	                    ok=True;
	                    nbBytes=self.file.tell()-start;
	                    break
	            if (ok):
	                source=os.path.abspath(self.file.name)+";"+str(start)+";"+str(nbBytes)
	                #print source
	                query=self.getQuery(st);
	                query.set("from", source);
			ide = int(query.identifier)
			if (ide in self.relevants.keys()):
				relevants = self.relevants[ide]
				query.set("relevants",relevants)
			else:
				query.set("relevants",None)
	            else:
	                self.file.close();
	                return None
	                
	        return query

	def getQuery(self,text):
		other={};
		modeT=False;
		modeA=False;
		modeK=False;
		modeW=False;
		modeX=False;
		info=""
		identifier=""
		author=""
		kw=""
		links=""
		title=""
		texte=""
		
		st=text.split("\n");
		s=""
		for s in st:
		    if(s.startswith(".I")):
		        identifier=s[3:]
		        continue
		    
		    if(s.startswith(".")):
		        if(modeW):
		            texte=info
		            info=""
		            modeW=False
		        
		        if(modeA):
		            author=info
		            info=""
		            modeA=False
		        
		        if(modeK):
		            kw=info;
		            info="";
		            modeK=False;
		        
		        if(modeT):
		            title=info;
		            info="";
		            modeT=False
		        
		        if(modeX):
		            other["links"]=links;
		            info="";
		            modeX=False;
		        
		    
		    
		    if(s.startswith(".W")):
		        modeW=True;
		        info=s[2:];
		        continue;
		    
		    if(s.startswith(".A")):
		        modeA=True;
		        info=s[2:];
		        continue;
		    
		    if(s.startswith(".K")):
		        modeK=True;
		        info=s[2:];
		        continue;
		    
		    if(s.startswith(".T")):
		        modeT=True;
		        info=s[2:];
		        continue;
		    
		    if(s.startswith(".X")):
		        modeX=True
		        continue;
		    
		    if(modeX):
		        l=s.split("\t");
		        if(l[0]!=identifier):
		            if(len(l[0])>0):
		                links+=l[0]+";";
		        
		        continue;
		    
		    if((modeK) or (modeW) or (modeA) or (modeT)):
		        #print "add "+s
		        info+=" "+s
		    
		
	    
		if(modeW):
		    texte=info;
		    info="";
		    modeW=False;
		
		if(modeA):
		    author=info;
		    info="";
		    modeA=False;
		
		if(modeK):
		    kw=info;
		    info="";
		    modeK=False;
		
		if(modeX):
		    other["links"]=links;
		    info=""
		    modeX=False;
		
		if(modeT):
		    title=info;
		    info="";
		    modeT=False;
		
		other["title"]=title
		other["text"]=texte
		other["author"]=author
		other["keywords"]=kw
		
		query=Document(identifier,title+" \n "+author+" \n "+kw+" \n "+texte,other);
		
		return query

	def getRelevants(self):
		jugement = self.file_jugement.readline()
		self.relevants = {}
		while (jugement!=''):
			st =  jugement.split()
			if (int(st[0]) in self.relevants.keys()):
				self.relevants[int(st[0])].append(int(st[1]))
			else :
				self.relevants[int(st[0])]=[int(st[1])]
			jugement = self.file_jugement.readline()


class IRlist():
	def __init__(self,Query,l):
		self.Query = Query
		self.l = l
		
		
class EvalMeasure():
	def set_IRlist(self,IRlist):
		self.IRlist = IRlist

	def eval(self):
		raise NotImplementedError

class PrecisionRappel(EvalMeasure):
    def __init__(self,IRlist):
		self.IRlist = IRlist
  
    def eval(self,NbLevels):
        L=[]
        p=1
        nbr = 0
        r = 0
        k = 0
        L.append([p,r])
        for key in self.IRlist.l.keys():
            if key in self.IRlist.Query.others['relevants']:
                nbr += 1
            k=k+1
            r=nbr/float(len(self.IRlist.Query.others['relevants']))
            p=nbr/float(k)
            L.append([p,r])    
        L = np.array(L)
        print L[1,0]
        result= {}
        print np.linspace(0,1,NbLevels)
        for i in np.linspace(0,1,NbLevels):
            result[i]=np.max(L[np.where(L[:,1]>=i),:],1)[0][0]
        print result
        return result

class PrecisionMoyenne(EvalMeasure):
	def __init__(self,IRlist):
		self.IRlist = IRlist
     
	def eval(self):
		result = {}
		precisions = []
		nbr = 0
		k_doc = 0
		if self.IRlist.Query.others['relevants'] != None :
			for key in self.IRlist.l.keys():
				k_doc += 1
				if key in self.IRlist.Query.others['relevants']:
					nbr += 1
					precisions.append(nbr/float(k_doc))
			nbrPertinent = len(precisions)
			result = (1/float(nbrPertinent))*sum(precisions)
			print result
			return result
		else:
			return 0
		
        
class EvalIRModel():
	def __init__(self,IRModel,name):
		self.IRModel = IRModel
		self.name = name
		
	def evaluate(self,QueryParser,Stemmer):
		AP=[]
		PR = []
		Query = QueryParser.nextQuery()
		while (Query!=None):
			query = Stemmer.getTextRepresentation(Query.others['text'])
			print ("evaluating requete "+ Query.identifier)
			l = self.IRModel.getRanking(query)
			irlist = IRlist(Query,l)
			if (self.name=="AP"):
				evaluation = PrecisionMoyenne(irlist)
				AP.append(evaluation.eval())
			if (self.name=="PR"):
				evaluation = PrecisionRappel(irlist)
				PR.append(evaluation.eval(11))
			Query = QueryParser.nextQuery()
		if (self.name=="AP"):
			print AP
			MAP = sum(AP)/float(len(AP))
			return MAP
		if (self.name=="PR"):
			PR = np.array(PR)
			return PR
			







    
A = PorterStemmer()
parser = ParserCACM()
Index_CACM = Index("cacm", parser, A, "/home/gozuslayer/Bureau/TP1-6/RI/cacm/")       
Weighters = Weighter_1(Index_CACM)

model = Vectoriel(Weighters,Index_CACM)
from modeles import *
L=languageModel(Index_CACM,0.7)
A = PorterStemmer()
Parser = CACM_QueryParser()     
Parser.initFile_query("/home/gozuslayer/Bureau/TP1-6/RI/cacm/cacm.qry")
Parser.initFile_jugement("/home/gozuslayer/Bureau/TP1-6/RI/cacm/cacm.rel")


Eval = EvalIRModel(L,"AP")
print Eval.evaluate(Parser,A)