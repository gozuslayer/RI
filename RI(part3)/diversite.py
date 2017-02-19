from sklearn.cluster import KMeans
from indexation import *
from modeles import *
import numpy as np
from collections import OrderedDict

def getRepresentationOfDoc(IDdoc,Dic,Index):
	VectorRep = []
	stem_doc = {}
	StemsOfDoc = Index.getTfsForDoc(str(IDdoc))
	Stem_Tf = StemsOfDoc.split()
	for element in Stem_Tf:
		stem,tf = element.split('|')
		stem_doc[stem] = tf

	for stem in Dic:
		if stem in stem_doc.keys():
			VectorRep.append(stem_doc[stem])
		else:
			VectorRep.append(0)
	return np.array(VectorRep)



def getRepresentationOfAllDoc(DocConsidere,Index):

	index_inverse = pkl.Unpickler(open(Index.index_inverse_file_position,'rb')).load()
	Dic = index_inverse.keys()
	result = np.zeros((len(DocConsidere),len(Dic)))
	i=0
	for IDdoc in DocConsidere:
		result[i,:] = getRepresentationOfDoc(IDdoc,Dic,Index)
		i+=1
	return result

def set_with_order(data):
	f = []
	for item in data:
	    if item not in f:
	        f.append(item)
	return f

def move_element(odict, thekey, newpos):
    odict[thekey] = odict.pop(thekey)
    i = 0
    for key, value in odict.items():
        if key != thekey and i >= newpos:
            odict[key] = odict.pop(key)
        i += 1
    return odict

def get_range(dictionary, table):
  	return OrderedDict((k, v) for k, v in dictionary.iteritems() if k in table)

def get_order_labels(DocConsidere,groups,DictRanking,nbrCluster):
	IDdocs = DictRanking.keys()
	Average = []
	for i in range(nbrCluster):
		A=0
		for j in np.array(DocConsidere)[np.where(groups==i)]:
			A = A + DictRanking[j]
		A = A/len(np.array(DocConsidere)[np.where(groups==i)])
		Average.append(A)
	res = get_index_ranking(Average)
	print np.array(DocConsidere)[np.where(groups==i)]
	return res	

def get_order_labels2(DocConsidere,groups,DictRanking,nbrCluster):
	res = []
	for element in groups:
		if element not in res:
			res.append(element)
	print groups
	print res
	return res	

def get_index_ranking(table):
	res = np.array(table)
	res=np.argsort(res)[::-1]
	print result
	return res


	

class diversite_by_clustering():
	def __init__(self,IRlist,Index):
		self.IRlist = IRlist
		self.Index = Index
		

	def fit_transform(self,nbrDocConsidere,nbrCluster,algo_clustering):
		DocConsidere = self.IRlist.l.keys()[0:nbrDocConsidere]
		Data = getRepresentationOfAllDoc(DocConsidere,self.Index)
		algo_clustering.fit(Data)
		groups = algo_clustering.labels_
		Ranking = OrderedDict()
		labels = get_order_labels2(DocConsidere,groups,self.IRlist.l,nbrCluster)
		decalage=0
		for i in range(nbrDocConsidere):

			#getting ID of next document
			label = labels[(i+decalage)%len(labels)]
			TailleCluster = np.where(groups==label,1,0).sum()
			while ( (i/len(labels)+1)>TailleCluster ):
				decalage +=1
				label = labels[(i+decalage)%len(labels)]
				TailleCluster = np.where(groups==label,1,0).sum()
			Id = np.array(DocConsidere)[np.where(groups==label)][i/len(labels)]

			Ranking[Id] = self.IRlist.l[Id]
		self.IRlist.l = Ranking

		return self.IRlist
		
def distanceEuclidienne(X,Y):
	X = np.sqrt(X.dot(X.T))*X
	Y = np.sqrt(Y.dot(Y.T))*Y
	return np.sqrt(   (   (X-Y).dot(np.array([(X-Y)]).T)  ) )

import math

def similarite(X):
	return math.exp(-X)



def getMatrixSimilariteEuclidienne(Data):
	'''Data in shape(n,1)'''
	n = Data.shape[0]
	result = np.zeros((n,n))
	for i in range(n):
		for j in range(i):
			result[i,j]=similarite(distanceEuclidienne(Data[i,:],Data[j,:]))
	return result


class diversite_by_glouton():
	def __init__(self,IRlist,Index):
		self.IRlist = IRlist
		self.Index = Index

	def fit_transform(self,nbrDocConsidere,alpha):
		DocConsideres= self.IRlist.l.keys()[0:nbrDocConsidere]
		DocConsidere = [i for i in DocConsideres]
		Data = getRepresentationOfAllDoc(DocConsidere,self.Index)
		MatrixDistance = getMatrixSimilariteEuclidienne(Data)


		Ranking = OrderedDict()
		pivot = []
		for i in range(nbrDocConsidere):
			#initialisation
			ValueMMR = np.zeros((len(DocConsidere),1))
			Similarite2 = np.zeros( (len(DocConsidere),len(pivot)) )
			
			

			for j in range(len(DocConsidere)):

				#extracting Similarity between doc and pivot
				if pivot==[]:
					ValueMMR[j,0] = alpha*np.array([self.IRlist.l[DocConsidere[j]]])
				else:
					if len(pivot)==1:
						Similarite2[j] = MatrixDistance[  DocConsideres.index(DocConsidere[j]) , DocConsideres.index(pivot[0])]
						Similarite2bis = Similarite2
					else:
						for k in range(len(pivot)):

							Similarite2[j,k] = MatrixDistance[  DocConsideres.index(DocConsidere[j]) , DocConsideres.index(pivot[k])]
						Similarite2bis = np.max(Similarite2,axis=1)
					
					#calculating Value for each doc not in pivot
					ValueMMR[j,0] = alpha*np.array([self.IRlist.l[DocConsidere[j]]]) - (1-alpha)*np.array([Similarite2bis[j]])


			IDdocIndex = np.argmax(ValueMMR)

			IDdoc = DocConsidere[IDdocIndex]
			Ranking[IDdoc]=ValueMMR[IDdocIndex,0]
			#remove doc and add to pivot
			DocConsidere.remove(IDdoc)
			pivot.append(IDdoc)


		self.IRlist.l = Ranking
		return self.IRlist







