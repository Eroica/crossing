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

def readDictionaryFile(dict_file):
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

def readVectorsFile(vectors_file):
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

def readWord2VecFile(vectors_file):
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

#------------------------------------------------------------------------------

def readDictionary(dict_file):
    """ Reads a file into a dictionary """
    d = [line.split() for line in codecs.open(dict_file, "r", "utf-8")]
    return dict(x for x in d if x)

def readVectorFile(word_list, vectors_file, filter=True):
    """ Reads a vectorfile """
    w("Reading VectorFile %s..." %(vectors_file))
    D = {}
    fl()
    with codecs.open(vectors_file, "r", "utf-8") as fin:
        for i, line in enumerate(fin):
            wil("Reading VectorFile %s - %i lines so far%s" 
                %(vectors_file, i+1), 20)
            vector = [x for x in line.split() if x]
            # die ersten zwei zeilen einer word2vec vector-datei kann man ignorieren.
            # sie sind nur ein paar informationen zur anzahl der vektoren und
            # der vektor </s> (anzahl der zeilen im korpus)
            if i > 1:
                # hier werden diejenigen vektoren rausgefiltert, die nicht
                # im wörterbuch sind
                if filter:
                    if vector[0] in word_list: 
                        D[vector[0]] = [float(x) for x in vector[1:]]
                        del word_list[word_list.index(vector[0])]
                elif not filter:
                    D[vector[0]] = [float(x) for x in vector[1:]]
            fl()

    wil("Reading VectorFile %s...Complete!%s\n" %(vectors_file), 30)
    return D

def readFile(filename, ignore_character="##########", onestring=False):
    """ Reads a file """  
    # ignore_character for leaving out redundant lines
    wil("Reading file %s" %(filename))

    file = codecs.open(filename, "r", "utf-8")
    lines = []
    line = file.readline()
    count = 0
    fl()

    while line != "":
        wil("Reading File %s - %i lines so far" %(filename, count), 20)
        if not line.startswith(ignore_character):
            lines.append(line)
    line = file.readline()
    count += 1
    fl()
    wil("Reading file %s...Complete!" %(filename), 30, "\n")
    if onestring:
        # If result should be one string instead an array of strings
        onestring = ""
        for i in xrange(len(lines)):
            onestring += lines[i] + " "
        return onestring
    return lines

def readTupleFile(input_file, separation_character="\t"):
    """ Reads a tuple file """  # tuples are separated by separation_character
    lines = readFile(input_file)
    tuples = []
    for line in lines:
        percentage = lines.index(line)*1.0/len(lines)*100.0
        wil("Reading tuple file %s - %.2f%% complete"
            %(input_file, percentage), 30)
        line = line.replace("\n", "")
        parts = line.split(separation_character)
        tuples.append(tuple(parts))
        fl()
    wil("Reading tuple file %s...Complete!" %(input_file), 30, "\n")
    return tuples

def readTupleFileToDict(input_file, dicttype, separation_character="\t"):
    """ Reads a tuple file into a dictionary""" 
    # Tuples are separated by separation_character
    lines = readFile(input_file)
    dict_ = {}
    dict_ = defaultdict()
    LENGTH = len(lines)
    for i in xrange(LENGTH):
        percentage = (i*1.0/LENGTH*100.0)
        wil("Reading tuple file %s and creating dictionary -%.2f%% complete%s" 
            %(input_file, percentage), 30)
        line = lines[i].replace("\n", "")
        parts = line.split(separation_character)
        if isinstance(dicttype, int): 
            dict_.setdefault(parts[0], int(parts[1]))
        elif isinstance(dicttype, basestring): 
            dict_.setdefault(unicode(parts[0]), unicode(parts[1]))
        fl()
    wil("Reading tuple file %s and creating dictionary...Complete!%s\n" 
        %(input_file), 30)
    return dict_

