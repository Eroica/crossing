crossing
========

"crossing" originally started as a software project by [Dennis Ulmer](https://github.com/Kaleidophon)
and [Sebastian Spaar](https://github.com/Eroica) during the summer semester 2014
at Heidelberg University, Germany.

In theory, `crossing` tries to create a transformation matrix from one
[Vector Space Model](http://en.wikipedia.org/wiki/Vector_space_model) in language A
to another one in language B using a provided dictionary (for instance, German-English).
Then---taking an unknown vector `v` in language A (a word not found in the
dictionary)---`crossing` can transform that vector into language B using the calculated
transformation matrix and looking for the most similiar vector in language B.

During the software project, `crossing` was used to analyze [anglicisms](http://en.wikipedia.org/wiki/Denglisch)
found in the German language, and whether that anglicism's meaning has changed
compared to the original English word (hence, "CrOssinG"---*C*ompa*R*ing *O*f Anglici*S*m*S* *IN* *G*erman).

Vector space models were created by using [`word2vec`](https://code.google.com/p/word2vec/)
on an English and German Wikipedia dump, that were converted to plaintext characters
beforehand using a slightly altered version of [`WikiExtractor.py`](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor).

Many thanks to [http://www.dict.cc](http://www.dict.cc) that provided us with a
German-English dictionary.

The original data and scripts that were used can be found in the `bin/` and `res/`
directories.

Installation
------------

`crossing` requires the following Python packages:

*   NumPy
*   SciPy
*   Scikit-Learn

Use `pip install -r requirements.txt` to install `crossing` and its requirements.
Using a virtual environment is recommended for not spamming your system packages
with a small software project.

Usage
-----

tbd