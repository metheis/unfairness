# Run this as ./mm-delay 60 ./mm-link const-120mbit const-1.2gbit -- bash pcc.sh
cca=pcc
sudo tcpdump -i ingress --snapshot-length 100 -w /tmp/pktslog &
iperf -c 100.64.0.1 --linux-congestion $cca -i 1 -t 30 >/tmp/log1 &
ping $MAHIMAHI_BASE >/tmp/pinglog &
sleep 5
#./mm-delay 10 ./mm-flex discretize 10 10 iperf -c 100.64.0.1 --linux-congestion $cca -i 1 -t 60 >/tmp/log2
./mm-flex discretize 1 60 iperf -c 100.64.0.1 --linux-congestion $cca -i 1 -t 30 >/tmp/log2
pkill ping

# Runs:
# 98.0 vs 11.1 Mbit/s
# 99.4 vs 9.93 Mbit/s
# 93.7 vs 15.4 Mbit/s
