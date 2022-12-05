#!/bin/bash
 
# declare an array

# for loop that iterates over each element in arr
while true
do
    python3 ../client.py Simple_ftp_server 152.7.177.210 7735 test.txt 64 500
    sleep 5
done