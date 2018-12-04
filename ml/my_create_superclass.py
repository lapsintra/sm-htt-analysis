#!/usr/bin/python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # disable ROOT internal argument parser
ROOT.TFile.__enter__ = lambda self: self
ROOT.TFile.__exit__ = lambda self, type, value, traceback: self.Close()

import argparse
import os
import sys
import yaml


import logging
logger = logging.getLogger("create_training_dataset")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_arguments():
    logger.debug("Parse arguments.")
    parser = argparse.ArgumentParser(description="Create mapped classes training dataset")
    parser.add_argument(
        "--train-config", required=True, help="Training config file")
    parser.add_argument(
        "--classes-config", required=True, help="Classes mapping config file")
    parser.add_argument(
        "--input-config", required=True, help="Input dataset config file")
    parser.add_argument(
        "--output-config", required=True, help="Output dataset config file")
    return parser.parse_args()


def parse_config(filename):
    logger.debug("Load YAML config: {}".format(filename))
    return yaml.load(open(filename, "r"))


def main(args, train_config, classes_config, dataset_config):
    era = sys.argv[1]
    channel = sys.argv[2]

    base_classes = classes_config.keys()
    new_classes = list(set(classes_config.values()))
    bn_map = classes_config
    nb_map = {n: [b for b, n2 in bn_map.iteritems() if n==n2] for n in new_classes}

    branch = train_config["event_weights"]
    sum_classes = dict()

    for _class in base_classes:
        sum_class = 0.

        for dataset in train_config["datasets"]:
            with ROOT.TFile(dataset, "read") as stream:
                tree = stream.Get(_class)
                for event in tree:
                    sum_class += getattr(tree, branch)
        sum_classes[_class] = sum_class

    weight_dict = dict()
    for new_class, base_classes in nb_map.iteritems():
        sum_superclass = 0.
        for class_ in base_classes:
            sum_superclass += sum_classes[class_]
        for class_ in base_classes:
            weight_dict[class_] = sum_superclass/sum_classes[class_]

    for process in dataset_config["processes"].itervalues():
        process["weight_string"] = "({})*({})".format(weight_dict.get(process["class"]), process["weight_string"])
        process["class"] = bn_map.get(process["class"])

    dataset_config["processes"] = {name: proc for name, proc in dataset_config["processes"].iteritems() if proc["class"] is not None}

    ############################################################################

    # Write output config
    logger.info("Write config to file: {}".format(args.output_config))
    yaml.dump(
        dataset_config, open(args.output_config, 'w'), default_flow_style=False)


if __name__ == "__main__":
    args = parse_arguments()
    train_config = parse_config(args.train_config)
    classes_config = parse_config(args.classes_config)
    input_config = parse_config(args.input_config)
    main(args, train_config, classes_config, input_config)
