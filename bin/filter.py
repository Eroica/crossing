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

"""filter.py:

    This module is used to filter out unwanted data in dict.cc-entries, 
    false-friend-pairs or anglicisms.
    """

#------------------------------------ Imports ---------------------------------

import re
import random

from file_handling import readTupleFileToDict
from scrn_out import w, wil, fl 

#---------------------------------- Main functions ----------------------------

def filterTuples(tuples, task, freq_threshold=0, printOuts=False, 
                filterCode="eebflpswmw"):
    """Filters out redundant tuples and multiple word expressions if needed and
    formats the remaining ones.
    """
    # Filtercode explanation:
    # The filtercode is a string that determines which filters are applied to 
    # the Dataset in mode DE
    #
    # The following parts can be added to the filterCode:
    #
    # ee: Empty entries are going to be filtered out
    # bf: Entries with "bad formatting" (= things that are hard to be processed
    #     because of inconsisteny, like hyphons, paranthesis etc.) 
    #     are going to by filtered out
    # mw: Multiword expressions are going to be filtered out.
    #     Multiword expression seem to make up at least (!) 70 % of the whole 
    #     dict.cc dataset, so be careful.
    # lp: If a entry has more than one translation, you can filter out the n 
    #     top translation with writing e.g. 3lp for the top 3 results. 
    #     Default is one using the top result.
    # sw: German and english stopwords are going to be filtered out
    # fr: Words with frequency lower than the freq_treshold argument in the 
    #     English and German Wikipedia-Corpus are going to be filtered out
    # ke: KeyError-throwing entries are going to be filtered out (a thrown 
    #     KeyError means that no entry for the corresponding word exists in 
    #     the frequency-dictionary)
    # sl: Allows processing of entries with a slash [NOT RECOMMENDED: 
    #     Processing those entries is messy and prone to errors as use of slash
    #     is very inconsistend]
    
    # Initialization of arrays and dictionaries
    tuples_new = []
    stopwords = []
    outs = []
    freqs_de = {}
    freqs_en = {}
    
    # tasks: FF = False Friends, AN = Anglicisms, DE = Dictionary Entries
    if task not in ["FF", "AN", "DE"]: 
        return
    
    LENGTH = len(tuples)  # because optimization, that's why
    PERCENTAGE = 100*1.0
    
    # Initialization of top_n_arg-argument for DE
    top_n_arg = 1
    if "lp" in filterCode:
        try:
            top_n_arg = int(filterCode[filterCode.index("lp") - 1])
        except:
            top_n_arg = 1
    TOP_N = top_n_arg - 1
    
    # Initialization of counters for DE
    emptyEntryCounter = 0
    badFormattingCounter = 0
    keyErrorCount = 0
    leftOutCount = 0
    multiWordCount = 0
    stopWordCounter = 0
    lowPriorityCounter = 0
    
    if task == "DE":
        # Initialization of stopwords - I was just too lazy to read them out of
        # a .txt-File, so whatever
        stopwords_en = ["a", "about", "above", "after", "again", "against", 
                        "all", "am", "an", "and", "any", "are", "aren", "as",
                        "at", "be", "because", "been", "before", "being", 
                        "below", "between", "both", "but", "by", "can", 
                        "cannot", "could", "couldn", "did", "didn", "do", 
                        "does", "doesn", "doing", "don", "down", "during", 
                        "each", "few", "for", "from", "further", "had", 
                        "hadn", "has", "hasn", "have", "haven", "having", 
                        "he", "her", "hers", "here", "hers", "herself", "him",
                        "himself", "his", "how", "i", "its", "if", "in", 
                        "into", "is", "it", "its", "itself", "me", "more", 
                        "most", "my", "myself", "no", "nor", "not", "of", 
                        "off", "on", "once", "only", "or", "other", "ought", 
                        "our", "ours", "ourselves", "out", "over", "own", 
                        "same", "she", "so", "some", "such", "than", "that", 
                        "the", "their", "theirs", "them", "themselves", 
                        "then", "there", "these", "they", "this", "those", 
                        "through", "to", "too", "under", "until", "up", 
                        "very", "was", "we", "were", "what", "when", "where", 
                        "which", "while", "who", "whom", "why", "with", "you",
                        "your", "yours", "yourself", "yourselves"]
        stopwords_de = [u'aber', u'als', u'am', u'an', u'auch', u'auf', u'aus',
                        u'bei', u'bin', u'bis', u'bist', u'da', u'dadurch', 
                        u'daher', u'darum', u'das', u'daß', u'dass', u'dein',
                        u'deine', u'dem', u'den', u'der', u'des', u'dessen', 
                        u'deshalb', u'die', u'dies', u'dieser', u'dieses', 
                        u'doch', u'dort', u'du', u'durch', u'ein', u'eine', 
                        u'einem', u'einen', u'einer', u'eines', u'er', u'es', 
                        u'euer', u'eure', u'für', u'hatte', u'hatten', 
                        u'hattest', u'hattet', u'hier', u'hinter', u'ich', 
                        u'ihr', u'ihre', u'im', u'in', u'ist', u'ja', u'jede',
                        u'jedem', u'jeden', u'jeder', u'jedes', u'jener', 
                        u'jenes', u'jetzt', u'kann', u'kannst', u'können', 
                        u'könnt', u'machen', u'mein', u'meine', u'mit', 
                        u'muß', u'mußt', u'musst', u'müssen', u'müßt', 
                        u'nach', u'nachdem', u'nein', u'nicht', u'nun', 
                        u'oder', u'seid', u'sein', u'seine', u'sich', u'sie',
                        u'sind', u'soll', u'sollen', u'sollst', u'sollt', 
                        u'sonst', u'soweit', u'sowie', u'und', u'unser', 
                        u'unsere', u'unter', u'vom', u'von', u'vor', u'wann', 
                        u'warum', u'was', u'weiter', u'weitere', u'wenn', 
                        u'wer', u'werde', u'werden', u'werdet', u'weshalb', 
                        u'wie', u'wieder', u'wieso', u'wir', u'wird', 
                        u'wirst', u'wo', u'woher', u'wohin', u'zu', u'zum', 
                        u'zur', u'über']
        if "fr" in filterCode:
            w("Gathering word frequencies...")
            freqs_en = readTupleFileToDict("../res/freqs_en.txt", 0)
            freqs_de = readTupleFileToDict("../res/freqs_de.txt", 0)
            w("Gathering word frequencies...Complete!")
    
    for i in xrange(LENGTH): 
        percentage = i*1.0/LENGTH*PERCENTAGE
        wil("Filtering tuples in mode %s - %.2f%% complete" 
            %(task, percentage), 50)
        
        if task == "FF":
            # Removing all kinds of parenthesis and checking if there are 
            # multiple words on one or both sides
            english_friend = re.sub("(\(.+\)|\[.+\])", "", tuples[i][0])
            english_friend_parts = [part for part in 
                                    re.split("(, | \/ |\/|; )", english_friend)
                                    if part not in ", / /; "]
            
            german_friend = re.sub("(\(.+\)|\[.+\])", "", tuples[i][2])
            german_friend_parts = [part for part in 
                                   re.split("(, | \/ |\/|; )", german_friend) 
                                   if part not in ", / /; "]
            
            # Generating tuples for every possible combination
            for j in xrange(len(english_friend_parts)):
                for k in xrange(len(german_friend_parts)):
                    # Replacing redundant characters, converting to lowercase,
                    # connecting multi-word-expressions with underscores
                    english_friend_parts[j] = trim(english_friend_parts[j].
                                                replace("to ", "").
                                                replace(u"…", "").
                                                replace("!", "").
                                                replace("-", "").
                                                replace(".", "").
                                                replace("\n", "").lower())
                    if len(english_friend_parts[j].split(" ")) > 1: 
                        english_friend_parts[j] = "_".join(trimArray(
                                                    english_friend_parts[j].
                                                    split(" ")))
                    german_friend_parts[k] = trim(german_friend_parts[k].
                                                replace("to ", "").
                                                replace(u"…", "").
                                                replace("!", "").
                                                replace("-", "").
                                                replace(".", "").
                                                replace("\n", "").lower())
                    if len(german_friend_parts[k].split(" ")) > 1: 
                        german_friend_parts[k] = "_".join(trimArray(
                                                    german_friend_parts[k].
                                                    split(" ")))
                    tuples_new.append((english_friend_parts[j], 
                                       german_friend_parts[k]))
        
        elif task == "AN":
            translations = tuples[i][1]
            anglicism = tuples[i][0].lower()
            # Connecting multi-word-expressions with underscores
            if len(anglicism.split(" ")) > 1: 
                anglicism = "_".join(anglicism.split(" "))
            for t in translations:
                t = t.lower()
                if len(t.split(" ")) > 1: t = "_".join(anglicism.split(" "))
                tuples_new.append((anglicism, t))
        
        elif task == "DE":
            english_entry = trim(unicode(tuples[i][0][0]).lower()).\
                            replace("to ", "").replace("be ", "")
            german_entry = trim(unicode(tuples[i][1][0]).lower())
            
            if (german_entry == "" or english_entry == "") and \
                "ee" in filterCode:
                # Empty entry filter
                outs.append("%s | %s | Empty entry" 
                            %(english_entry, german_entry))
                emptyEntryCounter += 1
                continue
            if (badFormatting(german_entry, '-.,()/_:"\'') or \
                badFormatting(english_entry, '-.,()/_:"\'')) and \
                "bf" in filterCode:
                # Undesired special character filter
                outs.append("%s | %s | bad formatting" 
                            %(english_entry, german_entry))
                badFormattingCounter += 1
                continue
            if (len(trimArray(german_entry.split(" "))) > 1 or \
               len(trimArray(english_entry.split(" "))) > 1) and \
               "mw" in filterCode:
                # Multiword expression filter
                outs.append("%s | %s | Multi-word expression" 
                            %(english_entry, german_entry))
                multiWordCount += 1
                continue
            if (" / " in english_entry or " / " in german_entry or \
               " " in english_entry or " " in german_entry) and \
               "sl" in filterCode:
                # For expressions with slashes
                english_entry_parts = re.split(" / ", english_entry)
                german_entry_parts = re.split(" / ", german_entry)
                for j in xrange(len(english_entry_parts)):
                    for k in xrange(len(german_entry_parts)):
                        try:
                            if len(tuples_new) > 0+TOP_N and \
                               english_entry_parts[j] in \
                               tuples_new[len(tuples_new)-(1+TOP_N)] and \
                                "lp" in filterCode:
                                # Filters out every entry besided the first 
                                # n ones
                                lowPriorityCounter += 1
                                outs.append("%s | %s | Low Priority" 
                                            %(english_entry, german_entry))
                                continue
                            if (arraysIntersect([trim(word) for word in  \
                               english_entry_parts[j].split(" ")], 
                               stopwords_en) or \
                               arraysIntersect([trim(word) for word in \
                               german_entry_parts[j].split(" ")], 
                               stopwords_de)) and \
                               "sw" in filterCode:
                                # Stopword filter
                                stopWordCounter += 1
                                outs.append("%s | %s | Stopword" 
                                            %(english_entry, german_entry))
                                continue
                            if sum([freqs_en[word] for word in \
                               english_entry_parts[j]]) > freq_threshold and \
                               sum([freqs_de[word] for word in \
                               german_entry_parts[k]]) > freq_threshold \
                               and "fr" in filterCode:
                                # Stopword filter
                                tuples_new.append((english_entry_parts[j],
                                                    german_entry_parts[k]))
                            elif "fr" in filterCode:
                                leftOutCount += 1
                                outs.append("%s | %s | Not frequent enough" 
                                            %(english_entry, german_entry))
                            else:
                                # if not filtered by frequencies
                                tuples_new.append((english_entry_parts[j],
                                                   german_entry_parts[k]))
                        except KeyError, e:
                            if "ke" in filterCode:
                                # Key Error filter
                                keyErrorCount += 1
                                outs.append("%s | %s | KeyError" 
                                            %(english_entry, german_entry))
                            else:
                                tuples_new.append((english_entry_parts[j],
                                                   german_entry_parts[k]))
            else:
                # Default (if not expression with slashes)
                try:
                    if len(tuples_new) > 0+TOP_N and english_entry in \
                       tuples_new[len(tuples_new)-(1+TOP_N)] and \
                       "lp" in filterCode:
                        # Filters out every entry besided the first n ones
                        lowPriorityCounter += 1
                        outs.append("%s | %s | Low Priority" 
                                    %(english_entry, german_entry))
                        continue
                    if english_entry in stopwords_en or \
                       german_entry in stopwords_de and "sw" in filterCode:
                        # Stopword filter
                        stopWordCounter += 1
                        outs.append("%s | %s | Stopword" 
                                    %(english_entry, german_entry))
                        continue
                    if freqs_en[english_entry] > freq_threshold and \
                       freqs_de[german_entry] > freq_threshold and \
                        "fr" in filterCode:
                        # Stopword filter
                        tuples_new.append((english_entry, german_entry))
                    elif "fr" in filterCode:
                        # if not filtered by frequencies
                        leftOutCount += 1
                        outs.append("%s | %s | Not frequent enough" 
                                    %(english_entry, german_entry))
                    else:
                        # Key Error filter
                        tuples_new.append((english_entry, german_entry))
                except KeyError, e:
                    if "ke" in filterCode:
                        # Key Error filter
                        keyErrorCount += 1
                        outs.append("%s | %s | KeyError" 
                                    %(english_entry, german_entry))
                    else:
                        tuples_new.append((english_entry, german_entry))
        fl()
    wil("Filtering tuples in mode %s...Complete!" %(task), 50, "\n")
    
    if printOuts:
        # Prints filtered-out entries - might be really long, obviously
        w("Outs:")
        for out in outs:
            print out
    
    if task == "DE":
        len_old = len(tuples)
        print "\nFilter Report:\n%s" %(75*"-")
        print "Outs: %i (%.2f%%)" %(len_old-len(tuples_new), 
                                   (len_old-len(tuples_new)*1.0)/
                                   len_old*100)
        if "ee" in filterCode: 
            print "%i empty entries (%.2f%%)"\
                   %(emptyEntryCounter, emptyEntryCounter*1.0/len_old*100)
        if "bf" in filterCode: 
            print "%i bad formattig (%.2f%%)"\
                  %(badFormattingCounter, badFormattingCounter*1.0/len_old*100)
        if "mw" in filterCode: 
            print "%i multi-word expressions (%.2f%%)"\
                  %(multiWordCount, multiWordCount*1.0/len_old*100)
        if "lp" in filterCode: 
            print "%i low Priority (%.2f%%)"\
                  %(lowPriorityCounter, lowPriorityCounter*1.0/len_old*100)
        if "sw" in filterCode: 
            print "%i stopwords (%.2f%%)"\
                  %(stopWordCounter, stopWordCounter*1.0/len_old*100)
        if "fr" in filterCode: 
            print "%i not frequent enough (%.2f%%)"\
                  %(leftOutCount, leftOutCount*1.0/len_old*100)
        if "ke" in filterCode: 
            print "%i KeyError (%.2f%%)"\
                  %(keyErrorCount, keyErrorCount*1.0/len_old*100)
        print "Ins: %i (%.2f%%)"\
                  %(len(tuples_new) , len(tuples_new)*1.0/len_old*100)
        print ""
    return tuples_new

