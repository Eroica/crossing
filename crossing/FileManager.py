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

"""FileManager.py

This module's functions is used by VectorManager to read dictionary and vector
data from files. Those files serve the data that is used later for matrix
transformation of vector space models.

"""

import sys

def readDictionary(dict_file):
    """Reads a dictionary file in the following format:
    language1   language2
    """

    print "Reading dictionary file " + dict_file + " ..."
    df = []

    try:
        df = [line.split() for line in open(dict_file)]
    except IOError:
        print "Dictionary file could not be found!"

    try:
        wordDict = dict(x for x in df if x)
            # in rare cases (depends on Unix/DOS/Mac line endings),
            # an empty line will be included and appended as ``[]''.
            # the ``x for x in d if x'' line removes this empty ``[]''.
    except ValueError:
        print "Something is wrong with the dictionary file!"

    print "Dictionary consisting of " + str(len(wordDict)) + \
          " entries."

    return wordDict

def readVectors(vectors_file):
    """Reads a text file in the following format:
    word a1 a2 a3 a4
    (``word'' being the word and everything after it its components)
    """

    vectorDict = {}
    with open(vectors_file) as fin:
        for i, line in enumerate(fin):
            vector = [x for x in line.split() if x]
            vectorDict[vector[0]] = [float(x) for x in vector[1:]]
    
    return vectorDict

def readWord2Vec(vectors_file):
    """Reads a word2vec vectors file. A word2vec file is special in the
    sense that the first two lines denote the number of vectors and their
    dimension, and thus can be skipped.
    """

    vectorDict = {}
    with open(vectors_file) as fin:
        for i, line in enumerate(fin):
            vector = [x for x in line.split() if x]
            if i > 1:
                vectorDict[vector[0]] = [float(x) for x in vector[1:]]

    return vectorDict