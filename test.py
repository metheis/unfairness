#!/usr/bin/env python3

"""
Usage:
./test.py <NUM_ITERATIONS> <NUM_FLOWS> <LONG_FLOW_LATENCY> <SHORT_FLOW_LATENCY> <CCA>
"""

import subprocess, threading, time, sys, os, parse

# Global Parameters
MAHIMAHI_BASE = '100.64.0.1'
LOG_DIR_BASE='logs-'
RUN_TIMELENGTH = 120
UPLOAD_FILE = 'const-120mbit'
DOWNLOAD_FILE = 'const-12mbit'

def thread_call(command):
    subprocess.run(command)

def spawn_flow(long_latency, short_latency, num, cca, exp_type):
    command = ['mm-delay', str(long_latency), 'mm-link', UPLOAD_FILE, DOWNLOAD_FILE, '--', \
        './iperf_spawner.sh', str(num), str(short_latency), str(RUN_TIMELENGTH), cca, exp_type]
    t = threading.Timer(0, thread_call, kwargs={'command':command})
    t.start()

def main(args):
    num_iter = int(args[1])
    num_flows = int(args[2])
    long_latency = int(args[3])
    short_latency = int(args[4])
    cca = args[5]
    exp_type = args[6]
    if 'num' in exp_type:
        exp_index = args[2]
    elif 'lat' in exp_type:
        exp_index = args[4]
    else:
        print('Unsupported experiment type.')
        exit(0)
    log_dir = exp_type + '/' + cca + '/' + LOG_DIR_BASE + exp_index

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # create flows:
    for i in range(num_iter):
        spawn_flow(long_latency, short_latency, num_flows, cca, exp_type)
        # Wait until flows are done:
        time.sleep(RUN_TIMELENGTH + 0.2*num_flows + 1)

        parse.main(['', exp_type, exp_index, cca])


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 7:
        print('Usage: ./test.py <NUM_ITERATIONS> <NUM_FLOWS> <LONG_FLOW_LATENCY> <SHORT_FLOW_LATENCY> <CCA> <EXP_TYPE>')
    else:
        main(args)