def createRandomSubset(tuples, size):
    """Creates a random subset of a tuple-array."""
    indices = []
    if size >= len(tuples):
        w("Creating random subset...complete!")
        return tuples
    
    # Selecting indices
    while len(indices) != size:
        percentage = len(indices)*1.0/size*100/2
        wil("Creating random subset - %.2f%% complete" %(percentage))
        index = random.randint(0, len(tuples))
        if index not in indices:
            indices.append(index)
            fl()
    subset = []
    
    # Retrieving entries for corresponding indices
    for index in indices:
        wil("Creating random subset - %.2f%% complete" %(percentage+50))
        subset.append(tuples[index])
        fl()
    wil("Creating random subset...complete!", 30)
    return subset


#----------------------------- Helping functions ------------------------------

def trim(s):
    """Deletes whitspaces in a string before and after a word."""
    res = ""
    for i in range(len(s)):
        if i == 0 and s[i] == " ":
            continue
        elif i == len(s) - 1 and s[i] == " ":
            continue
        else:
            res += s[i]
    return res

def trimArray(a):
    """Deletes entries which are empty strings in an array."""
    return [e for e in a if e != ""]

def arraysIntersect(a1, a2):
    """Tells if two array share at least one element."""
    for e in a1:
        if e in a2:
            return True
    return False

def badFormatting(s, charSet):
    """Tells if a character from charSet appears in a string s."""
    for c in charSet:
        if c in s:
            return True
    return False