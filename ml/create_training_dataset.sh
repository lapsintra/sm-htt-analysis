#!/bin/bash

ERA=$1
CHANNEL=$2

source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
source utils/setup_samples.sh $ERA

mkdir -p ml/${ERA}_${CHANNEL}

python ml/write_dataset_config.py \
    --era ${ERA} \
    --channel ${CHANNEL} \
    --base-path $ARTUS_OUTPUTS \
    --database $KAPPA_DATABASE \
    --output-path $PWD/ml/${ERA}_${CHANNEL} \
    --output-filename training_dataset.root \
    --tree-path ${CHANNEL}_nominal/ntuple \
    --event-branch event \
    --training-weight-branch training_weight \
    --additional-cuts ml/${ERA}_${CHANNEL}_cuts.yaml \
    --friends-config ml/${ERA}_${CHANNEL}_friends.yaml \
    --output-config ml/${ERA}_${CHANNEL}/base_dataset_config.yaml

./htt-ml/dataset/create_training_dataset.py ml/${ERA}_${CHANNEL}/base_dataset_config.yaml

# cp ml/${ERA}_${CHANNEL}/base_dataset_config.yaml ml/${ERA}_${CHANNEL}/dataset_config.yaml

python ml/my_create_superclass.py \
    --train-config ml/${ERA}_${CHANNEL}_training.yaml \
    --classes-config ml/${ERA}_${CHANNEL}_classes.yaml \
    --input-config ml/${ERA}_${CHANNEL}/base_dataset_config.yaml \
    --output-config ml/${ERA}_${CHANNEL}/dataset_config.yaml

rm -f ml/${ERA}_${CHANNEL}/*.root

./htt-ml/dataset/create_training_dataset.py ml/${ERA}_${CHANNEL}/dataset_config.yaml

hadd -f ml/${ERA}_${CHANNEL}/combined_training_dataset.root \
    ml/${ERA}_${CHANNEL}/fold0_training_dataset.root \
    ml/${ERA}_${CHANNEL}/fold1_training_dataset.root
echo
python ./ml/my_training_weights.py ml/${ERA}_${CHANNEL}/combined_training_dataset.root \
    ml/${ERA}_${CHANNEL}_training.yaml
echo
