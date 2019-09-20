#!/usr/bin/env python
import socket as sk
import json
import time

HOST = '10.22.14.254'
PORT = 12345
WAGON_SIZE = 1

s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
s.bind((HOST, PORT))

passengerQueue = []
wagonQueue = []


def addPassenger(address):  # add an IP + port to our passenger queue
    passengerQueue.append(address)
    s.sendto("You entered the passenger queue".encode(), address)
    print("Added the user to the passenger queue, we have ", str(len(passengerQueue)), " passengers in queue")


def addWagon(address):  # add an ip + port to our wagon queue
    wagonQueue.append(address)
    s.sendto("You entered the wagon queue".encode(), address)
    print("Added the user to the wagon queue, we have ", str(len(wagonQueue)), " wagons in queue")


def checkAvailableRide():  # check if we have a wagon and enough passengers for it, send away the wagon with the passengers
    # do we have a wagon and enough people for it?
    print("Checking if there is a wagon and enough passengers for it")
    if ((len(passengerQueue) >= WAGON_SIZE) and (len(wagonQueue) >= 1)):
        currentWagon = wagonQueue.pop(0)  # pop wagon from queue
        currentWagon = currentWagon[0]  # retrieve ip from tuple
        tcp_socket_wagon = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        tcp_socket_wagon.connect((currentWagon, 1337))  # open TCP connection with wagon

        print("Found enough passengers and a wagon, now messaging the passengers and the wagon")
        passengerListForWagon = []
        for i in range(WAGON_SIZE):  # tell each passenger the wagon ip, and tell wagon each passenger ip
            currentPassenger = passengerQueue.pop(0)  # pop passenger from queue

            currentPassengerIP = currentPassenger[0]  # retrieve ip from tuple
            passengerListForWagon.append(currentPassengerIP)
            s.sendto(('This is the ip of your wagon,' + str(currentWagon)).encode(), currentPassenger)
            print("Passenger number ", str(i + 1), " is now informed.")


        jsonData = json.dumps(passengerListForWagon)
        tcp_socket_wagon.send((jsonData).encode())
        print("The wagon is now informed about all passengers.")

        tcp_socket_wagon.close()
        print("The ride is now planned!")
    else:
        print("There is currently not enough passengers or wagons in queue..")


def sendAnotherPassenger(address):
    newPassenger = passengerQueue.pop(0)  # pop first passenger in queue
    s.sendto(newPassenger[0].encode(), address)
    print("Sent a new passenger to wagon with disconnected passenger.")


def handleClientMessage(msg, address):
    # if-else statement to handle the message received
    if (msg == "I want to join passenger queue"):
        addPassenger(address)
    elif (msg == "I want to join wagon queue"):
        addWagon(address)
    elif (msg == "I need one more passenger"):
        sendAnotherPassenger(address)


print("Server started!")
while 1:
    payload, client_address = s.recvfrom(65536)
    # data = json.loads(payload.decode())

    print("Received payload: " + payload.decode())
    print("Handling the message..")
    handleClientMessage(payload.decode(), client_address)  # Handle the message received accordingly
    checkAvailableRide()  # check the queues if we can send wagon with passenger
    print("")
