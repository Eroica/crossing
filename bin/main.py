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

"""main.py

    This is a meta-script which contains every process of data-preparation 
    for CrOssinG.
    """

#--------------------------------- Imports ------------------------------------

import urllib2
import re

from bs4 import BeautifulSoup as BS

from file_handling import writeTupleFile, readFile
from anglicisms import getAnglicismsList, generateEntries, lookUpTranslations
from dict_extract import extractDictEntries
from false_friends import extractFalseFriends
from filter import filterTuples, createRandomSubset
from scrn_out import wil, w, wh, fl, cl

#------------------------------- Main functions -------------------------------

def main():
    """ Main function to run most parts of CrOssinG """
    cl()
    wh("\t\tCrOssinG: CompaRing Of AngliciSmS IN German", 75)

    # paths
    ANGLICISMS_PATH = "../res/anglicisms.txt"
    DICTENTRIES_PATH = "../res/dictEntries.txt"
    FALSE_FRIENDS_PATH = "../res/false_friends.txt"
    SUBSET_PATH = "../res/subset.txt"

    # 1.: Extracts anglicisms and their translations
    w("+++++ Anglicisms (1/3) +++++")
    anglicisms_html = getAnglicismsList("http://de.wiktionary.org/wiki/"
                                        "Verzeichnis:Deutsch/Anglizismen")
    anglicisms = generateEntries(anglicisms_html, False)
    anglicisms_tuples = lookUpTranslations(anglicisms)
    anglicisms_tuples = filterTuples(anglicisms_tuples, "AN")
    writeTupleFile(anglicisms_tuples, ANGLICISMS_PATH)

    # 2.: Extracts dictionary entries and writes them
    w("\n++++++ Dictionary Entries (2/3) +++++")
    dictLines = readFile("../res/dict_cc_entries.txt", "#")
    dictEntries = extractDictEntries(dictLines, False)
    dictEntries = filterTuples(dictEntries, "DE", 100)
    writeTupleFile(dictEntries, DICTENTRIES_PATH)
    subset = createRandomSubset(dictEntries, 300)
    writeTupleFile(subset, SUBSET_PATH)

    # 3.: Extracts false friends
    w("\n+++++ False Friends (3/3) ++++++")
    false_friends = readFile("../res/false_friends.txt")
    false_friends_tuples = extractFalseFriends(false_friends)
    false_friends_tuples = filterTuples(false_friends_tuples,"FF", True)
    writeTupleFile(false_friends_tuples, FALSE_FRIENDS_PATH)

#------------------------------------ Main ------------------------------------

if __name__ == "__main__":
    main()