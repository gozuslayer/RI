import porter
from TextRepresenter import PorterStemmer
from ParserCACM import ParserCACM
import pickle as pkl


class Index():
	def __init__(self, name, parser, textRepresenter, dir):
		self.name = name
		self.docFrom = {}
		self.parser = parser
		self.textRepresenter = textRepresenter
		self.index = {}
		self.index_inverse = {}
		self.dir = dir
		self.index_file = dir + 'index_file'
		self.index_file_inverse = dir + 'index_inverse_file'

	def indexation(self, filename):
		self.parser.initFile(filename)

		#Fichier d'index
		index_file = open(self.index_file, 'wb')
		index_inverse_file = open(self.index_file_inverse, 'wb')
		doc_file = open(filename , 'r')


		# Premiere passe
		doc = self.parser.nextDocument()
		doc_source_place = 0
		doc_place = 0
		stem_place = 0
		print ("STEP COMPUTE")
		while (doc != None):
			id = doc.identifier
			if int(id) > 10:
				break
			print("COMPUTE doc " + str(id))
			print(doc)
			self.docFrom[id] = (filename, doc_source_place, len(doc.text))
			doc_source_place += len(doc.text)
			# Index normal, on "reserve" la place
			bow = self.textRepresenter.getTextRepresentation(doc.text)
			str_bow = self._dict_to_file(bow)
			byte_size = len(str_bow)
			self.index[id] = (doc_place, byte_size)
			doc_place += byte_size
			#Pour chaque stem, on le rajoute en tant que cle
			for i in bow.keys():
				if i not in self.index_inverse.keys():
					# Si il n'existe pas, on initialise sa position et sa longueur a 0
					self.index_inverse[i] = (0, 0)
				#On met a jour sa longueur, si il existe, on addition sa longueur
				self.index_inverse[i] = (0, self.index_inverse[i][1] + len(self._line_to_file(id, bow[i])))
			doc = self.parser.nextDocument()

		#A ce stade, les position sont a 0, on met a jour a partir de la long precedente
		for stem in self.index_inverse.keys():
			self.index_inverse[stem] = (stem_place, self.index_inverse[stem][1])
			stem_place += self.index_inverse[stem][1]


		print("STEP WRITE")
		# Seconde passe
		self.parser.initFile(filename)
		doc = self.parser.nextDocument()
		stem_place = {}
		while (doc != None):
			id = doc.identifier
			if int(id) > 10:
				break
			print("WRITE doc " + str(id))
			# Index normal
			bow = self.textRepresenter.getTextRepresentation(doc.text)
			#Pour chaque doc, on met l'offset a sa position et on ecrit les "stem | tf"
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

		doc_file.flush()
		doc_file.close()
		index_file.flush()
		index_inverse_file.flush()
		index_file.close()
		index_inverse_file.close()

	def getTfsForDoc(self, id_doc):
		index_file = open(self.index_file , 'r')
		index_file.seek(self.index[id_doc][0])
		stem_tf = index_file.read(self.index[id_doc][1])
		index_file.flush()
		index_file.close()
		return stem_tf

	def getTfsForStem(self, stem):
		index_file_inverse = open(self.index_file_inverse, 'r')
		index_file_inverse.seek(self.index_inverse[stem][0])
		doc_tf = index_file_inverse.read(self.index_inverse[stem][1])
		index_file_inverse.flush()
		index_file_inverse.close()
		return doc_tf

	def getStrDoc(self, id_doc):
		f = open(self.docFrom[id_doc][0], 'r')
		f.seek(self.docFrom[id_doc][1])
		doc = f.read(self.docFrom[id_doc][2])
		f.flush()
		f.close()
		return doc


	def _dict_to_file(self, dict):
		return ''.join([self._line_to_file(i, dict[i]) for i in dict.keys()])

	def _line_to_file(self, i, v):
		return str(i) + '|' + str(v) + ' '


tr = PorterStemmer()
parser = ParserCACM()
parser.initFile("C:\Users\king\Desktop\DAC2\RI\TP1-6\RI\cacm\cacm.txt")
doc = parser.nextDocument()
print type(doc.others["links"])


 
