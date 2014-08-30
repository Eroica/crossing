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

import FileManager
import cPickle as pickle
from scrn_out import w, wh, wil, fl, cl
import VectorManager


#------------------------------ Main functions --------------------------------

def main():
	cl()
	wh("\t\tCrOssinG: CompaRing Of AngliciSmS IN German", 75)

	dictionary = readDictionary("../res/dictEntries.txt")
	anglicisms = readTupleFile("../res/anglicisms.txt")
	devectors = pickle.load(open("../res/DE_VEC.bin"))
	envectors = pickle.load(open("../res/EN_VEC.bin"))
	false_friends = readTupleFile("../res/false_friends.txt")

	alphas = [0.0001, 0.0002, 0.001, 0.002, 0.01, 0.02, 0.1, 0.2]
	models = ["ridge", "net", "Lasso"]
	model_paras = [(model, alpha) for model in models for alpha in alphas]
	i = 1
	w("Creating VectorTransformators...\n")

	vm = VectorManager.VectorTransformator()
	vm.Dictionary = dictionary
	vm.V = devectors
	vm.W = envectors

	for tuple_ in model_paras:
		vm.createTransformationMatrix(tuple_[0], tuple_[1])
		w("VectorTransformator Nr. %i with Model=%s and alpha=%g has been"
		  " created\n" %(i, tuple_[0], tuple_[1]))
		i += 1

	w("Creating VectorTransformators...Complete!\n\n")
	models = vm.Models
	top_model = compareMatrices(false_friends, vm, models, devectors, envectors)

	w("\nChecking the quality of an evaluation with false-friend-pairs...\n")
	true_count = 0
	false_count = 0
	n_tests = 100
	for i in range(n_tests):
		wil("False friend test nr. %i" %(i+1))
		res = falseFriendsCheck(false_friends, vm, top_model, devectors,\
								envectors, dictionary, 50, False)
		if res:
			true_count += 1
		elif not res:
			false_count += 1
	w("\nIn %i out of %i times, a random subset had a lower or equal average"\
	 "similarity than a random false friend subset.\n" %(false_count, n_tests))

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

def evalMatrix(false_friends, devectors, envectors, vm, model,
				output=True, n=5):
	""" Evaluates the quality of a matrix """

	average_diff = 0
	similarities = []

	# Calulating the average difference of a false-friend-pair
	for pair in false_friends:
		try:
			if devectors[pair[1]] == []: continue
			elif envectors[pair[0]] == []: continue
			mapped = mapVector(vm, model, devectors[pair[1]])
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


def compareMatrices(false_friends, vm, models, devectors, envectors): 
	""" Compares differend matrices and finds the best one """  

	average_diffs = []

	for model in models:
		diff = evalMatrix(false_friends, devectors, envectors, vm, model,\
			output=False)
		average_diffs.append(diff)

	top_average_diff = 200
	for diff in average_diffs:
		if diff <= top_average_diff: top_average_diff = diff

	i = average_diffs.index(top_average_diff)+1
	w("Matrix nr. %i is best by average similarity with %.2f%%\n"
	  %(i, top_average_diff))
	w("Parameters: Model=%s, alpha=%g\n\n" 
		%(models[i-1].model, models[i-1].alpha))

	return models[i-1]

def falseFriendsCheck(false_friends, vectorManager, model, devectors, envectors,
	dictionary, sample_size, output=True):

	ff_sim = 0
	r_sim = 0

	false_friends = randomSubset(false_friends, sample_size, output)
	random_set = randomSubset(dictionary, sample_size, output)

	if output:
		w("\nChecking the quality of an evaluation with "\
			"false-friend-pairs...\n")

	# Calculates average similarity for random false friend subset
	ff_count = 0
	for pair in false_friends:
		try:
			vector_english = envectors[pair[0]]
			vector_german = devectors[pair[1]]
		except:
			continue
		mapped = mapVector(vectorManager, model, vector_english)
		mapped = [x.item((0, 0)) for x in mapped]
		ff_sim += dotproduct(mapped, vector_german)
		ff_count += 1

	ff_sim /= ff_count

	# Calculates similarity for random dictionary entry subset
	r_count = 0
	for pair in random_set:
		if random_set.index(pair) > ff_count:
			break # so both subsets have the same size and are comparable
		try:
			vector_english = envectors[pair[1]]
			vector_german = devectors[pair[0]]
		except:
			continue
		mapped = mapVector(vectorManager, model, vector_english)
		mapped = [x.item((0, 0)) for x in mapped]
		r_sim += dotproduct(mapped, vector_german)
		r_count += 1

	r_sim /= r_count 

	if ff_sim < r_sim: 
		return True
	else:
		return False

#---------------------------- Helping functions -------------------------------

def randomSubset(array, n, output=True):
	if output:
		w("Creating random subset...")
	if isinstance(array, dict): 
		# conversion to array of tuples
		keys = array.keys()
		values = array.values()
		length = len(array)
		array = [(keys[i], values[i]) for i in xrange(length)]
	res = []
	while len(res) != n:
		if output:
			percentage = len(res)*1.0/n*100
			wil("Creating random subset - %.2f%% complete" %(percentage))
		ri = random.randint(0, len(array)-1)
		res.append(array[ri])
		if output:
			fl()
	if output:		
		wil("Creating random subset...Complete!", 50, "\n")
	return res


def lookUp(key, dictionary):
	""" Looks up a key in a dicitonary, returns translation """
	try:
		return dictionary[key]
	except:
		return None

def mapVector(vm, model, v):
	""" Maps a vector """
	return model.T * vm.prepareVector(v) + model.b

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
	""" An alternative implementation of cosine similarity """
	return dotproduct(v1, v2)/length(v1)/length(v2)

def dotproduct(v1, v2):
	""" Returns the dotproduct of two vectors """
 	return sum((a*b) for a, b in zip(v1, v2))

def length(v):
	""" Returns the length of a vector """
 	return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
	""" Returns the angle between two vectors """
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