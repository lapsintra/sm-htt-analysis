#!/bin/bash

RUN=$1

for CHANNEL in cmb et mt tt; do
    if [ $CHANNEL=="cmb" ]; then
        CHANNELS="et mt tt"
    else
        CHANNELS=$CHANNEL
    fi
    
    ./run_analysis.sh 2016 $CHANNELS
    utils/move.sh $RUN $CHANNEL
done
