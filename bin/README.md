main.py
========

main.py is the main script for the whole data preparation process.
It extracts all the entries from the dict.cc-dictionary and filters them, extracts the false-friend-pairs used for evaluation and a list of anglicisms from wictionary.com.

Usage
-----

For using the script the recommended way, just execute it in your terminal:

>>> python main.py

If you wish to alter the resource directories, change the following variables at the begin of the script, which are set by default to the following values:

# paths
ANGLICISMS_PATH = "../res/anglicisms.txt"
DICTENTRIES_PATH = "../res/dictEntries.txt"
FALSE_FRIENDS_PATH = "../res/false_friends.txt"
SUBSET_PATH = "../res/subset.txt"

If you want to change the filter settings for the dictionary-extraction, add the
filterCode-parameter to the following line in main.py:

dictEntries = filterTuples(dictEntries, "DE", 100)

for e.g.

dictEntries = filterTuples(dictEntries, "DE", 100, filterCode="mw2lp")

You can find further explanation on how to create a filterCode in filter.py.

Summary
-------

This part is very project-specific. Don't expect to use much of this code here when applying the vector-transformation-part of CrOssInG to other languages or corpora.