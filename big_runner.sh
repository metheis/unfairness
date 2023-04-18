#!/bin/bash

# Declare an array with the elements
elements=(2 3 4 5 10 15 20 50 100)

n=$1
cca=$2
# Loop through the array and echo each element
for element in "${elements[@]}"; do
  python3 ./test_bbr.py $n $element 20 20 $cca
done
