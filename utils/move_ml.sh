#!/bin/bash

RUN=$1
ERA=$2
CWD=$(pwd)

mkdir -p ${CWD}/shelf/$RUN/ml
cd ml
cp *.yaml ${CWD}/shelf/$RUN/ml

for CHANNEL in et mt tt; do
    mkdir ${CWD}/shelf/${RUN}/ml/${CHANNEL}
    cd ${CWD}/ml/${ERA}_${CHANNEL}
    cp *.h5 *.pickle *.png *.yaml ${CWD}/shelf/${RUN}/ml/${ERA}_${CHANNEL}
done
