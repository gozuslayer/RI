#TME2
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

    def weight_t_d(self,idDoc,stem):
        raise NotImplementedError

    def weight_t_q(self,query,stem):
        raise NotImplementedError

    def getDocWeightsForDoc(self,idDoc):
        raise NotImplementedError

    def getDocWeightsForStem(self,stem):
        raise NotImplementedError

    def getWeightsForQuery(self,query):
        raise NotImplementedError

class Weighter_1(Weighter):
    

    def weight_t_d(self,tf):
        return tf

    def weight_t_q(self,stem,query):
        if (stem in query):
            return 1 
        else:
            return 0
        
    def getDocWeightsForDoc(self,idDoc):
        result ={}
        stem_tf = self.Index.getTfsForDoc(idDoc).split()
        for i in stem_tf:
            stem, tf = i.split('|')
            result[stem] = self.weight_t_d(int(tf))
        return result
        
    def getDocWeightsForStem(self,stem):
        result={}
        idDoc_tf = self.Index.getTfsForStem(stem)
        if (idDoc_tf!=None):
            idDoc_tf = idDoc_tf.split()
            for i in idDoc_tf:
                idDoc, tf = i.split('|')
                result[idDoc]= self.weight_t_d(int(tf))
        return result

    def getWeightsForQuery(self,query):
        result={}
        for stem in query.keys():
            result[stem]=self.weight_t_q(stem,query)
        return result

class Weighter_2(Weighter):
    

    def weight_t_d(self,tf):
        return tf

    def weight_t_q(self,tf):
        return tf
        
    def getDocWeightsForDoc(self,idDoc):
        result ={}
        stem_tf = self.Index.getTfsForDoc(idDoc).split()
        for i in stem_tf:
            stem, tf = i.split('|')
            result[stem] = self.weight_t_d(int(tf))
        return result
        
    def getDocWeightsForStem(self,stem):
        result={}
        idDoc_tf = self.Index.getTfsForStem(stem)
        if (idDoc_tf!=None):
            idDoc_tf = idDoc_tf.split()
            for i in idDoc_tf:
                idDoc, tf = i.split('|')
                result[idDoc]= self.weight_t_d(int(tf))
        return result

    def getWeightsForQuery(self,query):
        result={}
        for stem,tf in query.items():
            result[stem]=self.weight_t_q(tf)
        return result

class Weighter_3(Weighter):
    
    def weight_t_d(self,tf):
        return tf

    def weight_t_q(self,stem,query):
        if (stem in query):
            index = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load()
            docsHaveStem = self.Index.getTfsForStem(stem)
            if (docsHaveStem!=None):
                nbrDocAyantStem = len(docsHaveStem.split())
            else:
                nbrDocAyantStem = 0
            docFrom = pkl.Unpickler(open(self.Index.docFrom_file,'rb')).load()
            nbrDoc = len(docFrom.keys())
            idf = np.log((1+nbrDoc)/(1+nbrDocAyantStem))
            return idf
        else:
            return 0
        
    def getDocWeightsForDoc(self,idDoc):
        result ={}
        stem_tf = self.Index.getTfsForDoc(idDoc).split()
        for i in stem_tf:
            stem, tf = i.split('|')
            result[stem] = self.weight_t_d(int(tf))
        return result
        
    def getDocWeightsForStem(self,stem):
        result={}
        idDoc_tf = self.Index.getTfsForStem(stem)
        if (idDoc_tf!=None):
            idDoc_tf = idDoc_tf.split()
            for i in idDoc_tf:
                idDoc, tf = i.split('|')
                result[idDoc]= self.weight_t_d(int(tf))
        return result

    def getWeightsForQuery(self,query):
        result={}
        for stem,tf in query.items():
            result[stem]=self.weight_t_q(stem,query)
        return result

class Weighter_4(Weighter):
    
    def weight_t_d(self,tf):
        if tf>0:
            return 1+np.log(tf)
        else:
            return 0

    def weight_t_q(self,stem,query):
        if (stem in query):
            index = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load()
            docsHaveStem = self.Index.getTfsForStem(stem)
            if (docsHaveStem!=None):
                nbrDocAyantStem = len(docsHaveStem.split())
            else:
                nbrDocAyantStem = 0
            docFrom = pkl.Unpickler(open(self.Index.docFrom_file,'rb')).load()
            nbrDoc = len(docFrom.keys())
            idf = np.log((1+nbrDoc)/(1+nbrDocAyantStem))
            return idf
        else:
            return 0
        
    def getDocWeightsForDoc(self,idDoc):
        result ={}
        stem_tf = self.Index.getTfsForDoc(idDoc).split()
        for i in stem_tf:
            stem, tf = i.split('|')
            result[stem] = self.weight_t_d(int(tf))
        return result
        
    def getDocWeightsForStem(self,stem):
        result={}
        idDoc_tf = self.Index.getTfsForStem(stem)
        if (idDoc_tf!=None):
            idDoc_tf = idDoc_tf.split()
            for i in idDoc_tf:
                idDoc, tf = i.split('|')
                result[idDoc]= self.weight_t_d(int(tf))
        return result

    def getWeightsForQuery(self,query):
        result={}
        for stem,tf in query.items():
            result[stem]=self.weight_t_q(stem,query)
        return result

