# Run this as mm-delay 80 mm-link const-12mbit const-120mbit -- bash bbr_orig.sh
cca=bbr
log_directory="/home/mark/mahimahi_exp/logs_orig"
# sudo tcpdump -i ingress --snapshot-length 100 -w /tmp/pktslog &
iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t 120 >${log_directory}/long-flow &
#ping $MAHIMAHI_BASE > /home/mark/mahimahi_exp/pinglog &
# ./mm-link const-120mbit agg-10ms-120mbit  -- iperf -c 100.64.0.1 --linux-congestion cubic -i 1 -t 60 >/tmp/log2
mm-delay 40 iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t 120 >${log_directory}/short-flow-1 &
sleep 0.1
mm-delay 40 iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t 120 >${log_directory}/short-flow-2 & 
sleep 0.1
mm-delay 40 iperf -c $MAHIMAHI_BASE --linux-congestion $cca -i 1 -t 120 >${log_directory}/short-flow-3  
wait
# Add ./mm-flex discretize 1 10 for jitter if required
