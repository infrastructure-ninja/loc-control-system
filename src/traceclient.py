#!/usr/bin/python3

import json
import socket


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('', 31337)
print('\n\nListening on port {}..'.format(server_address[1]))
sock.bind(server_address)

print('Waiting to receive trace messages..\n')

incoming_message_dictionary = None
incoming_message = None

try:
    while True:
        data, address = sock.recvfrom(4096)

        #print('received {} bytes from {}'.format(len(data), address))
        try:
            incoming_message_dictionary = None
            incoming_message_dictionary = json.loads(data.decode())

        except:
            incoming_message = None
            incoming_message = data.decode()

        if incoming_message_dictionary:
            print('[{}] [{}]'.format(
                incoming_message_dictionary['function'],
                incoming_message_dictionary['message'])
            )

        else:
            print(incoming_message)

    #if data:
    #    sent = sock.sendto(data, address)
    #    print('sent {} bytes back to {}'.format(
    #        sent, address)
except KeyboardInterrupt:
    print('\nExiting..\n\n')
