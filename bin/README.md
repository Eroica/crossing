WikiExtractor.py
================

**CrOssinG** ships with a special version of `WikiExtractor.py` that
is able to extract characters based on its unicode group.

The original `WikiExtractor.py` needs to be patched first with the patch
found in this directory:

    patch < extractUnigroups.diff

A unicode group contains characters with similiar features, for instance:

*   `Lu` contains all upper case letters, regardless of having accents
    or other diacritic marks.
*   `Ll` contains all lower case letters.
*   `Po` contains all punctuation marks such as full stops, commas, etc.

Invoking `WikiExtractor.py` with several unicode groups as arguments tells
`WikiExtractor.py` to discard all characters that are not present in the
passed groups.

For instance, to only extract lowercase characters (most English word),
invoke `WikiExtractor.py` like this:

    ./WikiExtractor.py --unigroups=Ll

However, this will discard a beginning capital letter. To basically extract
all words that are written with letters, run `WikiExtractor.py` like this:

    ./WikiExtractor.py --unigroups=LuLl

Or pass the `--lowcase` argument to convert everything to lower case
while parsing:

    ./WikiExtractor.py --unigroups=Ll --lowcase 1

The strength in passing variable unicode groups is that it offers great
flexibility depending on what the corpus should be extracted for.
For example: The aforementioned commands extract all words one by one—
if one is interested in what words make up sentences, just pass the option
to preserve punctuation marks:

    ./WikiExtractor.py --unigroups=LlPo --lowcase 1

The complete command line arguments for the patched `WikiExtractor.py` are:

    --unigroups={Lu|Ll|Po|...}  :   Extract only characters found
                                    in these unicode groups
    --lowcase=[VALUE]           :   If a value is passed, convert
                                    everything to lower case while parsing.
    --concatenate=[FILE]        :   Pass a plain text file containing
                                    words, line by line, that should
                                    be concatenated with an `_''
                                    while parsing.