===========
crossing
===========

crossing simplifies the creation of transformation matrices using scikit-learn.
In theory, crossing can create a transformation matrix that maps a vector
in language A to language B, with vector data provided by programs such as
word2vec.

Requirements
------------

Three files are needed for the generation of transformation matrices:

1. A vector space model for language A
2. A vector space model for language B
3. A dictionary file A->B

The word vectors should like this:

    a 0.1 0.2 0.3
    word 1.0 2.0 3.0
    another 1.1 2.2 3.3
    thing 2.0 3.0 4.0
    ...

The dictionary file should look like this:

    word_1 translation_1
    ...

Usage
-----

It is best used inside the Python interpreter or another script.

Depending on accuracy and regression model, several transformation matrices
can be collected in a ``VectorTransformator'' object:

    >>> vt = crossing.VectorManager.VectorTransformator()

You have to fill VectorTransformator.V, VectorTransformator.W and
VectorTransformator.Dictionary with suitable language data.

A transformation matrix can then be created using:

    >>> vt.createTransformationMatrix()

The matrix is then represented by a ``TransformationMatrix'' object. Both
``TransformationMatrix'' and ``VectorTransformator'' can then be used with
other NumPy data (matrices/vectors) using standard multiplication.

For instance, to transform a vector to language B:

    >>> vt * "word"

Or:

    >>> vt * [1.0, 2.0, 3.0]