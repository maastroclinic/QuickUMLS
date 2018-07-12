'''
    Example of json TCP communication, make sure you have app/quickumls-service.py running on port 9999
'''

import json

import socket

def recvall(sock):
    BUFF_SIZE = 2048
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

TCP_IP = '127.0.0.1'
TCP_PORT = 9999
BUFFER_SIZE = 2048

with open('resources/ignored/report.txt', 'r') as reportfile:
    MESSAGE = reportfile.read()

data = {}
data['text'] = MESSAGE
json_data = json.dumps(data)
json_dataCRLF = json_data+'\r\n'

print("send " + json_data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(json_dataCRLF.encode('utf-8'))

data_response = recvall(s)
s.close()

data_response_obj = {}
data_response_obj['response'] = json.loads(data_response.decode("utf-8"))

print("received data:", data)
with open('resources/ignored/data_result.txt', 'w') as outfile:
    json.dump(data_response_obj, outfile)