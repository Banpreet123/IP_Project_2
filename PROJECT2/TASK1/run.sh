#!/bin/bash
 
# declare an array
# arr=("1" "2" "4" "8" "16" "32" "64" "128" "256" "512" "1024")

# for ((j=1; j<=5; j++))
# do
#     for i in "${arr[@]}"
#     do
while true
do 
    python3 ../server.py Simple_ftp_server 7735 output.txt 0.05
    sleep 2
done
