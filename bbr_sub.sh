#!/bin/bash

cca=bbr
MAHIMAHI_BASE=100.64.0.1
mm-delay 20 sleep $((20 - $(($1 * 0.2f)))) && iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t 120 > ${log_directory}/short-flow-${i}


