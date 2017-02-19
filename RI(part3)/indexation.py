import porter
from TextRepresenter import PorterStemmer
from ParserCACM import ParserCACM
import pickle as pkl


class Index():
	def __init__(self, name, parser, textRepresenter, dir):
		self.name = name
		self.parser = parser
		self.docFrom = {}
		self.textRepresenter = textRepresenter
		self.index = {}
		self.index_inverse = {}
		self.links = {}
		self.dir = dir
		self.index_file = dir + name + '_index'
		self.index_file_inverse = dir + name + '_index_inverted'
		self.index_file_position = dir + name + '_index_position'
		self.index_inverse_file_position = dir + name + '_index_inverse_position'
		self.docFrom_file = dir + name + '_docFrom'
		self.links_file = dir + name + '_links'
		self.nbrDoc = 4203
		

	def indexation(self, filename):
		#Parse le fichier corpus
		self.parser.initFile(filename)

		#Fichier Index et Index_inverse
		index_file = open(self.index_file, 'wb')
		index_inverse_file = open(self.index_file_inverse, 'wb')
		

		# Premiere passe
		doc = self.parser.nextDocument()

		#initialisation des positions dans le fichier index_inverse
		doc_source_place = 0
		doc_place = 0
		stem_place = 0
		
		#Calcul des positions et longueurs des stem dans les fichiers index et index_inverse
		print ("STEP COMPUTE")
		while (doc != None):
			id = doc.identifier
			print("Computing doc " + str(id))
			self.docFrom[id] = doc.others['from'].split(";")
			
			# Index normal, on "reserve" la place
			bow = self.textRepresenter.getTextRepresentation(doc.text)
			
			str_bow = self._dict_to_file(bow)

			#add links
			#self.links[id] = doc.others["links"]
			
			stem_byte_size = len(str_bow)
			self.index[id] = (doc_place, stem_byte_size)
			doc_place += stem_byte_size

			#Pour chaque stem, on le rajoute en tant que cle
			for stem in bow.keys():
				if stem not in self.index_inverse.keys():
					# Si il n'existe pas, on initialise sa position et sa longueur a 0
					self.index_inverse[stem] = (0, 0)


				#On met a jour sa longeur
				self.index_inverse[stem] = (0, self.index_inverse[stem][1] + len(self._line_to_file(id, bow[stem])))

			#prochain document
			doc = self.parser.nextDocument()

		#A ce stade, les position sont a 0, on met a jour a partir de la long precedente
		for stem in self.index_inverse.keys():
			self.index_inverse[stem] = (stem_place, self.index_inverse[stem][1])
			stem_place += self.index_inverse[stem][1]

		# Seconde passe
		print("STEP WRITE")
		self.parser.initFile(filename)
		doc = self.parser.nextDocument()
		stem_place = {}
		while (doc != None):
			id = doc.identifier
			
			print("Writing doc " + str(id))
			bow = self.textRepresenter.getTextRepresentation(doc.text)

			#Index
			#aller a la position du doc et Ecrire 
			index_file.seek(self.index[id][0])
			index_file.write(self._dict_to_file(bow))
			#Index inverse
			#On prend la position dans index_reverse...
			for stem in bow.keys():
				if stem not in stem_place.keys():
					stem_place[stem] = self.index_inverse[stem][0]
				#L'offset est place a la position du stem et on ecrit "id_doc | tf"
				index_inverse_file.seek(stem_place[stem])
				index_inverse_file.write(self._line_to_file(id, bow[stem]))

				#Pour le meme stem, la position est additionee par sa longueur
				stem_place[stem] = stem_place[stem] + len(self._line_to_file(id, bow[stem]))
			doc = self.parser.nextDocument()
		
		#serialisation dans un pickle
		index_pickle = pkl.Pickler(open(self.index_file_position,'wb'))
		index_pickle.dump(self.index)
		
		index_inverse_pickle = pkl.Pickler(open(self.index_inverse_file_position,'wb'))
		index_inverse_pickle.dump(self.index_inverse)

		links_pickle = pkl.Pickler(open(self.links_file,'wb'))
		links_pickle.dump(self.links)

		Doc_from_pickle = pkl.Pickler(open(self.docFrom_file,'wb'))
		Doc_from_pickle.dump(self.docFrom)

		index_file.flush()
		index_inverse_file.flush()
		index_file.close()
		index_inverse_file.close()

	def getTfsForDoc(self, id_doc):
		index_file = open(self.index_file, 'r')
		index = pkl.Unpickler(open(self.index_file_position,'rb')).load()
		index_file.seek(index[id_doc][0])
		stem_tf = index_file.read(index[id_doc][1])
		index_file.flush()
		index_file.close()
		return stem_tf

	def getLinksForDoc(self,id_doc):
		links_file = pkl.Unpickler(open(self.links_file, 'r')).load()
		links = links_file[id_doc]
		return links

	def getTfsForStem(self, stem):
		index_file_inverse = open(self.index_file_inverse, 'r')
		index_inverse = pkl.Unpickler(open(self.index_inverse_file_position,'rb')).load()
		if (stem in index_inverse.keys()):	
			index_file_inverse.seek(index_inverse[str(stem)][0])
			doc_tf = index_file_inverse.read(index_inverse[stem][1])
			return doc_tf
			index_file_inverse.flush()
			index_file_inverse.close()
		else:
			index_file_inverse.flush()
			index_file_inverse.close()
			return None
		

	def getStrDoc(self, id_doc):
		docFrom = pkl.Unpickler(open(self.docFrom_file,'rb')).load()
		f = open(docFrom[id_doc][0], 'r')
		f.seek(int(docFrom[id_doc][1]))
		doc = f.read(int(docFrom[id_doc][2]))
		f.flush()
		f.close()
		return doc


	def _dict_to_file(self, dict):
		return ''.join([self._line_to_file(i, dict[i]) for i in dict.keys()])

	def _line_to_file(self, i, v):
		return str(i) + '|' + str(v) + ' '
