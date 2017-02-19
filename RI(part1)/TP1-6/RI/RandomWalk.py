from indexation import *
import numpy as np

class RandomWalk():
	def __init__(self,index):
		self.index = index
		self.graph = {}
		self.completeGraph = {}
		self.DocTotal = 0
		self.matrix_adjacency = np.random.randn(self.DocTotal)
		self.matrix_transition = np.random.randn(self.DocTotal)
		self.node_degree = np.zeros(1,self.DocTotal)
		self.marche = np.ones(1,self.DocTotal)*(1/self.DocTotal)

	def get_graph(self,scores):
		doc = pkl.Unpickler(open(self.index.index_file_position,'rb')).load()
		for id in scores.keys():
			if (self.index.getLinksForDoc()>2):
				links = self.index.getLinksForDoc()
				links = links.split(";")
				self.graph[i] = links
				self.DocTotal += 1

		for id in doc.keys():
			if (self.index.getLinksForDoc()>2):
				links = self.index.getLinksForDoc()
				links = links.split(";")
				self.completeGraph[i] = links
		return self.graph

	def get_matrix_adjacency(self):
		k=0
		l=0

		for i in self.graph.keys():
			node_deg = 0
			for j in self.graph.keys():
				if (i in self.graph[j]):
					self.matrix_adjacency[k,l]=1/len(self.graph[j])
					node_deg +=1
				elif (i not in self.graph[j]):
					self.matrix_adjacency[k,l]=0
				l+=1
			self.node_degree[0,i] = node_deg
			k+=1


	def get_matrix_transition(self):
		self.matrix_transition = self.matrix_adjacency*self.node_degree


class PageRank(RandomWalk):
	def __init__(self,index,damping,error):
		self.index = index
		self.graph = {}
		self.completeGraph = {}
		self.DocTotal = 0
		self.matrix_adjacency = np.random.randn(self.DocTotal)
		self.matrix_transition = np.random.randn(self.DocTotal)
		self.node_degree = np.zeros(1,self.DocTotal)
		self.marche = np.ones(1,self.DocTotal)*(1/self.DocTotal)
		self.damping = damping
		self.error = error

	def get_rank(self):
		delta = 1
		rank = self.marche
		while (delta>self.error):
			newrank = ((1-self.damping)/self.DocTotal)*np.ones(1,self.DocTotal) + matrix_transition*rank
			delta = np.abs(newrank - rank).sum()
			rank = newrank
		return rank
    
class Hits(RandomWalk):
	def __init__(self,index,error):
		self.index = index
		self.graph = {}
		self.completeGraph = {}
		self.DocTotal = 4203
		self.matrix_adjacency = np.random.randn(self.DocTotal)
		self.matrix_transition = np.random.randn(self.DocTotal)
		self.node_degree = np.zeros(1,self.DocTotal)
		self.marche = np.ones(1,self.DocTotal)*(1/self.DocTotal)
		self.authorities = np.ones(1,self.DocTotal)
		self.hubs = np.ones(1,self.DocTotal)
		self.error = error

	def get_rank(self):
		delta = 1
		hubs = self.hubs
		authorities = self.authorities
		while (delta > self.error) :
			new_hubs  = (self.matrix_adjacency*authorities).sum(axis=0)
			new_authorities = (self.matrix_adjacency*hubs).sum(axis=0)
			norme_hubs = math.sqrt((new_hubs*new_hubs).sum())
			norme_authorities = math.sqrt((new_hubs*new_authorities).sum())
			new_hubs = new_hubs/norme_hubs
			new_authorities = new_authorities/norme_authorities
			delta = np.abs(new_authorities - authorities).sum()
			hubs, authorities = new_hubs, new_authorities
		return authorities


class search_model():
	def __init__(self,model,nbrDocumentSeed):
		self.model = model
		self.nbrDocumentSeed = nbrDocumentSeed
		


	def marche_aleatoire(self,query,RandomWalk,k):
		#Initialisation de VQ
		scores = self.model.getScores(query)[:self.nbrDocumentSeed]
		VQ = RandomWalk.get_graph(scores)

		add_to_VQ = []
		#Construction de VQ
		for keys,values in VQ:
			for element in values:
				if element not in VQ.keys():
					add_to_VQ += element

		#get complete graph
		
		AllGraph = RandomWalk.completeGraph
		for ID in VQ:
			add_to_VQ2 = []
			for keys in AllGraph.keys():
				if ID in AllGraph[keys]:
					add_to_VQ2 += keys
					
			#selectionner aléatoirement k docs
			nb_elem = k 
			indices = []  
			while nb_elem > 0:  
    			i = random.randint(0, len(add_to_VQ2) -1)  
    			while i in indices: # tant que le tirage redonne un nombre déjà choisi  
        			i = random.randint(0, len(add_to_VQ2) -1)  
    		 	indices.append(i)  
    			nb_elem = nb_elem - 1  
			resultat = []  				
			for index in indices:  
    			resultat.append(add_to_VQ2[index])
    		add_to_VQ += resultat

    	#Get final VQ
    	AllNodes = set(VQ.keys() + add_to_VQ)
    	RandomWalk.graph = { key: AllGraph[key] for key in AllNodes}
    	result = RandomWalk.get_rank()
    	return result













				
				
