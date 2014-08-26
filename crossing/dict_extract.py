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

"""dict_extract.py:

    This module extracts the dict.cc entries of a .txt-file.
    Check out dict.cc here: http://www.dict.cc/
    Download the vocabulary database here: 
    http://www1.dict.cc/translation_file_request.php

    The programs extracts every information for every entry stored in 
    'dict_cc_entries.txt' and returns them as an array of tuples.
    """

#-------------------------------- Imports -------------------------------------

import re

from scrn_out import w, wil, fl 

#------------------------------- Functions ------------------------------------

def extractDictEntries(lines, printErrors=True):
    """ Extracts dictionary entries and returns an array of tuples """
    # You can find the entries in the dict.cc-file in following form:
    # Entry {specification} Additional Entry <Abbreviation> 
    # [Comment1] [Comment2] [...]   wordtype
    # Many of these parts are optional or depend on the word class.
    
    tuples = [] # Array of tuples in form of (German DictEntry object, 
                # english DictEntry object, word class)
    errors = []

    for i in xrange(len(lines)):
        percentage = i*1.0/len(lines)*100
        wil("Extracting and generating dictionary entries - "
                         "%.2f%% complete" %(percentage), 50)
        try:
            # Seperates german part, english part and word class
            _entries = re.split("\t", lines[i]) 
            german_parts = extractParts(_entries[0])
            english_parts = extractParts(_entries[1])
            germanEntry = (german_parts[0], german_parts[1], german_parts[2], 
                           german_parts[3], german_parts[4])
            englishEntry = (english_parts[0], english_parts[1], 
                            english_parts[2], english_parts[3], 
                            english_parts[4])
            tuples.append((germanEntry, englishEntry, _entries[2].
                           replace("\n", "")))

        except Exception, e:
            errors.append("%s with line %s" %(e, lines[i]))
            continue
        finally:
            fl()
    wil("Extracting dictionary entries...Complete!", 90, "\n")
    if printErrors:
        w("The following errors occurred:\n")
        for error in errors:
            w(error)
    return tuples

def extractParts(dict_string):
    """ Extracts the different parts of an entry """
    entry_array = []  # Main entry
    specification = ""  # Specification, e.g. numerus or gender
    additional_entry_array = []  # Additional Entry
    abbr = ""  # Abbreviation
    comments = []  # Array of comments
    entry_end = False  # To determine whether the main entry ended already
    # Splitting with whitspaces; connecting parts in brackets
    parts = connectAnnotations(re.split(" ", dict_string))
    
    for part in parts:
        if part.startswith("{"):
            specification = part
            entry_end = True  # Main entry must have ended
        elif part.startswith("["):
            comments.append(part)
            entry_end = True  # Main entry must have ended
        elif part.startswith("<"):
            abbr = part
            entry_end = True  # Main entry must have ended
        elif not entry_end:
            entry_array.append(" ")  # Main entry is still ongoing
            entry_array.append(part)
        else:
            additional_entry_array.append(" ")  # Additional entry is ongoing
            additional_entry_array.append(part)
    return ("".join(entry_array), "".join(additional_entry_array), 
            specification, abbr, comments)  #

def connectAnnotations(list):
    """ Connects the parts of the entry in parenthesis because 
    else they get split up. """
    res_list = []  
    brackets = {"{": "}", "[": "]", "<": ">"}  # Parenthesis
    ongoing = False  # To determine wether a part in brackets is ongoing
    char = ""  # Current bracket
    
    for entry in list:
        if (entry.startswith("{") and entry.endswith("}")) or \
           (entry.startswith("[") and entry.endswith("]")) or \
           (entry.startswith("<") and entry.endswith(">")): 
            # If part is in brackets and not ongoing
            res_list.append(entry)
        elif ongoing:  # If part in brackets is ongoing
            if entry.endswith(brackets[char]):  # and ends in current part
                ongoing = False
                res_list[len(res_list)-1] += entry
            else:  # or still goes on
                res_list[len(res_list)-1] += entry + " "
        elif entry.startswith("{") or entry.startswith("[") or \
             entry.startswith("<"):  # if part has an opening bracket
            ongoing = True
            char = entry[0]
            res_list.append(entry + " ")
        else:  # Default case
            res_list.append(entry)     
    return res_list