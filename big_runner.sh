#!/bin/bash

# Declare an array with the elements
elements=(1 2 3 4 5 10 15 20 40)

n=$1
cca=$2
exp_type=$3

if [ "$exp_type" = "num_flows" ]; then
    for element in "${elements[@]}"; do
        python3 ./test.py $n $element 20 20 $cca num_flows
    done
else
    for element in "${elements[@]}"; do
        python3 ./test.py $n 2 20 $element $cca lat_ratio
    done
fi


