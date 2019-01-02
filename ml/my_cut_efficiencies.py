
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # disable ROOT internal argument parser
ROOT.gErrorIgnoreLevel = ROOT.kError
import json
import os
import sys
import yaml
import numpy as np
import argparse

import logging
logger = logging.getLogger()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Plot efficiencies for NN cuts.")

    parser.add_argument(
        "--directory",
        required=True,
        type=str,
        help="Directory with Artus outputs.")
    parser.add_argument(
        "--et-friend-directory",
        default=None,
        type=str,
        help=
        "Directory arranged as Artus output and containing a friend tree for et."
    )
    parser.add_argument(
        "--mt-friend-directory",
        default=None,
        type=str,
        help=
        "Directory arranged as Artus output and containing a friend tree for mt."
    )
    parser.add_argument(
        "--tt-friend-directory",
        default=None,
        type=str,
        help=
        "Directory arranged as Artus output and containing a friend tree for tt."
    )
    parser.add_argument(
        "--channel",
        type=str,
        help="Channel to be considered.")
    parser.add_argument("--era", type=str, help="Experiment era.")
    return parser.parse_args()



def main(args):
    channel = args.channel
    era = args.era

    friend_path = getattr(args, "{}_friend_directory".format(channel))
    merged_path = args.directory
    tree_path = os.path.join("{}_nominal".format(channel), "ntuple")
    config = yaml.load(open(os.path.join("ml", "{}_{}".format(era, channel), "base_dataset_config.yaml")))
    binning = list(np.arange(0., 1.01, 0.01))
    nn_cuts = list(np.arange(0., 1.0, 0.01))

    color_dict = {
        "ZTT": ROOT.kOrange-4,
        "ZL": ROOT.kAzure+8,
        "ZJ": ROOT.kTeal+9,
        "TTJ": ROOT.kMagenta-6,
        "TTT": ROOT.kBlue-6,
        "W": ROOT.kRed-6,
        "VV": ROOT.kRed-1,
        "QCD": ROOT.kRed-10,
        "EWKWm": ROOT.kSpring+1,
        "EWKWp": ROOT.kSpring+1,
        "EWKZ": ROOT.kSpring+1,
        "ggH": ROOT.kRed+1,
        "qqH": ROOT.kTeal-6
    }

    hists = dict()
    for pname, process in config["processes"].iteritems():

        print(pname)

        hname = pname
        htitle = pname
        hist = ROOT.TH1F(hname, htitle, len(binning)-1, np.array(binning))
        hist.SetMinimum(1e-1)
        hist.Sumw2()
        hists[pname] = hist

        cuts = process["cut_string"]
        weights = process["weight_string"]

        for cut in nn_cuts:
            print(cut)
            cut_string = "({})*({})".format("{}_signal >= {}".format(channel, cut), cuts)

            tree = ROOT.TChain()
            friend_tree = ROOT.TChain()
            for file_ in process["files"]:
                tree.Add(os.path.join(merged_path, file_, tree_path))
                friend_tree.Add(os.path.join(friend_path, file_, tree_path))
            tree.AddFriend(friend_tree)

            tree.Draw("{}_signal*0.01 + {} >> +{}".format(channel, cut, hname), cut_string, "goff")

            tree.RemoveFriend(friend_tree)
            tree.Reset()
            friend_tree.Reset()


    canvas = ROOT.TCanvas("c1", "c1", 579, 188, 700, 500)
    canvas.cd()
    # canvas.cd().SetLogy()

    n = len(nn_cuts)
    x_array = np.array(nn_cuts)
    err_x_array = np.zeros(n, dtype=float)
    legend = ROOT.TLegend()
    graphs = list()
    for i_hist, (pname, hist) in enumerate(hists.iteritems()):
        y = list()
        err_y = list()
        total = hist.GetBinContent(1)
        if total == 0:
            continue
        err_total = hist.GetBinError(1)
        for i_bin, bin_xlow in enumerate(nn_cuts):
            i_bin += 1

            selected = hist.GetBinContent(i_bin)
            err_selected = hist.GetBinError(i_bin)

            efficiency = selected/total
            if selected == 0:
                err_efficiency = efficiency*abs(err_selected - err_total/total)
            else:
                err_efficiency = efficiency*abs(err_selected/selected - err_total/total)

            y.append(efficiency)
            err_y.append(err_efficiency)

        y_array = np.array(y)
        err_y_array = np.array(err_y)

        gr = ROOT.TGraphErrors(n, x_array, y_array, err_x_array, err_y_array)
        gr.SetMarkerStyle(21)
        gr.SetMarkerColor(color_dict[pname])
        gr.SetFillColor(color_dict[pname])
        hist.SetLineWidth(3)

        legend.AddEntry(gr, pname, "pl")

        if i_hist == 0:
            gr.SetTitle("{} efficiencies".format(channel))
            gr.Draw("APL")
        else:
            gr.Draw("PL")

        graphs.append(gr)
    legend.Draw()

    ROOT.gSystem.Run()

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
