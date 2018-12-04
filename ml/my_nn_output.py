#!/usr/bin/python

import os
import sys
import ROOT
import yaml
import numpy as np


channel = sys.argv[1]
merged_path = "/lstore/cms/ev18131/approach_superclass"
tree_path = os.path.join(channel + "_nominal", "ntuple")
config = yaml.load(open(os.path.join("ml", channel, "dataset_config.yaml")))


class_filepaths = dict()
for process in config["processes"].itervalues():
    _class = process["class"]
    files = process["files"]

    if not class_filepaths.has_key(_class):
        class_filepaths[_class] = list()

    class_filepaths[_class].extend(files)

os.chdir(os.path.join(merged_path, channel))
for _class, filepaths in class_filepaths.iteritems():
    # print("hadd {}.root {}".format(_class, " ".join(filepaths)))
    os.system("hadd {}.root {}".format(_class, " ".join(filepaths)))


#
#
# root_out = ROOT.TFile(os.path.join("ml", channel, "nn_output.root"), "new")
#
# for _class, filepaths in class_filepaths.iteritems():
#     mytree = ROOT.TTree(_class, _class)
#     nn = np.zeros(1, dtype=float)
#     mytree.Branch(_class, nn, _class + "/D")
#
#     chain = ROOT.TChain(tree_path)
#     for filepath in filepaths:
#         chain.Add(os.path.join(merged_path, channel, filepath))
#
#     i=0
#     j=0
#     for evt in chain:
#         if i == 10000:
#             print(j)
#             i = 0
#             j +=1
#         nn[0] = evt.et_signal
#         mytree.Fill()
#         i += 1
#
#     mytree.Write()
#
# root_out.Close()
