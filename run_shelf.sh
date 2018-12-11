#!/bin/sh

RUN=$1

for CHANNEL in et mt tt; do
    ml/run_testing.sh 2016 $CHANNEL
done

utils/move_ml.sh $RUN 2016
