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

"""false_friends.py:

    This module extracts false-friend-pairs from the
    "Liste falscher Freunde - Wikipedia".html file.
    """

#-------------------------------- Imports -------------------------------------

from scrn_out import wil, fl 

#----------------------------- Functions --------------------------------------

def extractFalseFriends(lines):
    """ Extracts false friends from txt-File """
    wil("Extracting False Friends...")
    tuples = []
    array = ["" for i in range(4)]  
    entry_index = 0
    
    for l in lines:
        if l == "\n":
            # Reset
            entry_index = 0
            array = ["" for i in range(4)]
        elif entry_index == 3:
            array[entry_index] = l.replace("\n", "").replace("\t", "")
            tuples.append(tuple(array))
            # Reset
            entry_index = 0
            array = ["" for i in range(4)]
        else:
            array[entry_index] = l.replace("\n", "").replace("\t", "")
            entry_index += 1
    fl()
    wil("Extracting False Friends...Complete!\n")
    return tuples