#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ++++++++++++++++++++++++++++++++++++++++++++++
# Authors:
#
# Sebastian Spaar <spaar@stud.uni-heidelberg.de>
# Dennis Ulmer <d.ulmer@stud.uni-heidelberg.de>
#
# Project:
# CrOssinG (CompaRing Of AngliciSmS IN German)
#
# ++++++++++++++++++++++++++++++++++++++++++++++

""" eval.py:

	This module is the final step of CrOssinG, evaluating the results.
	"""

#-------------------------------- Imports -------------------------------------

import operator
from collections import defaultdict
import sys
import time
import math
import random

import numpy as np
from file_handling import readTupleFileToDict, readTupleFile, \
	readVectorFileToDict, readDictionary, readVectorFile
import cPickle as pickle
from scrn_out import w, wh, wil, fl, cl


### import anpassen:
# from vt import VectorTransformator
import VectorManager


#------------------------------ Main functions --------------------------------

def main():
	cl()
	wh("\t\tCrOssinG: CompaRing Of AngliciSmS IN German", 75)

	### nicht vergessen die pfade zu ändern
	dictionary = readDictionary("../res/dictEntries.txt")
	anglicisms = readTupleFile("../res/anglicisms.txt")
	devectors = pickle.load(open("../res/DE_VEC.bin"))
	envectors = pickle.load(open("../res/EN_VEC.bin"))
	# devectors = readVectorFileToDict("../res/out/de_small2.txt")
	# envectors = readVectorFileToDict("../res/out/en_small2.txt")
	false_friends = readTupleFile("../res/false_friends.txt")

	# alphas = [0.0001, 0.0002, 0.001, 0.002, 0.01, 0.02, 0.1, 0.2]
	# models = ["ridge", "net", "Lasso"]
	# model_paras = [(model, alpha) for model in models for alpha in alphas]
	model_paras = [("net", 0.1), ("Lasso", 0.2)]
	models = []
	i = 1
	w("Creating VectorTransformators...\n")

	### zuallererst ein VectorTransformator-Objekt, das mehrere Modelle halten kann
	vt = VectorManager.VectorTransformator("../res/dictEntries.txt", "../res/DE_VEC.bin", "../res/EN_VEC.bin")
	### da die nötigen vektoren schon oben erzeugt wurden, werden keine dateien übergeben
	### stattdessen müssen die vektoren separat in das objekt gespeichert werden.
	### änder den namen von dem deutsch-englisch wörterbuch (dictionary) am besten
	### in etwas anderes um, sonst ist es zu ähnlich an dem python-objekt "dict"

	for tuple_ in model_paras:
		### transformations-matrix mit der methode createTransformationMatrix() erstellen
		### die sieht so aus:
		### def createTransformationMatrix(self, model="Lasso", alpha=0.1):
		### also zuerst den namen des modells übergeben, dann den alphawert
		### wörterbuch und vektoren müssen nicht übergeben werden, da sie im
		### vt objekt enthalten sind.
		### printErrors geht natürlich leider auch nicht mehr
		vt.createTransformationMatrix(tuple_[0], tuple_[1])
		
		### wenn du auf die transformationsmatrizen zugreifen willst, mach das am besten so:
		### vt[0].T
		### über [0..] wird das 1., .. model von vt angesprochen. das modell selbst
		### enthält die variable "T", die die matrix enthält
		### vergiss nicht dass zu jedem modell nicht nur eine matrix gehört,
		### sondern auch ein absolutes glied ...
		### die folgende zeile könnte daher entfallen:
		matrix = vt.M
		
		w("VectorTransformator Nr. %i with Model=%s and alpha=%g has been"
		  " created\n" %(i, tuple_[0], tuple_[1]))
		
		### hier genauso: wenn du auf die einzelnen modelle zugreifen willst,
		### benutz einfach vt[x].
		### jedes dieser modelle hat auch die informationen zu modell und alpha gespeichert
		### sagen wir vt[1] ist ein modell. dann hat es folgende variablen:
		### vt[1].T :: matrix
		### vt[1].b :: absolutes glied
		### vt[1].model :: name des models (string)
		### vt[1].alpha :: alpha-wert (float)
		### grundsätzlich kannst du es aber auch so lassen
		### später benutzt du ja die "models" variable weiter, also falls es zu kompliziert wird,
		### lass es einfach so wie jetzt
		### nur musst du bedenken, dass ich die erstellung von   vt   außerhalb
		### der for-schleife gesetzt habe. es gibt also nur EIN vt objekt
		### dieses vt objekt enthält, in der variablen vt.models, mehrere transformationsmatrizen
		### wenn du diese transformationsmatrizen vergleichen willst, solltest du also
		### vt.models an funktionen übergeben oder
		### vt an sich und die funktionen greifen dann auf vt.models zu
		models.append((tuple_[0], tuple_[1], vt, matrix))

		i += 1


	w("Creating VectorTransformators...Complete!\n\n")


	### wie oben schon erwähnt: die "models" variable hier kann im prinzip ersetzt werden,
	### indem einfach das    vt   objekt übergeben wird.
	### vt hat ja auch die deutschen und englischen vektoren in vt.V und vt.W
	top_model = compareMatrices(false_friends, models, devectors, envectors)
	
	falseFriendsCheck(false_friends, top_model[2] , devectors, envectors, dictionary, 50)


