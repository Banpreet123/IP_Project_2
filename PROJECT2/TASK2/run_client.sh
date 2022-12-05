#!/bin/bash
 
# declare an array
arr=("100" "200" "300" "400" "500" "600" "700" "800" "900" "1000")


for i in "${arr[@]}"
do

    for ((j=1; j<=5; j++))
    do
        # python3 client.py Simple_ftp_server 127.0.0.1 7735 abc.txt $i 500
        python3 ../client.py Simple_ftp_server 152.7.177.209 7735 test.txt 64 ${i}
        echo "${j} =========== ${i}"
        sleep 5
    done

done