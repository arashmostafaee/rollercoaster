#!/usr/bin/env python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
srvadr = ('10.22.14.254', 12345)
lapsDoneOnRollerCoaster = 0

def waitForWagonFromServer():
    print("Waiting for a message from the server about an available wagon")
    socketMsg, socketAddress = sock.recvfrom(1024)
    print(socketMsg)
    msgParts = socketMsg.decode().split(',')

    if msgParts[0] == "This is the ip of your wagon":
        print("Received message from the server about an available wagon")
        return msgParts[1]
    return ""


def waitForWagonResponse(wagonIP):
    wagonSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    wagonSocket.bind(('', 4321))
    socketMsg, socketAddress = wagonSocket.recvfrom(1024)
    waitUntilTime = time.time() + 3 # wait 3 seconds else wagon is faulty
    while True:

        print(socketMsg)
        if socketAddress == wagonIP or 1 == 1:
            if socketMsg.decode() == "Hello are you ready for a ride with me?":
                print("Received message from the available wagon! Sending a response to receive time of arrival.")
                sock.sendto("I am ready for a ride with you".encode(), socketAddress)

                socketMsg2, socketAddress = wagonSocket.recvfrom(1024)
                socketMsg2 = socketMsg2.decode().split(',')
                print("Time of arrival message received lets go for a ride...")
                if socketMsg2[0] == "The ride has started and will arrive at time":
                    print("Wagon told us the ride is soon starting!")
                    return socketMsg[1]
                if time.time() > waitUntilTime:
                    return -1
    #return -1

def startRide(rideFinishTime):
    print("We are starting the ride weeeeeeeeeeeeeeeeeeeeeeeeeeee!")
    while rideFinishTime - time.time() > 0: continue

while True:
    sock.sendto('I want to join passenger queue'.encode(), srvadr)
    serverResponse, serverAddress = sock.recvfrom(1024)
    print(serverResponse)

    if serverResponse.decode() == "You entered the passenger queue":
        print("We have entered the queue for the rollercoaster")
        wagonToRide = waitForWagonFromServer()
        rideFinishTime = waitForWagonResponse(wagonToRide)
        if rideFinishTime > 0:
            startRide(rideFinishTime)
            lapsDoneOnRollerCoaster += 1
            print("I did another lap on the rollercoaster, we have now done ", str(lapsDoneOnRollerCoaster) , " laps.")
        else:
            print("ERROR! Something went wrong with the wagon, waited too long for it to start")









