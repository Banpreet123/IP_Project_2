import sys
import socket
import struct
import threading
import time


#recvfrom - Receive a messgae from the socket - Param: CLIENT_BUFFER - Points to the CLIENT_BUFFER where the message should be stored.
def ack_function():
    global SERVER_HOST,SERVER_PORT_NUMBER,FILE_NAME,N,MSS,TIMEOUT,CLIENT_BUFFER,current_window,transmission_lock,client_socket,file_read
    while True:
        if file_read and not current_window:
            break
        (ack, server_address) = client_socket.recvfrom(CLIENT_BUFFER)
        header = struct.unpack('!LHH', ack[0:8])
        if header[1] != 0b0000000000000000:
            print("CHECKSUM ALERT! There is some Error!")
            continue
        if header[2] != 0b1010101010101010:
            print("DATA PKT ALERT! There is some Error!")
            continue
        sequence_number = header[0]
        transmission_lock.acquire()
        for i in range(len(current_window)):
            if current_window[i][0] == sequence_number:
                current_window = current_window[i+1:]
                break
        transmission_lock.release()

#rdt_send() handles the initial packet sending till the receipt of the acknowledgement from the receiver or current window is full
def rdt_send():
    global SERVER_HOST,SERVER_PORT_NUMBER,FILE_NAME,N,MSS,TIMEOUT,CLIENT_BUFFER,current_window,transmission_lock,client_socket,file_read
    current_file = open(FILE_NAME, "r")
    sequence_number = 0
    while True:
        while len(current_window) >= N:
            time.sleep(0.1)
        #print("sequence_number"+str(sequence_number))
        if file_read == True:
            header = struct.pack('!LHH', sequence_number, checksum(''), 0b0101010101010101)         #in bytes
            transmission_lock.acquire()
            current_window.append([sequence_number,header,time.time()])
            transmission_lock.release() 
            client_socket.sendto(header, (SERVER_HOST, SERVER_PORT_NUMBER))                        #accepts bytes
            break
        data_read = ''
        while MSS >len(data_read):
            input_data_byte = current_file.read(1)
            if not input_data_byte:
                file_read = True
                current_file.close()
                break
            data_read = data_read + input_data_byte
        if len(data_read)>0:
            header = struct.pack('!LHH', sequence_number,   checksum(data_read), 0b0101010101010101)
            packet_to_transfer = header+str(data_read).encode()                                             # to convert in bytes
            transmission_lock.acquire()
            current_window.append([sequence_number,packet_to_transfer,time.time()])
            transmission_lock.release()
            client_socket.sendto(packet_to_transfer, (SERVER_HOST, SERVER_PORT_NUMBER))
            sequence_number=sequence_number+1

def checkTimeout():
    global SERVER_HOST,SERVER_PORT_NUMBER,FILE_NAME,N,MSS,TIMEOUT,CLIENT_BUFFER,current_window,transmission_lock,client_socket,file_read
    if len(current_window)>0:
        if (time.time() - current_window[0][2]) > TIMEOUT:
            return True
        else:
            return False
    return False

def retransmit_packet():
    global SERVER_HOST,SERVER_PORT_NUMBER,FILE_NAME,N,MSS,TIMEOUT,CLIENT_BUFFER,current_window,transmission_lock,client_socket,file_read
    transmission_lock.acquire()
    for i in range(len(current_window)):
        current_window[i][2] = time.time()
        client_socket.sendto(current_window[i][1], (SERVER_HOST, SERVER_PORT_NUMBER))
    transmission_lock.release()


def retransmission(transmit_thread,ack_thread):
    global SERVER_HOST,SERVER_PORT_NUMBER,FILE_NAME,N,MSS,TIMEOUT,CLIENT_BUFFER,current_window,transmission_lock,client_socket,file_read
    while True:
        if transmit_thread.is_alive() or ack_thread.is_alive():
            time.sleep(TIMEOUT)
            if checkTimeout():
                print("Timeout, sequence number = " +str(current_window[0][0])+" ~ Retransmitting")
                retransmit_packet()
        elif not transmit_thread.is_alive() and not ack_thread.is_alive():
            break

#Referance for checksum :- https://stackoverflow.com/questions/1767910/checksum-udp-calculation-python
#https://github.com/houluy/UDP/blob/master/udp.py
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

# RLock: reentrant lock objects
# AF_INET: address family - specify the address types that can be used - host and port number
# SOCK_DGRAM: datagram-based protocol, send 1, get 1, connection ends - for UDP
if __name__=="__main__":

    global SERVER_HOST,SERVER_PORT_NUMBER,FILE_NAME,N,MSS,TIMEOUT,CLIENT_BUFFER,current_window,transmission_lock,client_socket,file_read

    SERVER_HOST = sys.argv[2]
    SERVER_PORT_NUMBER = int(sys.argv[3])
    FILE_NAME = str(sys.argv[4])
    N = int(sys.argv[5])
    MSS = int(sys.argv[6])
    TIMEOUT = 1
    CLIENT_BUFFER = 4096
    current_window = []
    transmission_lock = threading.RLock()
    file_read = False
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    transmit_thread = threading.Thread(target=rdt_send)
    ack_thread = threading.Thread(target=ack_function)
    retransmit_thread = threading.Thread(target=retransmission,args=(transmit_thread,ack_thread,))
  
    start_time = time.time()
    ack_thread.start()
    transmit_thread.start()
    retransmit_thread.start()
  
    retransmit_thread.join()
    transmit_thread.join()
    ack_thread.join()

    print("Final Data Transfer time:  ", time.time()-start_time)
    
    #close the socket
    client_socket.close()