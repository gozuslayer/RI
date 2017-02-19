#Optimisation des parametres
Queries = []
parser = CACM_QueryParser()
parser.initFile_query("/home/gozuslayer/Bureau/TP1-6/RI/cacm/cacm.qry")
parser.initFile_jugement("/home/gozuslayer/Bureau/TP1-6/RI/cacm/cacm.rel")
query = parser.nextQuery()
while (query!=None):
    Queries.append(query)
    query = parser.nextQuery()
nbrQuery = len(Queries)
Queries = shuffle(Queries)
sizeQtrain = round(nbrQuery*0.8)
sizeQtest = nbrQuery - sizeQtrain
Qtrain = Queries[:sizeQtrain-1]
Qtest = Queris[sizeQtrain:]

lambdas_to_search = np.linspace(0,1,5)
k1_to_search = np.linspace(1,2,5)
b_to_search = np.linspace(0.5,1,3)

#eval
Parser = CACM_QueryParser()		
Parser.initFile_query("/home/gozuslayer/Bureau/TP1-6/RI/cacm/cacm.qry")
Parser.initFile_jugement("/home/gozuslayer/Bureau/TP1-6/RI/cacm/cacm.rel")
Query = Parser.nextQuery()

A = PorterStemmer()
query = A.getTextRepresentation(Query.others['text'])

parser = ParserCACM()
Index_CACM = Index("cacm", parser, A, "/home/gozuslayer/Bureau/TP1-6/RI/cacm/")
print Index_CACM.getStrDoc('248')
print Index_CACM.getStrDoc('1410')			
Weighters = Weighter_1(Index_CACM)

model = Vectoriel(Weighterq,Index_CACM)
V = IRlist(Query,model.getRanking(query))
A = PrecisionRappel(V).eval(10)

print model.getRanking(query)
print Query