def finalOutput(similarities, anglicisms, n):
	""" Generates the "final output" of crossing, printing the most and least
	similar anglicism-pairs """

	for key in similarities.keys():
		if key not in anglicisms:
			del similarities[key]

	if len(similarities) < n: n = len(similarities) # Just to be sure
	
	w("\nFinal results\n%s\n\n" %(40*"-"))
	
	w("Top %i pairs with highest similarity:\n" %(n))
	top_n = findTopN(similarities, n, 1)

	for pair in top_n:
		w("%i. %s - %s | %.2f%% similarity\n"\
		  %(top_n.index(pair)+1, pair[0][0], pair[0][1], pair[1]*50+50))

	w("\nTop %i pairs with lowest similarity:\n" %(n))
	bottom_n = findTopN(similarities, n, -1)
	for pair in bottom_n:
			w("%i. %s - %s | %.2f%% similarity\n"\
			  %(bottom_n.index(pair)+1, pair[0][0], pair[0][1], pair[1]*50+50))

def evalMatrix(false_friends, devectors, envectors, VectorTransformator,
				output=True, n=5):
	""" Evaluates the quality of a matrix """

	average_diff = 0
	similarities = []

	# Calulating the average difference of a false-friend-pair
	for pair in false_friends:
		try:
			if devectors[pair[1]] == []: continue
			elif envectors[pair[0]] == []: continue
			mapped = mapVector(VectorTransformator, devectors[pair[1]])
			mapped = [x.item((0, 0)) for x in mapped]
			sim = cosine_similarity(mapped, envectors[pair[0]])
			similarities.append((sim, pair))
			average_diff += sim
		except KeyError:
			continue

	average_diff /= len(similarities)

	# Output

	if output:
		print "Average similarity was %.2f%% for %i elements"\
			  %(average_diff*50+50, len(similarities))
		sorted_ = sorted(similarities)

		print "Highest differences:\n"
		for similarity in sorted_[:n]:
			w("%.2f%% similarity with %s - %s\n"\
			  %(similarity[0]*50+50, similarity[1][0], similarity[1][1]))
		print "\nLowest differences:\n"
		sorted_.reverse()
		for similarity in sorted_[:n]:
			w("%.2f%% similarity with %s - %s\n"\
			  %(similarity[0]*50+50, similarity[1][0], similarity[1][1]))
		print "\n"
		
	return average_diff*50+50


def compareMatrices(false_friends, models, devectors, envectors): 
	""" Compares differend matrices and finds the best one """  

	average_diffs = []

	for model in models:
		diff = evalMatrix(false_friends, devectors, envectors, model[2],\
			output=True)
		average_diffs.append(diff)

	top_average_diff = 200

	for diff in average_diffs:
		if diff <= top_average_diff: top_average_diff = diff

	i = average_diffs.index(top_average_diff)+1
	w("Matrix nr. %i is best by average similarity with %.2f%%\n"
	  %(i+1, top_average_diff))
	w("Parameters: Model=%s, alpha=%g\n\n" %(models[i-1][0], models[i-1][1]))

	return models[i-1]

def findSubstitutions(anglicism, dictionary, devectors, envectors, n=5,
	printErrors=True):
	""" Finds alternative words for an anglicism """

	wil("Looking for words-substitutions for %s" %(anglicism))
	translation = dictionary[anglicism]
	anglicism_vector = devectors[anglicism]
	translation_vector = envectors[translation]

	length = len(devectors)
	keys = devectors.keys()
	proposals = []
	errors = []

	fl()
	for i in xrange(length):
		wil("Looking for words-substitutions for %s - %.2f%% complete%s" 
			%(anglicism, i*1.0/length*100), 30)
		try:
			current_word = keys[i]
			de_diff = vectorDistance(anglicism_vector, devectors[i])
			en_diff = 0
			# current_word_translation = lookUp(current_word, dictionary)
			# en_diff = vectorDistance(translation_vector, 
			# 	envectors[current_word_translation])
			# if de_diff + en_diff != 0:
			# 	# "Squared loss"
			proposals.append(((de_diff + en_diff)**2, current_word))
		except Exception, e:
			errors.append(unicode(e))
			continue
		finally:
			fl()

	wil("Looking for words-substitutions for %s...Complete!%s\n" 
		%(anglicism), 40)

	# Sort ascending by difference
	proposals = sorted(proposals, key =lambda e: e[0])


	w("\nProposals for %s:\n" %(anglicism))
	i = 1
	for proposal in proposals[:n]:
		w("%i. %s with a difference of %g\n" %(i, proposal[1], proposal[0]))
		i += 1

	if printErrors:
		w("\nErrosr:\n")
		for error in errors:
			print error

