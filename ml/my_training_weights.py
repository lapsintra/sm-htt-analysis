#!/usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import argparse
import os
import yaml

import logging
logger = logging.getLogger("write_dataset_config")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Sum training weights of classes in training dataset.")
    parser.add_argument("dataset", type=str, help="Training dataset.")
    parser.add_argument(
        "--train-config", required=True, help="Training config file")
    parser.add_argument(
        "--classes-config", required=True, help="Classes mapping config file")
    parser.add_argument(
        "--weight-branch",
        default="training_weight",
        type=str,
        help="Branch with weights.")
    return parser.parse_args()


def parse_config(filename):
    logger.debug("Load YAML config: {}".format(filename))
    return yaml.load(open(filename, "r"))


def main(args, train_config, classes_config):
    print(classes_config)
    classes = list(set(classes_config.values()))


    logger.info("Process training dataset %s.", args.dataset)
    f = ROOT.TFile(args.dataset)
    counts = {}
    sum_all = 0.0
    for name in classes:
        logger.debug("Process class %s.", name)
        sum_ = 0.0
        tree = f.Get(name)
        if tree == None:
            logger.fatal("Tree %s does not exist in file.", name)
            raise Exception
        for event in tree:
            sum_ += getattr(event, args.weight_branch)
        sum_all += sum_
        counts[name] = sum_

    train_config["classes"] = classes
    train_config["class_weights"] = {c: sum_all/counts[c] for c in classes}


    # Write output config
    logger.info("Write config to file: {}".format(args.train_config))
    with open(args.train_config, "w") as stream:
        yaml.dump(
            train_config, stream, default_flow_style=False)


    for name in classes:
        logger.info(
            "Class {} (sum, fraction, inverse): {:g}, {:g}, {:g}".format(
                name, counts[name], counts[name] / sum_all, sum_all / counts[name]))


if __name__ == "__main__":
    args = parse_arguments()
    classes_config = parse_config(args.classes_config)
    train_config = parse_config(args.train_config)
    main(args, train_config, classes_config)