def readVectorFileToDict(filename):
    """ Reads a vector file into a dictionary with word as key """
    print "This file %s" %(filename)
    dict_ = defaultdict(list)
    with codecs.open(filename, "r", "utf-8") as f:
        content = f.readlines()
        length = len(content)
        for i in xrange(length):
            y = content[i].split()
            dict_[y[0]] = [float(dimension) for dimension in y[1:]]
    return dict_

def loadDictionary(self, dict_file):
    """ Loads a dictionary from ``dict_file''. """
    try:
        self.dictEntries = dict([line.split() for line in open(dict_file)])
    except IOError:
        print >> sys.stderr, \
                 "Cannot find dictionary file " + dict_file + "!"
    finally:
        print "#" + str(len(self.dictEntries)) + " entries in dictionary."

def loadObject(self, name):
    """ Loads a cPickle object """
    try:
        return cPickle.load(open(name))
    except IOError:
        print >> sys.stderr, name + " file could not be found!"
        return None


def extractPlaintext(self, input_file, unigroups, conc_file=None):
        """
        Extracts plaintext data from ``input_file'' with characters only found
        in the unicode groups specified by ``unigroups''.
        If ``conf_file'' is specified, the script will concatenate those words
        with an `_' while parsing.
        All characters will be converted to lower case.
        """
        def filterCharacters(UNIPRINT):
            """
            A small helper function that deletes those characters not found
            in the unicode groups defined by ``UNIPRINT''.
            """
            result = []
            for char in line:
                char = unicodedata.category(char) in UNIPRINT and char or u'#'
                result.append(char)
            return u"".join(result).replace(u'#', u' ')

        if len(unigroups) % 2 == 1:
            print >> sys.stderr, "Unicode groups string malformed!"
            print >> sys.stderr, "Expected: {Ll|Nd|...}"
            print >> sys.stderr, "Got: " + unigroups
            return None

        if conc_file is not None:
            concWords = [line.strip() for line in open(concatenated, "r")]

        UNIPRINT = tuple(re.findall("..", args.unigroups))
        output_file = "plain_" + input_file

        with open(input_file, "r") as inf:
            with open(output_file, "w") as outf:
                for line in inf:
                    line = filterCharacters(line.decode("utf-8").lower(),
                                            UNIPRINT)
                    line = re.sub(" +", " ", line)

                    if conc_file is not None:
                        if any(word in line for word in concWords):
                            for word in concatenatedWords:
                                line = line.replace(word,
                                                    word.replace(" ", "_"))

                    print >> outf, line.encode("utf-8")


#-------------------------------- Writing -------------------------------------

def writeFile(filename, content):
    """ Simple file writing """
    file = codecs.open(filename, "w", "utf-8")
    for i in xrange(len(content)):
        file.write(content[i])
    file.close()

def writeTupleFile(tuples, output_file, separation_character="\t", 
                   printErrors=True):
    """ Enhanced function for writing a tuple file """
    file = codecs.open(output_file, "w", "utf-8")
    for i in xrange(len(tuples)):
        percentage = i*1.0/len(tuples)*100
        wil("Writing file %s - %.2f%% complete" 
            %(output_file, percentage), 50)
        try:
            file.write(unicode(tuples[i][0]) + separation_character +
                       unicode(tuples[i][1]) + "\n")
        except Exception, ex:
            if printErrors:
                w("%s: %s" %(str(ex), str(tuples[i])))
            continue
        finally:
            fl()
    wil("Writing file %s...Complete!" %(output_file), 50, "\n")
    file.close()

def dumpObject(self, object_, name = None):
        """
        Takes an object as an argument and dumps its content on disk using
        ``name'' as its file name. If no file name is specified, repr(object_)
        will instead be used.
        """
        try:
            with open(name, "wb") as output_file:
                pickle.dump(object_, output_file, -1)
            print "Successfully dumped " + object_ + " into " + name + "."
        except IOError:
            with open(repr(object_), "wb") as output_file:
                pickle.dump(object_, output_file, -1)
            print "Successfully dumped " + object_ + \
                  " into " + repr(object_) + "."