def falseFriendsCheck(false_friends, vectorTransformator, devectors, envectors,
	dictionary, sample_size):

	ff_sim = 0
	r_sim = 0

	false_friends = randomSubset(false_friends, sample_size)
	random_set = randomSubset(dictionary, sample_size)

	w("\nChecking the quality of an evaluation with false-friend-pairs\n")

	ff_count = 0
	for pair in false_friends:
		try:
			vector_english = envectors[pair[0]]
			vector_german = devectors[pair[1]]
		except:
			print "LookUp Fail"
			continue
		mapped = mapVector(VectorTransformator, vector_english)
		mapped = [x.item((0, 0)) for x in mapped]
		ff_sim += dotproduct(mapped, vector_german)
		ff_count += 1

	ff_sim /= ff_count
	print ff_sim






#---------------------------- Helping functions -------------------------------

def randomSubset(array, n):
	w("Creating random subset...")
	if isinstance(array, dict): 
		keys = array.keys()
		values = array.values()
		length = len(array)
		array = [(keys[i], values[i]) for i in xrange(length)]
	res = []
	while len(res) != n:
		percentage = len(res)*1.0/n*100
		wil("Creating random subset - %.2f%% complete" %(percentage))
		ri = random.randint(0, len(array)-1)
		res.append(array[ri])
		fl()
	wil("Creating random subset...Complete!", 50, "\n")
	return res


def lookUp(key, dictionary):
	""" Looks up a key in a dicitonary, returns translation """
	try:
		return dictionary[key]
	except:
		return None

def mapVector(vt, v):
	return vt.M * vt.prepareVector(v) + vt.b

def findTopN(similarities, n, top=1):
	""" Finds top n elements of an array """

	if isinstance(similarities, dict): 
		 similarities = [(similarities.keys()[i], similarities.values()[i])\
		 for i in range(len(similarities))]
	if top == 1:
		 return sorted(similarities, key=lambda e: e[1],
		 reverse=True)[:n]
	elif top == -1:
		 return sorted(similarities, key=lambda e: e[1], 
		 reverse=False)[:n]
	else:
		return None

def cosine_similarity(v1, v2):
	""" Return the cosine similarity of two vectors """
	res = np.dot(v1,v2)/np.linalg.norm(v1)/np.linalg.norm(v2)
	return res

def cosine_similarity2(v1, v2):
	return dotproduct(v1, v2)/length(v1)/length(v2)

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def vectorDistance(v1, v2):
	""" Returns the euklidian distance of two vectors """
	return np.linalg.norm([i-j for i in v1 for j in v2])

def calculateSimilarities(devectors, envectors, dictionary, matrix, 
						VectorTransformator, printErrors=True):
	""" Calculates the similarities of word-pairs """
	similarities = defaultdict(float)
	length = len(devectors.keys())
	keys_de = devectors.keys()
	keys_en = envectors.keys()
	errors = []
	
	for i in range(length):
		deword = keys_de[i]
		enword = lookUp(deword, dictionary)
		if deword != None and enword != None:
			try:
				devector = devectors[deword]
				envector = envectors[enword]
				mapped = mapVector(VectorTransformator, devector)
				mapped = [x.item((0, 0)) for x in mapped]
				similarity = cosine_similarity(mapped, envector)
				similarities.setdefault((deword, enword), similarity)
			except KeyError, e:
				errors.append("No corresponding vector found %s: %s | %s" 
							  %(str(e), deword, enword))
				continue
			except ValueError, e:
				errors.append("Matrices not aligned %s: %s | %s" 
							  %(str(e), deword, enword))
				continue
			except:
				continue
		else:
			errors.append("No translation found: %s" %(deword))
			continue
			   
	if printErrors: 
		print "\nErrors:\n%s\n" %(40*"-")
		for e in errors:
			print e

	return similarities


#---------------------------------- Main --------------------------------------

if __name__ == "__main__":
	main()