
from TextRepresenter import *
from indexation import *
from evaluation import *
from modeles import *


tr = PorterStemmer()
parser = ParserCACM()
index = Index("Clef08", parser, tr, "/media/gozuslayer/Data/Master2DAC/RI/RI(part3)/easyCLEF08/")

#model
Weighter = Weighter_1(index)
model = Vectoriel(Weighter,index)

#QueryParser
Parser = CACM_QueryParser()     
Parser.initFile_query("/media/gozuslayer/Data/Master2DAC/RI/RI(part3)/easyCLEF08/easyCLEF08_query.txt")
Parser.initFile_jugement("/media/gozuslayer/Data/Master2DAC/RI/RI(part3)/easyCLEF08/easyCLEF08_gt_without_comments.txt")

#evaluation
precision = EvalIRModel(model,"P")
pa20 = precision.evaluate(Parser,tr)

