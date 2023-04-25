#!/bin/bash
# mm-delay 80 mm-link const-480mbit const-120mbit -- bash bbr.sh 5 40 60 cubic num_flows 

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <number_of_logs> <short_lat> <timelength> <cca> <exp_type>"
    exit 1
fi

num_logs=$1
short_lat=$2
cca=$4
exp_type=$5
MAHIMAHI_BASE=100.64.0.1
if [ "$exp_type" = "multi_flow" ]; then
    log_directory=/home/mark/unfairness/$exp_type/$cca/logs-$num_logs
else
    log_directory=/home/mark/unfairness/$exp_type/$cca/logs-$short_lat
fi
timelength=$3

# sudo tcpdump -i ingress --snapshot-length 100 -w /home/mark/mahimahi_exp/pktslog &
iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t $timelength > ${log_directory}/flow-1 &
# ping $MAHIMAHI_BASE > /home/mark/mahimahi_exp/pinglog &

# if [ "$cca" = "bbr" ]; then
#     mm-delay $short_lat iperf -c $MAHIMAHI_BASE --linux-congestion cubic -i 1 -t $timelength > ${log_directory}/flow-0 &
#     sleep 0.2
# else
#     mm-delay $short_lat iperf -c $MAHIMAHI_BASE --linux-congestion bbr -i 1 -t $timelength > ${log_directory}/flow-0 &
#     sleep 0.2
# fi

iperf -c $MAHIMAHI_BASE --linux-congestion cubic -i 1 -t $timelength > ${log_directory}/flow-0 &


for i in $(seq 2 $num_logs); do
#    mm-delay $(( 10*i + 1 )) iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t 120 > ${log_directory}/log-${i} &
    mm-delay $short_lat iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t $timelength > ${log_directory}/flow-${i} &
    sleep 0.2
done

# Wait for all background jobs to finish
wait
