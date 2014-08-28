#!/usr/bin/env bash
make
./word2vec -train ../en.txt \
           -output ../en_vectors.txt \
           -min-count 0 \
           -size 10
