#!/bin/bash
# mm-delay 80 mm-link const-480mbit const-120mbit -- bash bbr.sh 5 40 60

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <number_of_logs> <short_lat> <timelength> <cca>"
    exit 1
fi

num_logs=$1
short_lat=$2
cca=$4
MAHIMAHI_BASE=100.64.0.1
log_directory=/home/mark/unfairness/$cca/logs-$1
timelength=$3

# sudo tcpdump -i ingress --snapshot-length 100 -w /home/mark/mahimahi_exp/pktslog &
iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t $timelength > ${log_directory}/flow-1 &
# ping $MAHIMAHI_BASE > /home/mark/mahimahi_exp/pinglog &

for i in $(seq 2 $num_logs); do
#    mm-delay $(( 10*i + 1 )) iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t 120 > ${log_directory}/log-${i} &
    mm-delay $short_lat iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t $timelength > ${log_directory}/flow-${i} &
    sleep 0.2
done

# Wait for all background jobs to finish
wait
