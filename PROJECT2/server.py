import socket
import os
import threading
import struct
import sys
import random

BUFFER_SIZE = 4096
def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    if len(msg)%2 == 1:
        msg+='0'
    #print(msg)
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

def ack_connection(server_socket,FILE_NAME,PACKET_LOSS_PROB):
    output_file = open(FILE_NAME, "w")
    expected_seq_no = 0
    file_received = False
    while file_received == False:
        (client_data, client_address) = server_socket.recvfrom(BUFFER_SIZE)
        header = struct.unpack('!LHH', client_data[0:8])
        data = str(client_data[8:].decode())
        sequence_number = header[0]
        if header[2] != 0b0101010101010101 or checksum(data) != header[1]:
            print("ALERT! Error in Checksum or Data packet!")
            continue
        if sequence_number <= expected_seq_no:
            if random.random() > PACKET_LOSS_PROB:
                server_socket.sendto(struct.pack('!LHH', header[0], 0b0000000000000000, 0b1010101010101010), client_address)
                if len(data) > 0 and sequence_number == expected_seq_no:
                    output_file.write(data)
                    expected_seq_no+=1
                elif len(data)==0:
                    output_file.close()
                    server_socket.close()
                    file_received = True
            else:
                print("Packet loss, sequence number = "+str(sequence_number))

# AF_INET: address family - specify the address types that can be used - host and port number
# SOCK_DGRAM: datagram-based protocol, send 1, get 1, connection ends - for UDP
if __name__=="__main__":

    directory = "/Users/banpreetsinghchhabra/Downloads/PROJECT2/"
    FILE_NAME = str(sys.argv[3])
    if os.path.exists(directory +FILE_NAME):
        os.remove(directory +FILE_NAME)
    PACKET_LOSS_PROB = float(sys.argv[4])
    SERVER_PORT = int(sys.argv[2])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    HOST_NAME = '0.0.0.0'
    server_socket.bind((HOST_NAME, SERVER_PORT))
    print("UDP server up and listening")
    ack_thread = threading.Thread(target=ack_connection,args=(server_socket,directory +FILE_NAME,PACKET_LOSS_PROB))
    ack_thread.start()
    ack_thread.join()