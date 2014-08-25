crossing
========

"crossing" originally started as a software project by [Dennis Ulmer](https://github.com/Kaleidophon)
and [Sebastian Spaar](https://github.com/Eroica) during the summer semester 2014
at Heidelberg University, Germany.

In theory, `crossing` tries to create a transformation matrix from one
[Vector Space Model](http://en.wikipedia.org/wiki/Vector_space_model) in language A
to another one in language B using a provided dictionary (for instance, German-English).
Then -- taking an unknown vector `v` in language A (a word not found in the
dictionary) -- `crossing` can transform that vector into language B using the calculated
transformation matrix and looking for the most similiar vector in language B.

During the software project, `crossing` was used to analyze [anglicisms](http://en.wikipedia.org/wiki/Denglisch)
found in the German language, and whether that anglicism's meaning has changed
compared to the original English word (hence, *"CrOssinG"* -- CompaRing Of AngliciSmS IN German).

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

`crossing`'s usage can easily be learned by using it interactively in a
Python interpreter. Make sure to install `crossing` and its dependencies,
open a Python interpreter and import it:

    >>> import crossing

There is some example data prepared in the `res/` directory:

    res/
    ├── de.txt
    ├── de_vectors.txt
    ├── dict.txt
    ├── en.txt
    └── en_vectors.txt

Of these files, `de_vectors.txt`, `en_vectors.txt` and `dict.txt` are of
particular interest. They are based on the corpus "Town Musicians of Bremen"
found in `de.txt/en.txt`. Let's create a `VectorTransformator` object that will
represent vector transformations from German to English using `dict.txt`:

    >>> vt = crossing.VectorManager.VectorTransformator("res/dict.txt", "res/de_vectors.txt", "res/en_vectors.txt")

`VectorTransformator` only wraps several transformation matrices. This way you
could compare different transformation models and different accuracies. We now 
need to create a transformation matrix -- by default, `sklearn.Linear_Model.Lasso`
with `alpha = 0.1` is used (refer to the `docstring` to see other models):

    >>> vt.createTransformationMatrix()

Let's have a look at the word `katze` (German for *cat*). Its vector form is,
in German and English respectively:

    katze   0.000607 -0.005260  0.001268 -0.001395 -0.004689  0.004297 -0.002352 ...
    cat    -0.000362  0.003718 -0.004984  0.004327  0.002802 -0.004585 -0.001044 ...

We can now see how `crossing` would transform the vector for `katze` into the
English vector space, using the transformation matrix that was just created:

    >>> vt * "katze"

Summary
-------

Most of the time, when using vector information from `word2vec` and `sklearn.Linear_Models`,
our algorithm fails miserably to create an adequate transformation matrix. One
reason might be that the information provided by `word2vec` is not useful for creating
a vector space model of a language, since `word2vec` straightforwardly tries to
represent a word by a numerical value.