class Weighter_5(Weighter):
    
    def weight_t_d(self,tf,stem):
        if tf>0:
            docsHaveStem = self.Index.getTfsForStem(stem)
            if (docsHaveStem!=None):
                nbrDocAyantStem = len(docsHaveStem.split())
            else:
                nbrDocAyantStem = 0
            nbrDoc = self.Index.nbrDoc
            idf = np.log((1+nbrDoc)/(1+nbrDocAyantStem))
            return 1+np.log(tf)*idf
        else:
            return 0

    def weight_t_q(self,tf,stem):
        if (tf>0):
            docsHaveStem = self.Index.getTfsForStem(stem)
            if (docsHaveStem!=None):
                nbrDocAyantStem = len(docsHaveStem.split())
            else:
                nbrDocAyantStem = 0
            docFrom = pkl.Unpickler(open(self.Index.docFrom_file,'rb')).load()
            nbrDoc = len(docFrom.keys())
            idf = np.log((1+nbrDoc)/(1+nbrDocAyantStem))
            return 1+np.log(tf)*idf
        else:
            return 0
        
    def getDocWeightsForDoc(self,idDoc):
        result ={}
        stem_tf = self.Index.getTfsForDoc(idDoc)
        print stem_tf
        if (stem_tf!=None):
            stem_tf.split()
            for i in stem_tf:
                stem, tf = i.split('|')
                result[stem] = self.weight_t_d(int(tf),stem)
        return result
        
    def getDocWeightsForStem(self,stem):
        result={}
        idDoc_tf = self.Index.getTfsForStem(stem)
        if (idDoc_tf!=None):
            idDoc_tf = idDoc_tf.split()
            for i in idDoc_tf:
                idDoc, tf = i.split('|')
                result[idDoc]= self.weight_t_d(int(tf),stem)
        return result

    def getWeightsForQuery(self,query):
        result={}
        for stem,tf in query.items():
            result[stem]=self.weight_t_q(tf,stem)
        return result

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
        self.DocsWeights = {} 

    def getScores(self,query):
        result = {}
        DicQueryWeights = self.Weighter.getWeightsForQuery(query)
        if self.normalized==False:
            for stem in query.keys():
                DicWeigthsDoc = self.Weighter.getDocWeightsForStem(stem)
                for IdDoc in DicWeigthsDoc.keys():
                    if IdDoc in result.keys():
                        result[int(IdDoc)] += DicWeigthsDoc[IdDoc]*DicQueryWeights[stem]
                    else:
                        result[int(IdDoc)] = DicWeigthsDoc[IdDoc]*DicQueryWeights[stem]
        if self.normalized==True:
            sumQueryWeights = np.sqrt(np.array([i*i for i in self.Weighter.getWeightsForQuery(query).values()]).sum())
            for stem in query.keys():
                DicWeightsDoc = self.Weighter.getDocWeightsForStem(stem)
                for IdDoc in DicWeightsDoc.keys():
                    if int(IdDoc) not in result.keys():
                        result[int(IdDoc)] = DicWeightsDoc[IdDoc]*DicQueryWeights[stem]
                    else:
                        result[int(IdDoc)] += DicWeightsDoc[IdDoc]*DicQueryWeights[stem]
            for idDoc in result.keys():
                if idDoc in self.DocsWeights.keys():
                    result[int(IdDoc)] = result[int(IdDoc)]/(self.DocsWeights[int(idDoc)]*sumQueryWeights)
                else:
                    self.DocsWeights[idDoc] = np.sqrt(np.array([i*i for i in self.Weighter.getDocWeightsForDoc(str(idDoc)).values()]).sum())
                    result[int(idDoc)] = result[int(idDoc)]/(self.DocsWeights[int(idDoc)]*sumQueryWeights)
        return result

#TME4

