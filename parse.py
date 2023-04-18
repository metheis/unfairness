#!/usr/bin/env python3

"""
Usage:
./parse.py <NUM_LOGS>
"""

import threading, time, sys, os

# Global Parameters
LOG_DIR_BASE='logs-'
IPERF_HEADER_LINE_NUM = 6
IPERF_STARTUP_REJECT = 2
IPERF_ENDING_REJECT = 3

def thread_call(path, filename, summary_flows):
    with open(path + '/' + filename, 'r') as infile:
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
        ## if 'long' in filename:
        ##    summary_flows[0] = average_mbits
        ## else:
        split_path = filename.split('-')
        summary_flows[int(split_path[-1])] = average_mbits

def spawn_flow(log_dir, filename, summary_flows):
    t = threading.Thread(group=None, target=thread_call, kwargs={'path':log_dir, 'filename':filename, 'summary_flows':summary_flows})
    t.start()

def jains_fairness_index(bandwidths):
    sum_bandwidths = sum(bandwidths)
    sum_squares_bandwidths = sum(b * b for b in bandwidths)

    if sum_squares_bandwidths == 0:
        return 0.0

    fairness_index = (sum_bandwidths * sum_bandwidths) / (len(bandwidths) * sum_squares_bandwidths)
    return fairness_index

def main(args):
    num_logs = int(args[1])
    log_dir = LOG_DIR_BASE + args[1]
    if not os.path.exists(log_dir):
        print("Those logs don't exist")
    else:
        summary_flows = {}

        # parse flows
        for filename in os.listdir(log_dir):
            if 'summary' not in filename:
                spawn_flow(log_dir, filename, summary_flows)

        # Wait until parsing is done:
        time.sleep(0.2)


        fairness_idx = jains_fairness_index(summary_flows.values())
        print("Fairness: " + str(round(fairness_idx, 3)))

        # Print summary:
        # long_avg = summary_flows[0]
        # del summary_flows[0]
        # short_avg = sum(summary_flows.values())/len(summary_flows)
        # print('Long: ' + str(round(long_avg, 3)) + ', Short: ' + str(round(short_avg, 3)) + ', Ratio: ' + str(round(long_avg/short_avg, 4)))

        # Save summary:
        with open(log_dir + '/summary-' + str(num_logs), 'a+') as summaryfile:
           # summaryfile.write('Long:  ' + str(round(long_avg, 3)) + '\n')
           # summaryfile.write('Short: ' + str(round(short_avg, 3)) + '\n')
           # summaryfile.write('Ratio: ' + str(round(long_avg/short_avg, 4)) + '\n')
           summaryfile.write(f"Fairness {round(fairness_idx, 3)}\n")

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print('Usage: ./parse.py <NUM_LOGS>')
    else:
        main(args)
