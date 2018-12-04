#!/bin/bash

RUN=$1
CHANNEL=$2

mkdir -p shelf/$RUN/$CHANNEL
mv *.root *.txt *.json *.pdf *.png *.log *.html plots output shelf/$RUN/$CHANNEL
