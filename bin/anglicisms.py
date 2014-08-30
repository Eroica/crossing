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

"""anglicisms.py:
   This module extracts anglicisms from the online wikipedia wictionary.
   (Check it out here: https://www.wiktionary.org/)

   The program looks into the html-code and checks if an anglicisms has an own
   entry in the wictionary. If so, it will search in it for a 
   german translation.
   """

#-------------------------------- Imports -------------------------------------

import urllib2
import re

from bs4 import BeautifulSoup as BS

from scrn_out import w, wil, fl 

#----------------------------- Main functions ---------------------------------

def getAnglicismsList(url):
    """Extracts a list of anglicisms from a wiktionary page."""
    anglicisms_list_html = BS(urllib2.urlopen(url)) # Extract the html-code
    # Extracting every relevant section from the html-code
    sections = anglicisms_list_html.find_all("p") 
    wil("Extracting anglicisms from wictionary.", 30)
    entries = []  # Array for anglicisms
    
    for section in sections:
        # The many variants of seperators
        section_ = re.split("( - | – | -|- |– )", str(section)) 
        for s in section_:
            entries.append(s)

    entries = entries[3:len(entries)-1]  # Using only the relevant parts
    fl()
    wil("Extracting anglicisms from wictionary..")

    for i in range(len(entries)-1, -1, -1):
        if entries[i] in [" - ", "- ", " -", " – ", "– "]:
            entries.pop(i)  # Popping redundant matches

    fl()
    wil("Extracting anglicisms from wictionary...Complete!", 30, "\n")
    return entries

def generateEntries(list, printErrors=True):
    """Generates array of tuples (anglicism, wiktionary-link)."""
    tuples = []  # Array for tuples (anglicism, wiktionary-link)
    errors = []  
    
    for e in list:
        percentage = list.index(e)*1.0/len(list)*100
        wil("Creating tuples of anglicisms and their wikilink -" 
        	"%.2f%% complete" %(percentage), 60)
        try:
            anglicism = re.findall(">[0-9a-zA-Z-. äöüÄÖÜßé]+<", e)
            if anglicism == []:
                continue
            # Extracting the anglicisms
            anglicism = anglicism[0].replace("<", "").replace(">", "")
            wikilink = ""
            
            if "(Seite nicht vorhanden)" not in str(e):
            	# Extracting the wikilink
                wikilink = re.findall('=".+"\s', e)[0].replace('="', 
                				        "").replace('" ', "") 
                wikilink = "http://de.wiktionary.org" + wikilink
            tuples.append((anglicism, wikilink))
        except Exception, ex:
            errors.append((str(e), str(ex)))
            continue
        finally:
            fl()
                    
    if printErrors == True:
        wil("The following errors occured:", 150, "\n")
        for error in errors:
            print "Error at entry: %s - %s" %(error[0], error[1])

    wil("Creating tuples of anglicisms and their wikilinks...Complete!", 
            30, "\n")
    return tuples

def lookUpTranslations(list, printErrors=True):
    """Looks up the English translation of an anglicism."""
    # Array for tuples with format (anglzism, [translation 1, translation2])
    tuples = [] 
    
    for e in list:
        percentage = list.index(e)*1.0/len(list)*100
        wil("Looking up translations for %s - %.2f%% complete" 
        	%(e[0].replace("ä", "ae").replace("é", "e"), percentage), 20)
        if e[1] == "":  # If there is no wikilink
            fl()
            continue
        try:
            # Extracting the html-code of wiktionary-page
            r = urllib2.Request(e[1])
            html = BS(urllib2.urlopen(r))
            # If there are English translations
            if len(re.findall("/wiki/Englisch.+<\/li>", str(html))) > 0: 
                translations = re.findall("/wiki/Englisch.+<\/li>", 
                						  unicode(html))[0]
                translations = re.findall(">[0-9a-zA-Z-. äöüÄÖÜßé]+<", 
                						  translations)
                for i in range(len(translations)-1, -1, -1):
                    if translations[i] == "> <" or \
                       translations[i] == ">Englisch<":
                        translations.pop(i)  # Popping redundant matches...
                    else:
                    	# ...or just formatting the results
                        translations[i] = translations[i].replace(">", 
                        					"").replace("<", "") 
            else:
                translations = []  # Default
            tuples.append((e[0].decode('utf-8'), translations))
        except Exception, ex:
            if printErrors:
                print str(ex) 
            fl()

    wil("Looking up translations...Complete!%s\n" %(40* " "))          
    return tuples