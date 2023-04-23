#!/usr/bin/env python3

"""
Usage:
./graph.py <EXP_TYPE> <CCA>
"""
import sys, os
import matplotlib.pyplot as plt

def main(args):
    exp_type = args[1]
    cca_list = args[2:]

    cca_dict = {}

    for cca in cca_list:
        cca_dict[cca] = load_data(exp_type, cca)
    
    make_graph(exp_type, cca_dict)


def load_data(exp_type, cca):
    fairness_dict = {}
    filename_list = os.listdir(exp_type + '/' + cca)
    filename_list.sort(key=lambda a : int(a.split('-')[1]))
    for filename in filename_list:
        d = os.path.join(exp_type, cca, filename)
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
    
def make_graph(exp_type, cca_dict):
    plt.figure(figsize=(7,5))
    plt.style.use('seaborn-dark-palette')
    plt.ylabel("Jain's Fairness Index")
    if 'num' in exp_type:
        for cca in cca_dict:
            plt.plot(cca_dict[cca].keys(), cca_dict[cca].values())
        plt.legend(cca_dict.keys())
        plt.xlabel("Number of Competing Flows")
        plt.title("CCA Fairness vs Number of Flows")
        plt.savefig("num_flows_experiment" + ".png", dpi=300)
    elif 'ratio' in exp_type:
        for cca in cca_dict:
            plt.plot([x / 20 + 1 for x in cca_dict[cca].keys()], cca_dict[cca].values())
        plt.legend(cca_dict.keys(), loc='lower right')
        plt.xlabel("Latency Ratio of Competing Flows")
        plt.title("CCA Fairness vs Flow Latency Ratios")
        plt.savefig("ratios_experiment" + ".png", dpi=300)
    


if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 1:
        print('Usage: <EXP_TYPE> <CCA1> <CCA2>...')
    else:
        main(args)
