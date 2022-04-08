#!/bin/bash

We="1.0"
Ohs="1e-5"
Lo="4.0"
Level="10"
tmax="25"
Bo="0.1"
Ohd="0.1"

qcc -fopenmp -Wall -O2 bounce.c -o bounce -lm # Linux
# qcc -Xpreprocessor -fopenmp -lomp -Wall -O2 bounce.c -o bounce -lm #Mac
export OMP_NUM_THREADS=8
./bounce $Level $tmax $We $Ohd $Ohs $Bo $Lo