class languageModel(IRmodel):
    
    def __init__(self,Index,lamb):
        self.Index = Index
        self.getAllDocProbability()
        self.lamb=lamb
        
    def getScores(self,query):
        result={}
        
        for stem in query.keys():
            PMc_stem,Docs = self.getProbabilityStemCorpus(stem)
            Docs = self.Index.getTfsForStem(stem)
            idDoc = []
            if Docs!=None:
                Docs = Docs.split()
                for element in Docs:
                    idD, Tf = element.split('|')
                    idDoc.append(idD)
                    PMd_stem = self.AllDocProbability[idD][stem]
                    if idD in result.keys():
                        result[idD] += query[stem]*(np.log(self.lamb*PMd_stem + (1-self.lamb)*PMc_stem))
                    else:
                        result[idD] = query[stem]*(np.log(self.lamb*PMd_stem + (1-self.lamb)*PMc_stem))
                
            #Ajout sur Doc n'ayant pas le stem
            DocSansStem = [i for i in self.IdTotalDocs if i not in idDoc] 
            print idDoc,DocSansStem 
            for idD in DocSansStem:
                if idD in result.keys():
                    result[idD] += query[stem]*(np.log((1-self.lamb)*PMc_stem))
                else:
                    result[idD] = query[stem]*(np.log((1-self.lamb)*PMc_stem))
        return result
                
    def getDocProbability(self,idDoc):
        print ("calculating probabilities for " + idDoc)
        result={}
        sumTf = 0
        stem_tfs = self.Index.getTfsForDoc(idDoc).split()
        for element in stem_tfs:
            Stem,Tf = element.split('|')
            sumTf += int(Tf)
            result[Stem]=int(Tf)
        
        for i in result.keys():
            result[Stem]=result[Stem]/float(sumTf)
        return result
        
    def getAllDocProbability(self):
        result={}
        index = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load()
        for idDoc in index.keys():
            result[idDoc] = self.getDocProbability(idDoc)
        self.IdTotalDocs = index.keys()
        self.NbrTotalDocs = len(index.keys())
        self.AllDocProbability = result
        
    def getProbabilityStemCorpus(self,stem):
        result={}
        DocsAyantStem = self.Index.getTfsForStem(stem)
        if DocsAyantStem != None:
            DocsAyantStem = DocsAyantStem.split()
            nbrDocsAyantStem = len(DocsAyantStem)
            result = nbrDocsAyantStem/self.NbrTotalDocs
        else:
            result = 1
        return result
        
class BM25(IRmodel):
    def __init__(self,Index,k1,b):
        self.Index = Index
        self.k1 = k1
        self.b = b
        self.getAllLongueurDoc()
        self.getLongueurMoyenneDoc()
        
    def getScores(self,query):
        result={}
        for stem in query.keys():
            Docs_tf = self.Index.getTfsForStem(stem).split()
            NbrDocAyantStem = len(Doc_Tf)
            Idf_Stem = max(0,np.log((self.NbrTotalDoc - NbrDocAyantStem + 0.5)/float(NbrDocAyantStem + 0.5)))
            for element in Docs_tf:
                IdDoc,Tf = element.split('|')
                if IdDoc in result.keys():
                    result[IdDoc] += Idf_Stem * (   ((self.k1+1)*int(Tf)) / (self.k1*((1-self.b)+self.b*self.AllLongueurDoc[IdDoc]/self.LongueurDocMoyenne) + int(Tf)))
                else:
                    result[IdDoc] = Idf_Stem * (   ((self.k1+1)*int(Tf)) / (self.k1*((1-self.b)+self.b*self.AllLongueurDoc[IdDoc]/self.LongueurDocMoyenne) + int(Tf)))
        return result
                    
                    
    def getLongueurDoc(self,idDoc):
        print("computing longueur doc " + idDoc)
        DL = 0
        stem_tfs = self.Index.getTfsForDoc(idDoc).split()
        for element in stem_tfs:
            Stem,Tf = element.split('|')
            DL += int(Tf)
        return DL

    def getAllLongueurDoc(self):
        result={}
        index = pkl.Unpickler(open(self.Index.index_file_position,'rb')).load()
        self.IdTotalDocs = index.keys()
        for idDoc in self.IdTotalDocs :
            result[idDoc] = self.getLongueurDoc(idDoc)
        self.AllLongeurDoc = result
        self.NbrTotalDoc = len(index.keys())


    def getLongueurMoyenneDoc(self):
        self.LongueurDocMoyenne = sum(self.AllLongueurDoc.values())/float(self.NbrTotalDoc)

class OptimizationParameters():
    def __init__(self,Queries,IRModel):
        self.Queries = Queries
        self.IRModel = IRModel

    def getTrainTest(self):
        NbrQueries = len(self.Queries)
        AllQueries = shuffle(self.Queries)
        sizeQtrain = floor(0.7*AllQueries)
        train = AllQueries[:sizeQtrain]
        test = sizeQtrain[(sizeQtrain + 1 ):]
        return train,test

    