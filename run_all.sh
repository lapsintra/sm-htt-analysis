#!/bin/bash

RUN=$1

ERA=2016
# for CHANNEL in et mt tt; do
#     ml/create_training_dataset.sh $ERA $CHANNEL
#     ml/run_training.sh $ERA $CHANNEL
#     ml/run_testing.sh $ERA $CHANNEL
#     ml/run_application.sh $ERA $CHANNEL
# done
#
# utils/move_ml.sh $RUN 2016
#
# fake-factors/run_fake_factors.sh 2016 NN_score inclusive

# for CHANNEL in et mt tt cmb; do
for CHANNEL in et mt tt; do
    echo Analysis on $CHANNEL channel
    if [ $CHANNEL == "cmb" ]; then
        CHANNELS="et mt tt"
    else
        CHANNELS=$CHANNEL
    fi

    ./run_analysis.sh 2016 $CHANNELS
    utils/move.sh $RUN $CHANNEL
done
