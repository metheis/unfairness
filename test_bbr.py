#!/usr/bin/env python3

"""
Usage:
./test_bbr.py <NUM_ITERATIONS> <NUM_FLOWS> <LONG_FLOW_LATENCY> <SHORT_FLOW_LATENCY>
"""

import subprocess, threading, time, sys, os, parse

# Global Parameters
MAHIMAHI_BASE = '100.64.0.1'
LOG_DIR_BASE='logs-'
CCA = 'bbr'
RUN_TIMELENGTH = 120
UPLOAD_FILE = 'const-120mbit'
DOWNLOAD_FILE = 'const-12mbit'

def thread_call(command):
    subprocess.run(command)

def spawn_flow(long_latency, short_latency, num):
    command = ['mm-delay', str(long_latency), 'mm-link', UPLOAD_FILE, DOWNLOAD_FILE, '--', \
        './bbr.sh', str(num), str(short_latency), str(RUN_TIMELENGTH)]
    t = threading.Timer(0, thread_call, kwargs={'command':command})
    t.start()

def main():
    num_iter = int(sys.argv[1])
    num_flows = int(sys.argv[2])
    log_dir = LOG_DIR_BASE + sys.argv[2]
    long_latency = int(sys.argv[3])
    short_latency = int(sys.argv[4])

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # create flows:
    for i in range(num_iter):
        spawn_flow(long_latency, short_latency, num_flows)
        # Wait until flows are done:
        time.sleep(RUN_TIMELENGTH + 0.2*num_flows + 1)

        parse.main(['', str(num_flows)])


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 5:
        print('Usage: ./test_bbr.py <NUM_ITERATIONS> <NUM_FLOWS> <LONG_FLOW_LATENCY> <SHORT_FLOW_LATENCY>')
    else:
        main()
