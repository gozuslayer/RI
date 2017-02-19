
from TextRepresenter import *
from indexation import *
from evaluation import *
from modeles import *
from diversite import *

tr = PorterStemmer()
parser = ParserCACM()
index = Index("Clef08", parser, tr, "/media/gozuslayer/Data/Master2DAC/RI/RI(part3)/easyCLEF08/")

#model
Weighter = Weighter_2(index)
model = Vectoriel(Weighter,index,normalized=True)

#QueryParser
Parser = CACM_QueryParser()     
Parser.initFile_query("/media/gozuslayer/Data/Master2DAC/RI/RI(part3)/easyCLEF08/easyCLEF08_query.txt")
Parser.initFile_jugement("/media/gozuslayer/Data/Master2DAC/RI/RI(part3)/easyCLEF08/easyCLEF08_gt_without_comments.txt")

#evaluation sur cluster recall
precision = EvalIRModel(model,"CR")
CR20 = precision.evaluate(Parser,tr)
CR20Cluster = precision.evaluate(Parser,tr,diversite=True)
CR20glouton = precision.evaluate(Parser,tr,diversite=True,type_diversite='glouton')

print CR20,CR20glouton,CR20Cluster
#evaluation sur cluster recall
precision = EvalIRModel(model,"P")
P20 = precision.evaluate(Parser,tr)
P20Cluster = precision.evaluate(Parser,tr,diversite=True)
P20glouton = precision.evaluate(Parser,tr,diversite=True,type_diversite='glouton')

print P20,P20glouton,P20Cluster
