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
These tools can be found in the `opt/` directory.

Many thanks to [http://www.dict.cc](http://www.dict.cc) that provided us with a
German-English dictionary.

Installation
------------

`crossing` requires the following Python packages:

*   NumPy
*   SciPy
*   scikit-Learn
*   nose (a requirement of scikit-learn, sometimes needed for installation)
*   BeautifulSoup (for the scripts found in `bin/`)

Use `pip install -r requirements.txt` to install `crossing` and its requirements.
Using a virtual environment is recommended for not spamming your system packages
with a small software project.

Usage
-----

`crossing`'s usage can easily be learned by using it interactively in a
Python interpreter. Make sure to install `crossing` and its dependencies,
open a Python interpreter and import it:

    >>> import crossing

There is some example data prepared in the `share/` directory:

    share
    ├── de.txt
    ├── de_dummy.txt
    ├── de_vectors.txt
    ├── dict.txt
    ├── dict_dummy.txt
    ├── en.txt
    ├── en_dummy.txt
    └── en_vectors.txt

Of these files, `de_vectors.txt`, `en_vectors.txt` and `dict.txt` are of
particular interest. They are based on the corpus "Town Musicians of Bremen"
found in `de.txt/en.txt`. Let's create a `VectorTransformator` object that will
serve sevel vector transformation matrices:

    >>> vt = crossing.VectorManager.VectorTransformator()

We have to fill our `vt` object with some language data. `vt` has three variables
that need to be filled: `vt.V` and `vt.W` represent two vector spaces, and
`vt.Dictionary` contains the translation of the words found in `vt.V` to `vt.W`.
For this example, use the data found in the `share/` directory and load them
into `vt` using the functions of `FileManager.py`:

    >>> vt.Dictionary = FileManager.readDictionary("../share/dict.txt")
    >>> vt.V = FileManager.readWord2Vec("../share/de_vectors.txt")
    >>> vt.W = FileManager.readWord2Vec("../share/en_vectors.txt")

(Since we are working with `word2vec` data, `FileManager.readWord2Vec()` is used.
However, you could pass every dictionary in the following format to `vt.V/W`:)

    {"word" = [1.0, 2.0, 3.0, ...], "another" = [0.1, 0.2, 0.3, ...], ...}

Remember that `VectorTransformator` only wraps several transformation matrices.
This way you could create different transformation models and compare their
accuracies. Let's create a transformation matrix now -- by default, `sklearn.Linear_Model.Lasso`
with `alpha = 0.1` is used (refer to the `docstring` to see other models):

    >>> vt.createTransformationMatrix()

Let's have a look at the word `katze` (German for *cat*). Its vector form is,
in German and English respectively:

    katze 0.006136 -0.052587 0.012688 -0.014030 -0.046991 0.042845 -0.023529 -0.001199 0.034139 -0.003296 
    cat -0.067114 0.033746 0.020565 0.032246 0.113999 0.016741 -0.021005 0.043264 0.060346 -0.008794 

We can now see how `crossing` would transform the vector for `katze` into the
English vector space, using the transformation matrix that was just created:

    >>> vt * "katze"
    (matrix([[-0.01070324],
            [-0.00699281],
            [ 0.00408598],
            [ 0.00868466],
            [ 0.03515451],
            [-0.00209241],
            [-0.02295664],
            [ 0.01283001],
            [ 0.01598752],
            [-0.00638645]]),)

Summary
-------

Most of the time, when using vector information from `word2vec` and `sklearn.Linear_Models`,
our algorithm fails miserably to create an adequate transformation matrix. One
reason might be that the information provided by `word2vec` is not useful for creating
a vector space model of a language, since `word2vec` is more of a straightforward
approach of representing words by a numerical value.

Using dummy data, like the `_dummy` files found in `share/`, creating transformation
matrices works fine.