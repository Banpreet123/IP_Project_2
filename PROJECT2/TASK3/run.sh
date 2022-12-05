#!/bin/bash
 
# declare an array
arr=("0.01" "0.02" "0.03" "0.04" "0.05" "0.06" "0.07" "0.08" "0.09" "0.10")

for i in "${arr[@]}"
do

    for ((j=1; j<=5; j++))
    do
        python3 ../server.py Simple_ftp_server 7735 output.txt $i
        echo "${j} =========== ${i}"
        sleep 2
    done

done