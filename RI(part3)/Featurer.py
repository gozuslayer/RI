from evaluation import *

class Featurer():
	def __init__(self,index):
		self.index = index
		self.features = {}

	def getFeatures(self,idDoc,query):
		raise NotImplementedError

class FeaturerModel(Featurer):
	def __init__(self,model):
		Featurer.__init__()
		self.model = model
		self.name = str(model)

	def getFeatures(self,idDoc,query):
		if (self.features == {}):
			self.features = model.getScores(query)
			return self.features[idDoc]
		else:
			return self.features[idDoc]

class FeaturerList(Featurer):
	def __init__(self,ListFeaturer):
		Featurer.__init__():
		for element in ListFeaturer:
			self.features[element.name] = element.features

class MetaModel(IRmodel):
	def __init__(self,Index,FeaturerList,QueryParser):
		self.Index = Index
		self.FeaturerList = FeaturerList
		self.parameters = np.random.randn(len(FeaturerList),1)
		self.QueryParser = QueryParser
		self.Queries = {}
		self.getTableOfQueries()

	def getTableOfQueries(self):
		Query = self.QueryParser.nextQuery()
		while (Query!=None):
			self.Queries[int(Query.identifier)] = Query
			Query = QueryParser.nextQuery()

class My_MetaModel(MetaModel):

	def getScoresForDoc(self,idDoc):
		#TODO for every doc
		result = {}
		Xd_q = np.random.randn(1,len(self.FeaturerList))
		i=0
		for element,feature in self.FeaturerList.features:
			Xd_q[0,i] = feature[idDoc,query]
		result[idDoc] = Xd_q*self.parameters
		return result

	def ltheta(self):

		ltheta=0
		for Query in self.Queries:
			nbrDocPertinentPourQuery = len(Query.others["relevants"])
			nbrDocNonPertinent = 4203 - nbrDocPertinentPourQuery
			Docs = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load().keys()
			docNonPertinent = [i for i in Docs if i not in Query.others["relevants"]]
			for idDocPertinent in Query.others["relevants"]:
				for idDocNonPertinent in docNonPertinent:
					ltheta += (1/float(nbrDocNonPertinent*nbrDocPertinentPourQuery))*np.max(0,1-self.getScoresForDoc(idDocPertinent,query)+self.getScoresForDoc(idDocNonPertinent,query))
		ltheta += lamb*np.sqrt(self.parameters.T*self.parameters)
		return ltheta

	def gradient_stochastique(self,learning_rate,tmax,lamb):
		Ltheta = {}
		nbrQuery = len(self.Queries.keys())
		for i in range(tmax):
			idx = np.random.randint(nbrQuery,1)
			Query = self.Queries[idx]
			nDp = len(Query.others['relevants'])
			idx_Pertinent = np.random.randint(nDp)
			DocPert = Query.others['relevants'][idx_Pertinent]
			Docs = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load().keys()
        	nDnp = len(Docs)
        	idx_nonPertinent = np.random.randint(nDnp)
        	while int(Docs[idx_nonPertinent]) in Query.others['relevants']:
        		idx_nonPertinent = np.random.randint(nDnp)
        	DocNonPert = int(Docs[idx_nonPertinent])
        	res = 1 - self.getScoresForDoc(DocPert) + self.getScoresForDoc(DocNonPert)
        	if res > 0:
        		#TODO
        		self.parameters = self.parameters + learning_rate*(Xd_q - Xd_q)

        	self.parameters = (1 - 2*learning_rate*lamb)*self.parameters
        	Ltheta[i] = self.ltheta()








