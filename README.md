# SFTP - Simple File Trasfer Protocol implementation of Go-Back-N 
## Steps to run:

1. Clone the repository

2. Make sure the system has python3 installed

3. Go to the root directory of the folder in the terminal 

4. First run the SERVER file. To run, use the following command
     	Command:    python3 server.py Simple_ftp_server #SERVER_PORT #FILE_NAME #P_VALUE
      
where #ABC means a command line argument
      
5. For running the CLIENT, run "client.py" using following command
		Command:    python3 client.py Simple_ftp_client #SERVER_IP #SERVER_PORT #FILE_NAME #N_VALUE #MSS_VALUE
    
where #ABC means a command line argument

6. The file will be downloaded in the same directory as server.py

## Connection to VCL:

1. Reserve and connect to a VCL NCSU's EOS server instance 'CentOS 7 Base (64 bit VM)'

2. Run 'sudo iptables -I INPUT -p udp -s 0.0.0.0/0 --dport 7735 -j ACCEPT'

3. For ufw installation, run 'sudo yum install -y ufw'

4. Allow port on ufw, run 'sudo ufw allow 7735'

5. Run 'sudo ufw reload' 

6. Install Python on VCL, run 'yum install -y python3'

## Steps to run TASK 1, 2 and 3:

1. To run the client:
	* Run the shell script using command
		Command: sh run_client.sh
2. To run the server
	* Run the shell script using command
		Command: sh run.sh
