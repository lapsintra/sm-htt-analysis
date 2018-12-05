#!/bin/bash

ERA=$1

# Samples Run2016
ARTUS_OUTPUTS_2016=/lstore/cms/bargassa/HTT/Artus_2018-08-21_fixedEmbedding/merged
ARTUS_FRIENDS_ET_2016=/lstore/hpclip/t3cms/lsintra/friends/C_NN2_nn0/et
ARTUS_FRIENDS_MT_2016=/lstore/hpclip/t3cms/lsintra/friends/C_NN2_e95/mt
ARTUS_FRIENDS_TT_2016=/lstore/hpclip/t3cms/lsintra/friends/C_NN2_e95/tt
ARTUS_FRIENDS_FAKE_FACTOR_2016=/lstore/hpclip/t3cms/lsintra/fakes/NN_score
ARTUS_FRIENDS_FAKE_FACTOR_INCL_2016=/lstore/hpclip/t3cms/lsintra/fakes_incl

# Samples Run2017
ARTUS_OUTPUTS_2017=/ceph/akhmet/merged_files_from_naf/27_11_2018_mt-et-tt_all-pipelines_sv-fit
ARTUS_FRIENDS_ET_2017=/ceph/wunsch/Artus17_Nov/et_keras_20181202
ARTUS_FRIENDS_MT_2017=/ceph/wunsch/Artus17_Nov/mt_keras_20181202
ARTUS_FRIENDS_TT_2017=/ceph/wunsch/Artus17_Nov/tt_keras_20181204
ARTUS_FRIENDS_FAKE_FACTOR_2017=/ceph/swozniewski/SM_Htautau/ntuples/Artus17_NovPU/fake_factor_friends_njets_mvis_NEW_NN_Dec04
ARTUS_FRIENDS_FAKE_FACTOR_INCL_2017=/ceph/swozniewski/SM_Htautau/ntuples/Artus17_NovPU/fake_factor_friends_njets_mvis_incl_NEW23

# Error-handling
if [[ $ERA == *"2016"* ]]
then
    ARTUS_OUTPUTS=$ARTUS_OUTPUTS_2016
    ARTUS_FRIENDS_ET=$ARTUS_FRIENDS_ET_2016
    ARTUS_FRIENDS_MT=$ARTUS_FRIENDS_MT_2016
    ARTUS_FRIENDS_TT=$ARTUS_FRIENDS_TT_2016
    ARTUS_FRIENDS_FAKE_FACTOR=$ARTUS_FRIENDS_FAKE_FACTOR_2016
    ARTUS_FRIENDS_FAKE_FACTOR_INCL=$ARTUS_FRIENDS_FAKE_FACTOR_INCL_2016
elif [[ $ERA == *"2017"* ]]
then
    ARTUS_OUTPUTS=$ARTUS_OUTPUTS_2017
    ARTUS_FRIENDS_ET=$ARTUS_FRIENDS_ET_2017
    ARTUS_FRIENDS_MT=$ARTUS_FRIENDS_MT_2017
    ARTUS_FRIENDS_TT=$ARTUS_FRIENDS_TT_2017
    ARTUS_FRIENDS_FAKE_FACTOR=$ARTUS_FRIENDS_FAKE_FACTOR_2017
    ARTUS_FRIENDS_FAKE_FACTOR_INCL=$ARTUS_FRIENDS_FAKE_FACTOR_INCL_2017
else
    echo "[ERROR] Era $ERA is not implemented." 1>&2
    read -p "Press any key to continue... " -n1 -s
fi

# Kappa database
KAPPA_DATABASE=/lstore/cms/bargassa/HTT/Artus_2018-08-21/datasets_2018-08-01.json
