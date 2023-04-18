for i in {1..$1}
do
	mm-delay 120 mm-link const-12mbit const-120mbit -- bash bbr.sh 2 &
	sleep 2 
	echo hi
done
