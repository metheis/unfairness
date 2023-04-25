#!/bin/bash

# Declare an array with the elements
elements=(0 1 2 3 4 5 10 15 20 30 40 50 60 70 80)

n=$1
cca=$2
exp_type=$3

if [ "$exp_type" = "num_flows" ]; then
    for element in "${elements[@]}"; do
        python3 ./test.py num_flows $n $element 20 20 $cca 
    done
else
    for element in "${elements[@]}"; do
        python3 ./test.py lat_ratio $n 2 20 $element $cca
    done
fi


