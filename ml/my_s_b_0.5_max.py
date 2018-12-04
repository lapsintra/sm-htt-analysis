#!/usr/bin/python

import json
import os
import sys
import ROOT
import yaml
import numpy as np


channel = sys.argv[1]

merged_path_friends = "/lstore/cms/ev18131/approach_superclass"
merged_path_orig = "/lstore/cms/bargassa/HTT/Artus_2018-02-25/merged"
tree_path = os.path.join(channel + "_nominal", "ntuple")
config = yaml.load(open(os.path.join("ml", channel, "dataset_config.yaml")))
kappa_dataset = json.load(open(os.path.join("ml", "datasets.json")))

class_filepaths = dict()

for key,process in config["processes"].iteritems():
    _class = process["class"]
    files = process["files"]

    if not class_filepaths.has_key(_class):
        class_filepaths[_class] = list()
    if key != "qqH" and key != "ZTT":
        class_filepaths[_class].extend(files)


lumi = 35870.0

yields = dict()
uncer_yields = dict()

cuts = list(np.arange(0.0, 1.0, 0.05))
figs_merit = list()
uncer_figs_merit = list()

for cut in cuts:
    cut_str = "{:.2f}".format(cut)

    yields[cut_str] = dict()
    uncer_yields[cut_str] = dict()



    for _class, class_files in class_filepaths.iteritems():
        total_yield = 0.0
        var_total_yield = 0.0

        for file_ in class_files:

            root_orig =ROOT.TFile(os.path.join(merged_path_orig, file_), "read")
            tree_orig =root_orig.Get(tree_path)
            leafy = tree_orig.GetLeaf("crossSectionPerEventWeight")
            leafy.GetBranch().GetEntry(0)
            cross_section = leafy.GetValue()

            root_app = ROOT.TFile(os.path.join(merged_path_friends, channel, file_), "read")
            tree_friends = root_app.Get(tree_path)

            tot_gen_evts = int(kappa_dataset[os.path.dirname(file_)]["n_events_generated"])
            uncer_tot_gen_evts = tot_gen_evts**0.5
            sel_evts = tree_friends.GetEntries("{}_signal >= {}".format(channel, cut))
            uncer_sel_evts = sel_evts**0.5

            if not sel_evts:
                continue

            process_yield =  lumi*cross_section*sel_evts/tot_gen_evts
            uncer_process_yield = process_yield * abs(uncer_sel_evts/sel_evts - uncer_tot_gen_evts/tot_gen_evts)

            total_yield += process_yield
            var_total_yield += uncer_process_yield**2

        uncer_total_yield = var_total_yield**0.5

        yields[cut_str][_class] = total_yield
        uncer_yields[cut_str][_class] = uncer_total_yield

    s = yields[cut_str]["signal"]
    b = yields[cut_str]["background"]
    uncer_s = uncer_yields[cut_str]["signal"]
    uncer_b = uncer_yields[cut_str]["background"]
    print("s:", s, uncer_s)
    print("b:", b, uncer_b)

    fig_merit = s/b**0.5
    uncer_fig_merit = (uncer_s**2/b + s**2*uncer_b**2/(4*b**3))**0.5

    figs_merit.append(fig_merit)
    uncer_figs_merit.append(uncer_fig_merit)

    print("At {} -> {:.2f} +- {}".format(cut, fig_merit, uncer_fig_merit))

n = len(cuts)
cuts_array = np.array(cuts)
fig_array =  np.array(figs_merit)
uncer_fig_array = np.array(uncer_figs_merit)
horiz_error = np.zeros(n, dtype=float)

gr = ROOT.TGraphErrors(n, cuts_array, fig_array, horiz_error, uncer_fig_array)
gr.Draw()

ROOT.gSystem.Run()
