import numpy as np
from indexation import *
import porter
from TextRepresenter import PorterStemmer
from ParserCACM import ParserCACM
import pickle as pkl
from collections import OrderedDict

class Weighter():
	def __init__(self,Index):
		self.Index=Index

	def weight_t_d(self,x):
		if x>0:
			return 1+np.log(x)
		else:
			return 0

	def weight_t_q(self,x):
		index = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load()
		docsHaveStem = self.Index.getTfsForStem(x)
		nbrDocAyantStem = len(docsHaveStem.split())
		nbrDoc = len(index.keys())
		idf = np.log((1+nbrDoc)/(1+nbrDocAyantStem))
		return idf
		
	
	def getWeightsForDoc(self,idDoc):
		result ={}
		Doc = self.Index.getTfsForDoc(idDoc).split()
		for i in Doc:
			stem, tf = i.split('|')
			
			result[stem]= self.weight_t_d(int(tf))
		return result
		

	def getDocWeightsForStem(self,stem):
		result={}
		Stem = self.Index.getTfsForStem(stem).split()
		for i in Stem:
			if len(i) == 0 :
				break
			idDoc, tf = i.split('|')
			result[idDoc]= self.weight_t_d(int(tf))
		return result

	def getWeightsForQuery(self,query):
		result={}
		for i in query.keys():
			result[i]=self.weight_t_q(i)
		return result

class Weighter_1(Weighter):
	def weight_t_d(self,tf_d):
		return tf_d

	def weight_t_q(self,tf):
		return 1

class Weighter_2(Weighter):
	def weight_t_d(self,tf_d):
		return tf_d
	
	def weight_t_q(self,tf_q):
		return tf_q

class Weighter_3(Weighter):
	def weight_t_d(self,tf_d):
		return tf_d

	def weight_t_q(self,tf_q):
		return Idf_t

class Weighter_4(Weighter):
	def weight_t_d():
		return 1+np.log(x)

	def weight_t_q(tf_q):
		return 1

class Weighter_5(Weighter):
	def weight_t_d(x):
		return 1+np.log(x)


class IRmodel():
	def __init__(self,Index):
		self.Index = Index

	def getScores(self,query):
		raise NotImplementedError

	def getRanking(self,query):
		result={}
		result=self.getScores(query)
		index_file_position = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load()
		for idDoc in index_file_position.keys():
			if (int(idDoc) not in result.keys()):
				result[int(idDoc)]=0
		result = OrderedDict(sorted(result.items(), key=lambda t: t[1], reverse=True))
		return result

class Vectoriel(IRmodel):
	def __init__(self,Weighter,Index,normalized=False):
		self.Weighter = Weighter
		self.Index = Index
		self.normalized = normalized
		self.first_query = True
		self.sumDocsWeights = 0 

	def getScores(self,query):
		result = {}
		DicQueryWeights = self.Weighter.getWeightsForQuery(query)
		if self.normalized==False:
			for stem in query:
				DicWeigthsDoc = self.Weighter.getDocWeightsForStem(stem)
				for IdDoc in DicWeigthsDoc.keys():
					if IdDoc in result.keys():
						result[int(IdDoc)] += DicWeigthsDoc[IdDoc]*DicQueryWeights[stem]
					else:
						result[int(IdDoc)] = DicWeigthsDoc[IdDoc]*DicQueryWeights[stem]
		if self.normalized==True:
			sumQueryWeights = np.square(np.array(self.Weighter.getWeightsForQuery(query).values())).sum()
			if self.first_query == True:
				doc = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load()
				for i in doc.keys():
					
					DicDocWeights = self.Weighter.getWeightsForDoc(i)
					self.sumDocsWeights += np.array([i*i for i in self.Weighter.getWeightsForDoc(i).values()])
				self.sumDocsWeights = np.square(self.sumDocsWeights)
				self.first_query = False
			for stem in query.keys():
				DicWeightsDoc = self.Weighter.getDocWeightsForStem(stem)
				for IdDoc in DicWeigthsDoc.keys():
					result[int(IdDoc)] += DicWeigthsDoc[IdDoc]*QueryWeights[stem]
			
			result[int(IdDoc)] = result[int(IdDoc)]/(self.sumDocsWeights*sumQueryWeights)
		return result


		
		
