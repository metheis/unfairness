#!/usr/bin/env python3

"""
Usage:
./graph.py <CCA>
"""
import sys, os
import matplotlib.pyplot as plt

def main(args):
    cca_list = args[1:]

    cca_dict = {}

    for cca in cca_list:
        cca_dict[cca] = load_data(cca)
    
    make_graph(cca_dict)


def load_data(cca):
    fairness_dict = {}
    for filename in os.listdir(cca):
        d = os.path.join(cca, filename)
        if os.path.isdir(d) and 'old' not in filename:
            with open(d + '/summary-' + filename.split('-')[1], 'r') as infile:
                lines = infile.readlines()
                total = 0
                count = 0
                for line in lines:
                    splitline = line.split()
                    if len(splitline) == 2:
                        fairness = float(splitline[1])
                        total += fairness
                        count += 1
                avg_fairness = total / count
                fairness_dict[int(filename.split('-')[1])] = avg_fairness
    return fairness_dict
    
def make_graph(cca_dict):
    plt.figure(figsize=(7,5))
    plt.style.use('seaborn-dark-palette')
    for cca in cca_dict:
        plt.plot(cca_dict[cca].keys(), cca_dict[cca].values())
    plt.legend(cca_dict.keys())
    plt.xlabel("Number of Competing Flows")
    plt.ylabel("Jain's Fairness Index")
    plt.title("CCA Fairness vs Number of Flows")
    plt.savefig("num_flows_experiment" + ".png", dpi=300)


if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 1:
        print('Usage: <CCA1> <CCA2>...')
    else:
        main(args)
