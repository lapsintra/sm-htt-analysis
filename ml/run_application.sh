#!/bin/bash

ERA=$1
CHANNEL=$2

source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
source utils/setup_samples.sh $ERA

python ml/write_application_filelist.py \
    --directory $ARTUS_OUTPUTS \
    --database $KAPPA_DATABASE \
    --channel ${CHANNEL} \
    --era ${ERA} \
    --output ml/${ERA}_${CHANNEL}/application_filelist.yaml

export KERAS_BACKEND=theano
export OMP_NUM_THREADS=32
# export THEANO_FLAGS=gcc.cxxflags=-march=corei7

python ml/run_application.py \
    --dataset-config ml/${ERA}_${CHANNEL}/dataset_config.yaml \
    --training-config ml/${ERA}_${CHANNEL}_training.yaml \
    --application-config ml/${ERA}_${CHANNEL}_application.yaml \
    --filelist ml/${ERA}_${CHANNEL}/application_filelist.yaml \
    --num-processes 8
