#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Authors:
#
# Sebastian Spaar <spaar@stud.uni-heidelberg.de>
# Dennis Ulmer <d.ulmer@stud.uni-heidelberg.de>
#
# Project:
# CrOssinG (CompaRing Of AngliciSmS IN German)
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from sklearn import linear_model
import cPickle as pickle
import numpy as np
import FileManager
import sys

class TransformationMatrix(object):
    """A class

    """


    def __init__(self, T, b, model, alpha):
        """doc
        """

        self.T = (np.matrix(T))
        self.b = np.transpose(np.matrix(b))
        self.model = model
        self.alpha = alpha

    def __mul__(self, v):
        return self.T * v + self.b


class VectorTransformator(object):
    """A flexible object that creates transformations matrices


    """


    def __init__(self, dict_file, vector1_file, vector2_file, isWord2Vec=True):
        """hmm
        """
        
        self.Dictionary = FileManager.readDictionary(dict_file)
        self.Models = []        # consists of all vector transformation models

        if isWord2Vec:
            self.V = FileManager.readWord2Vec(vector1_file)
            self.W = FileManager.readWord2Vec(vector2_file)
        else:
            self.V = FileManager.readVectors(vector1_file)
            self.W = FileManager.readVectors(vector2_file)

    def createTransformationMatrix(self, model="Lasso", alpha=0.1):
        """Creates a transformation matrix from vs1 to vs2.
        """

        if model == "ridge":
            clf = linear_model.Ridge(alpha)
        elif model == "net":
            clf = linear_model.ElasticNet(alpha)
        else:
            clf = linear_model.Lasso(alpha)

        m = len(self.V.values()[0])
        X = []
        Y = []
        T = []
        b = []


        # The transformation matrix is calculated using the following vectors:
        # Vectors of V that also appear in language 1 in the word dictionary AND
        # that have a translation, according to the dictionary, found in Vector
        # space W.
        subDict = [s for s in self.Dictionary if s in self.V and self.Dictionary[s] in self.W]

        for word in subDict:
            X.append(self.V[word])
            Y.append(self.W[self.Dictionary[word]])

        if len(X) == len(Y):
            if len(map(list, zip(*X))) == len(map(list, zip(*Y))):
                print "X, Y are aligned!"

        Yt = map(list, zip(*Y))

        for i in xrange(0, m):
            print "Starting fit with Yt[" + str(i) + "] = " + str(Yt[i])
            clf.fit(X, Yt[i])
            row = []
            for j in clf.coef_:
                row.append(j)
            T.append(row)
            b.append(clf.intercept_)

        self.Models.append(TransformationMatrix(T, b, model, alpha))

    def translateAllVectors(self, intoFile=None):
        """
        """

        
        allResults = {}
        results = {}
        for model in self.Models:
            for v in self.V:
                results[v] = model * self.prepareVector(self.V[v])
            allResults[model] = results
        
        if intoFile:
            with open(intoFile, "w") as fout:
                for model in allResults:
                    print >> fout, "### " + str(model.model) + "_" + str(model.alpha)
                    
                    for v in allResults[model]:
                        print >> fout, v + " " + str(self.V[v])
                        vt = allResults[model][v].flatten()
                        print >> fout, " ---> " + str(vt) + "\n"
                    
                    print >> fout, "\n"

        return allResults


    def prepareVector(self, v):
        """Prepares a vector from a vector space dictonary to use with
        addition/multiplication.
        """
        
        return np.transpose(np.matrix(v))

    def __mul__(self, v):
        if self.Models == []:
            print "You first have to create some models!"
            return

        if type(v) == str:
            if v not in self.Dictionary:
                print v + " not found in Dictionary. Aborting ..."
                return
            
            results = [model * self.prepareVector(self.V[v]) for model in self.Models]
            return tuple(results)

        if type(v) == list:
            print v
            results = [model * self.prepareVector(v) for model in self.Models]
            return tuple(results)

    def __getitem__(self, index):
        return self.Models[index]

if __name__ == "__main__":
    print "################################"
    vt = VectorTransformator("res/dict.txt", "res/de_small.txt", "res/en_small.txt")
    
    vt.createTransformationMatrix()
    vt.createTransformationMatrix("Lasso", 0.01)
    vt.createTransformationMatrix("Lasso", 0.5)

    vt.translateAllVectors("results.txt")
    # print vt * "apfel"
    # print vt.V["apfel"]
    # print vt * [7.0, 2.0, 8.0, 9.0, 8.0, 7.0, 3.0, 6.0, 4.0, 7.0]
    # print vt.Models[2] * vt.prepareVector([7.0, 2.0, 8.0, 9.0, 8.0, 7.0, 3.0, 6.0, 4.0, 7.0])