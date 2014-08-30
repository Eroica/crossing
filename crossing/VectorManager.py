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

"""VectorManager.py

This module serves two objects: VectorTransformator and TransformationMatrix.
VectorTransformator holds several TransformationMatrix objects that operate
on the language data provided by VectorTransformator.

"""

from sklearn import linear_model
import numpy as np
import sys

class TransformationMatrix(object):
    """A class representing a transformation matrix from vector space A to
    vector space B.
    """


    def __init__(self, T, b, model, alpha):
        """Creates a transformation matrix using the results of
        sklearn.linear_model.
        """

        self.T = T
        self.b = np.transpose(np.matrix(b))
        self.model = model
        self.alpha = alpha

    def __mul__(self, v):
        """Overrides the * operator to allow multiplication with NumPy
        matrices/vectors.
        """

        return self.T * v + self.b

class VectorTransformator(object):
    """A flexible object that can hold several transformation matrices from
    vector space V into vector space W, using the dictionary in self.Dictionary.
    self.V and self.W are dictionaries that contain vectors in the following
    format:

        {"word" = [0.1, 0.2, 0.3, ...]}

    self.Models contains all transformation matrices that can be used to
    transform a given vector by using the overridden ``*`` operator.

    When given a vector ``v``, the default behaviour of ``VectorTransformator``
    is to return a tuple containing the result of ``v`` multiplicated with all
    models from self.Models. If only a single model should be used, the ``[]``
    operator can be used to select that model.
    """

    def __init__(self):
        """A ``VectorTransformator`` object holds several transformation
        matrices If no files are specified when creating a VectorTransformator,
        self.Dictionary, self.V and self.W have to be filled with dictionaries.
        """
        self.Dictionary = {}
        self.Models = []
        self.V = {}
        self.W = {}

    def createTransformationMatrix(self, model="Lasso", alpha=0.1):
        """Creates a transformation matrix using the provided model and alpha
        value. Possible models are:

            *   "Lasso" for linear_model.Lasso,
            *   "ridge" for linear_model.Ridge,
            *   "net" for linear_model.ElasticNet
        """

        # The transformation matrix is calculated using the following vectors:
        # Vectors of V that also appear in language 1 in the word dictionary AND
        # that have a translation, according to the dictionary, found in Vector
        # space W.
        subDict = [s for s in self.Dictionary if s in self.V and self.Dictionary[s] in self.W]

        vectors_de = [self.V[word] for word in subDict]
        vectors_en = [self.W[self.Dictionary[word]] for word in subDict]

        X = np.zeros((len(vectors_de), len(vectors_de[0])))

        for i, v in enumerate(vectors_de):
            X[i]=v
        
        Y = np.zeros((len(vectors_en), len(vectors_en[0])))
        
        for i, v in enumerate(vectors_en):
            Y[i]=v

        W = np.zeros((len(vectors_en[0]), len(vectors_de[0])))
        b = np.zeros((len(vectors_en[0])))

        for j in xrange(len(vectors_en[0])):
            y_j = [x[j] for x in vectors_en]
            
            if model == "ridge":
                clf = linear_model.Ridge(alpha)
            elif model == "net":
                clf = linear_model.ElasticNet(alpha)
            elif mode == "Lasso":
                clf = linear_model.Lasso(alpha)

            clf.fit(X,y_j)
            W[j] = clf.coef_
            b[j] = clf.intercept_

        self.Models.append(TransformationMatrix(W, b, model, alpha))

    def translateAllVectors(self, intoFile=None):
        """Using all vector transformation matrices found in self.Models,
        attemps to translate all vectors from self.V into self.W. If a filename
        is provided, the results will be written into that file.
        """
        
        TransformationResults = {}
        VectorResults = {}
        for model in self.Models:
            for v in self.V:
                VectorResults[v] = model * self.prepareVector(self.V[v])
            TransformationResults[model] = VectorResults
        
        if intoFile:
            with open(intoFile, "w") as fout:
                for model in TransformationResults:
                    print >> fout, "### " + str(model.model) + "_" + str(model.alpha)
                    
                    for v in TransformationResults[model]:
                        print >> fout, v + " " + str(self.V[v])
                        vt = TransformationResults[model][v].flatten()
                        print >> fout, " ---> " + str(vt) + "\n"
                    
                    print >> fout, "\n"

        return TransformationResults

    def translate(self, word, index=0):
        """Takes a word from vector Space V, maps it into W and returns the
        closest vector in W.
        """

        v = self.V[word]
        translatedWord = v * self.Model[index]

        res = []
        for vector in self.W:
            res.append(calculateAngle(word, vector))

        i = res.index(min(res))

        return self.W[i]

    def calculateAngle(self, v, w):
        c = np.dot(v, w)/norm(v)/norm(w)
        angle = arccos(c)
        if np.isnan(angle):
            if (v == w).all():
                return 0.0
            else:
                return np.pi

        return angle

    def prepareVector(self, v):
        """Prepares a vector in the following format:

            [0.1, 0.2, 0.3, ...]

        for use with NumPy multiplication.
        """
        
        return np.transpose(np.matrix(v))

    def __mul__(self, v):
        """Attempts to translate a word from one vector space to another, using
        all models found in self.Models.

        ``word`` can either be

            *   a word found in self.V so that its components from self.V are
                used or
            *   a vector in the format [0.1, 0.2, 0.3, ...]
        """

        if self.Models == []:
            print "You first have to create some models!"
            return

        if type(v) == str:
            if v not in self.V:
                print v + " not found in vector space. Aborting ..."
                return
            
            results = [model * self.prepareVector(self.V[v]) for model in self.Models]
            return tuple(results)

        if type(v) == list:
            results = [model * self.prepareVector(v) for model in self.Models]
            return tuple(results)

    def __getitem__(self, index):
        return self.Models[index]