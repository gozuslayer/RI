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
from sklearn.cluster import KMeans
from diversite import *
import time

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
			
			if (len(jugement)>4):
				st =  jugement.split() # st = (IDQuery,IDdoc,pert,soustheme)
				if (int(st[0]) in self.relevants.keys()):
					if ( int(st[3]) in self.relevants[int(st[0])].keys()):
						self.relevants[int(st[0])][int(st[3])].append(int(st[1]))
					else:
						self.relevants[int(st[0])][int(st[3])] = [int(st[1])]
				else :
					self.relevants[int(st[0])] = {}
					self.relevants[int(st[0])][int(st[3])] = [int(st[1])]

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
        result= {}
        for i in np.linspace(0,1,NbLevels):
            result[i]=np.max(L[np.where(L[:,1]>=i),:],1)[0][0]
        return result

class AveragePrecision(EvalMeasure):
	def __init__(self,IRlist):
		self.IRlist = IRlist
     
	def eval(self):
		nbrDocPertinent = 0
		k_doc = 0
		precisions = []

		#check if query have relevants
		if self.IRlist.Query.others['relevants'] != None :

			for key in self.IRlist.l.keys():
				k_doc += 1

				#variable i pour ne pas dire qu'un document est deux fois pertinent malgres plus de un soustheme.
				i=0
				for sousTheme in self.IRlist.Query.others['relevants'].keys():
					if (key in self.IRlist.Query.others['relevants'][sousTheme])&(i==0):
						nbrDocPertinent +=  1
						precisions.append(nbrDocPertinent/float(k_doc))
						i+=1

			nbrPertinent = len(precisions)
			result = (1/float(nbrPertinent))*sum(precisions)
			return result			
		else:
			return 1

class Precision(EvalMeasure):
	'''Precision a n documents'''

	def __init__(self,IRlist):
		self.IRlist = IRlist

	def eval(self,n):
		nbPertRet = 0

		#check for first n items in ranking list
		for key in self.IRlist.l.keys()[:n]:

			#variable a is for checking if doc has multiple sous theme.
			a = False
			for Soustheme in self.IRlist.Query.others['relevants'].keys():
				if (key in self.IRlist.Query.others['relevants'][Soustheme]) & (a == False):

					a= True
					nbPertRet += 1 

		result = nbPertRet / float(n)
		return result

class ClusterRecall(EvalMeasure):
	'''cluster recall a n documents'''

	def __init__(self,IRlist):
		self.IRlist = IRlist

	def eval(self,n):
		nbSousTheme = 0
		SousTheme = set()
		nbTotalSousTheme = len(self.IRlist.Query.others['relevants'].keys())
		
		#check for first n items in ranking list
		ListToEvaluate = self.IRlist.l.keys()[:n]
		for key in ListToEvaluate:
			for soustheme in self.IRlist.Query.others['relevants'].keys():
				if key in self.IRlist.Query.others['relevants'][soustheme]:
					SousTheme.add(soustheme)
		nbSousTheme = len(SousTheme)
		return nbSousTheme / float(nbTotalSousTheme)
        
class EvalIRModel():
	def __init__(self,IRModel,name):
		self.IRModel = IRModel
		self.name = name
		
	def evaluate(self,QueryParser,Stemmer,at=20,nbLevels = 11,diversite=False,type_diversite='clustering',nb_cluster=10,nbr_Doc_considere=100,alpha=0.95):
		AP = []
		PR = []
		P = []
		CR = []
		i=0
		Query = QueryParser.nextQuery()
		while (Query!=None):
			# measure process time
			print ("evaluating requete "+ Query.identifier)
			t0 = time.clock()
			query = Stemmer.getTextRepresentation(Query.others['text'])
			
			l = self.IRModel.getRanking(query)			
			irlist = IRlist(Query,l)
			print irlist.l.keys()[:at]

			#Adding algorithme diversite
			if (diversite==True):
				if (type_diversite=='clustering'):
					kmeans = KMeans(n_clusters=nb_cluster)
					reorder = diversite_by_clustering(irlist,self.IRModel.Index)
					irlist = reorder.fit_transform(nbr_Doc_considere,nb_cluster,kmeans)
					print irlist.l.keys()[:at]
				if (type_diversite=='glouton'):						
					reorder = diversite_by_glouton(irlist,self.IRModel.Index)
					irlist = reorder.fit_transform(nbr_Doc_considere,alpha)
					print irlist.l.keys()[:at]


			if (self.name == "AP"):
				evaluation = AveragePrecision(irlist)
				AP.append(evaluation.eval())
			if (self.name=="PR"):
				evaluation = PrecisionRappel(irlist)
				PR.append(evaluation.eval(nbLevels))
			if (self.name == "P"):
				evaluation = Precision(irlist)
				P.append(evaluation.eval(at))
			if (self.name == "CR"):
				evaluation = ClusterRecall(irlist)
				CR.append(evaluation.eval(at))

			print 'evaluation time for requete : {}'.format(time.clock() - t0)
			Query = QueryParser.nextQuery()

		if (self.name=="AP"):
			MAP = sum(AP)/float(len(AP))
			return MAP
		elif (self.name=="PR"):
			PR = np.array(PR)
			return PR
		elif (self.name=="P"):
			P = sum(P)/float(len(P))
			return P
		elif (self.name=="CR"):
			CR = sum(CR)/float(len(CR))
			return CR
		else:
			raise NotImplementedError
			

