#!/bin/bash

RUN=$1
CHANNEL=$2

mkdir -p shelf/$RUN/$CHANNEL
mv *.root *.txt *.json *.pdf *.png *.log *.html 2016_plots output shelf/$RUN/$CHANNEL
