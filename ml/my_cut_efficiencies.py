
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
config = yaml.load(open(os.path.join("ml", channel + "_base_dataset_config.yaml")))
kappa_dataset = json.load(open(os.path.join("ml", "datasets.json")))

class_filepaths = dict()

for key,process in config["processes"].iteritems():
    _class = process["class"]
    files = process["files"]

    if not class_filepaths.has_key(_class):
        class_filepaths[_class] = list()

    class_filepaths[_class].extend(files)


cuts = list(np.arange(0.0, 1.0, 0.05))
effs_per_class = dict()

for _class, class_files in class_filepaths.iteritems():
    effs_per_class[_class] = list()
    for cut in cuts:
        weighted_eff = 0.
        sum_weights = 0.

        for file_ in class_files:

            root_orig = ROOT.TFile(os.path.join(merged_path_orig, file_), "read")
            tree_orig = root_orig.Get(tree_path)
            leafy = tree_orig.GetLeaf("crossSectionPerEventWeight")
            leafy.GetBranch().GetEntry(0)
            cross_section = leafy.GetValue()
            root_app = ROOT.TFile(os.path.join(merged_path_friends, channel, file_), "read")
            tree_friends = root_app.Get(tree_path)

            tot_gen_evts = int(kappa_dataset[os.path.dirname(file_)]["n_events_generated"])
            uncer_tot_gen_evts = tot_gen_evts**0.5
            sel_evts = float(tree_friends.GetEntries("{}_signal >= {}".format(channel, cut)))
            uncer_sel_evts = sel_evts**0.5

            weighted_eff += sel_evts/tot_gen_evts * cross_section
            sum_weights += cross_section


        efficiency = weighted_eff/sum_weights
        print(_class, cut,  efficiency)
        effs_per_class[_class].append(efficiency)

n = len(cuts)
cuts_array = np.array(cuts)
graphs = list()

vert_error = np.zeros(n, dtype=float)
horiz_error = np.zeros(n, dtype=float)

legend = ROOT.TLegend()
for i_class, _class in enumerate(class_filepaths):
    eff_array =  np.array(effs_per_class[_class])

    gr = ROOT.TGraphErrors(n, cuts_array, eff_array, vert_error, horiz_error)
    gr.SetMarkerStyle(21)
    gr.SetMarkerColor(i_class+1)

    legend.AddEntry(gr, _class, "p")

    if i_class == 0:
        gr.SetTitle("efficiencies")
        gr.Draw("APL")
    else:
        gr.Draw("PL")

    graphs.append(gr)
legend.Draw()

ROOT.gSystem.Run()
