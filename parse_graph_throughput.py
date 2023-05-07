#!/usr/bin/env python3

"""
Usage:
./graph.py <EXP_TYPE> <CCA>
"""
import sys, os
import matplotlib.pyplot as plt

# Global Parameters
LOG_DIR_BASE='logs-'
IPERF_HEADER_LINE_NUM = 6
IPERF_STARTUP_REJECT = 2
IPERF_ENDING_REJECT = 3

def main(args):
    exp_type = args[1]
    cca_list = args[2:]

    cca_dict = {}

    for cca in cca_list:
        flow_1, flow_2 = load_data(exp_type, cca)
        cca_dict[cca] = [flow_1, flow_2]
    
    make_graph(exp_type, cca_dict)


def load_data(exp_type, cca):
    flow_1_throughput_dict = {}
    flow_2_throughput_dict = {}
    filename_list = os.listdir(exp_type + '/' + cca)
    filename_list.sort(key=lambda a : int(a.split('-')[1]))
    for filename in filename_list:
        d = os.path.join(exp_type, cca, filename)
        if os.path.isdir(d) and 'old' not in filename:
            for log_filename in os.listdir(d):
                if 'summary' not in log_filename:
                    with open(os.path.join(d, log_filename), 'r') as infile:
                        lines = infile.readlines()
                        lines = lines[IPERF_HEADER_LINE_NUM + IPERF_STARTUP_REJECT:]
                        if IPERF_ENDING_REJECT > 0:
                            lines = lines[:-IPERF_ENDING_REJECT]
                        total_mbits = 0
                        total_lines = 0
                        for line in lines:
                            splitline = line.split()
                            unit = splitline[-1]
                            value = splitline[-2]
                            if unit == 'Mbits/sec':
                                total_mbits += float(value)
                            elif unit == 'Kbits/sec':
                                total_mbits += float(value) / 1000
                            elif unit == 'Gbits/sec':
                                total_mbits += float(value) * 1000
                            elif unit == 'bits/sec':
                                total_mbits += float(value) / (1000 * 1000)
                            else:
                                print('Error: unsupported unit: ' + unit)
                            total_lines += 1
                        average_mbits = total_mbits / total_lines
                        split_path = log_filename.split('-')
                        idx = int(split_path[-1])
                        if idx == 1:
                            flow_1_throughput_dict[int(filename.split('-')[-1])] = average_mbits
                        else:
                            flow_2_throughput_dict[int(filename.split('-')[-1])] = average_mbits
    return flow_1_throughput_dict, flow_2_throughput_dict
    
def make_graph(exp_type, cca_dict):
    plt.figure(figsize=(7,5))
    plt.style.use('seaborn-dark-palette')
    plt.ylabel("Throughput (mbps)")
    for cca in cca_dict:
        flow_1 = cca_dict[cca][0]
        flow_2 = cca_dict[cca][1]
        plt.plot([x / 20 + 1 for x in flow_1.keys()], flow_1.values())
        plt.plot([x / 20 + 1 for x in flow_2.keys()], flow_2.values())
    plt.legend(['Flow 1 Throughput', 'Flow 2 Throughput'])
    plt.xlabel("Latency Ratio of Competing Flows")
    plt.title("Throughput vs Flow Latency Ratios for BBR")
    plt.savefig("ratios_experiment_throughput" + ".png", dpi=300)
    


if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 1:
        print('Usage: <EXP_TYPE> <CCA1> <CCA2>...')
    else:
        main(args)
