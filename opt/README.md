WikiExtractor.py
================

`crossing` ships with a special version of `WikiExtractor.py` that
is able to extract characters based on its unicode group.

A file with the changes to the original `WikiExtractor.py` can be found in this
directory.

Usage
-----

A unicode group contains characters with similiar features, for instance:

*   `Lu` contains all upper case letters, regardless of having accents
    or other diacritic marks.
*   `Ll` contains all lower case letters.
*   `Po` contains all punctuation marks such as full stops, commas, etc.

You can then run `WikiExtractor.py` and pass several unicode groups as arguments.
This will tell `WikiExtractor.py` to discard all characters not found in those
unicode groups.

For instance, to only extract lowercase characters (most English word),
invoke `WikiExtractor.py` like this:

    ./WikiExtractor.py --unigroups=Ll

However, this will discard capital letters from names, beginning of sentences, etc.
To basically extract all words that are written with letters, run `WikiExtractor.py` like this:

    ./WikiExtractor.py --unigroups=LuLl

Or pass the `--lowcase` argument to convert everything to lower case while parsing:

    ./WikiExtractor.py --unigroups=Ll --lowcase 1

This offers a great flexibility depending on what the corpus should be extracted for.
For example: If one is interested in all words that form sentences, the option to
preserve punctuation marks can be passed:

    ./WikiExtractor.py --unigroups=LlPo --lowcase 1

For the use with `word2vec`, another option is provided: `--concatenate=[FILE]`.

Imagine this sentence: "The world wide web is a ..."

`word2vec` would parse "world wide web" as three different words, but when using
vector space models, it is helpful to regard this as a single word.
The `--concatenate` option allows you to pass a file that looks like this:

    world wide web
    world of warcraft
    ...

This will tell `WikiExtractor.py` to concatenate those words with an underscore.
`word2vec` will then parse `world_wide_web`, `world_of_warcraft`, ... as a single word.

The complete command line arguments for the patched `WikiExtractor.py` are:

    --unigroups={Lu|Ll|Po|...}  :   Extract only characters found
                                    in these unicode groups
    --lowcase=[VALUE]           :   If a value is passed, convert
                                    everything to lower case while parsing.
    --concatenate=[FILE]        :   Pass a plain text file containing words,
                                    line by line, that should be concatenated
                                    with an underscore while parsing.