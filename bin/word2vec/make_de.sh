#!/usr/bin/env bash
make
./word2vec -train ../de.txt \
           -output ../de_vectors.txt \
           -min-count 0 \
           -size 10
