#!/usr/bin/env bash

python3 make-chapter-title.py $1 | tee >(pbcopy)
