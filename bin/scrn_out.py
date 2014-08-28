#!/usr/bin/python
# -*- coding: utf-8 -*-

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

"""scrn_out.py:

   This module just simplifies screen output in other modules.
   """

#-------------------------------- Imports -------------------------------------

import sys
import os

#------------------------------ Main functions --------------------------------

def cl():
	""" Clears Screen """
	clearScreen = ['cls', 'clear'][os.name == 'posix']
	os.system(clearScreen)

def w(s, whitespaces = 0):
	""" Writes on screen """
	sys.stdout.write("%s%s" %(s, " "*whitespaces))

def wil(s, whitespaces = 0, _finally = ""):
	""" Writes on screen without beginning a new line plus opt. whitespaces """
	sys.stdout.write("\r%s%s%s" %(s, " "*whitespaces, _finally))

def wh(h, hyphons = 0):
	""" Writes a header """
	sys.stdout.write("%s\n%s\n%s\n\n" %("-"*hyphons, h, "-"*hyphons))

def fl():
	""" Flushes """
	sys.stdout.flush()