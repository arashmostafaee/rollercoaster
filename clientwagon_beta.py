#!/usr/bin/env python
import socket
import time
import json

srvadr = ('10.22.14.254', 12345)  # Server address and port
WAGON_SIZE = 1  # Amount of passenger seats in the wagon
TRACK_LAP_TIME = 5  # Time for one lap with the wagon in seconds
PASSENGER_PORT = 4321

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#global passengerList
#passengerList = []
readyPassengerList = []
lapsDoneOnRollerCoaster = 0


def receivePassengersFromServer():
    # receive our passengers with a TCP connection with server
    TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_socket.bind(('', 1337))
    TCP_socket.listen(1)
    # now wait for the server to open the TCP connection and talk with us
    TCP_conn, TCP_servaddr = TCP_socket.accept()
    passengerListMessage = TCP_conn.recv(500)
    print("We received msg from tcp:")
    print(passengerListMessage)
    # receivingPassengers = False

    # with TCP_conn:
    listOfPassengers = json.loads(passengerListMessage.decode())

    print("We have received a list of passengers")
    ##while not receivingPassengers:
    ##print("Connected to server with TCP, waiting for passengers to take on a trip..")
    # while len(passengerList) > 0: #firstMessage.decode() == "I am sending your passengers now, are you ready?":
    # TCP_conn.send("I am ready to receive passengers".encode())
    # newPassenger = TCP_conn.recv(64)
    # newPassenger = passengerList.pop(0)
    # receivingPassengers = True
    # print("We are now receiving the passengers from the server.")
    # while TCP_conn:  # retrieve passengers for the seats
    # if not newPassenger: break
    # passengerList.append(newPassenger)
    # if len(passengerList) >= WAGON_SIZE:
    # TCP_conn.close()
    # newPassenger = TCP_conn.recv(64)
    # print("Receiving done!")
    # else:
    # time.sleep(0.1)
    TCP_socket.close()
    return listOfPassengers

def readyCheckPassengers(passengers):
    #readyPassengerList.clear()
    readyPassengers = []
    # while len(readyPassengerList) < WAGON_SIZE:
    print("Checking if every passenger is ready for the ride.")
    while len(passengers) > 0:
        passenger = passengers[0]
        sock.sendto("Hello are you ready for a ride with me?".encode(), (passenger,PASSENGER_PORT))
        print("Checking if a passenger is ready")
        passengerResponse, addr = sock.recvfrom(1024)
        print("Got a message from him")
        if passengerResponse.decode() == "I am ready for a ride with you":
            print("A passenger is ready!")
            passengers.remove(passenger)
            readyPassengers.append(passenger)
            e = 23
    print("Ready check is done!")
    return readyPassengers


def startRide(rideStartTime, listOfPassengers):
    msgToPassengers = ("The ride has started and will arrive at time," + str(rideStartTime + TRACK_LAP_TIME)).encode()
    print("Going to start the ride soon!")
    readyPassengerList = listOfPassengers
    print("this is the passenger list:")
    print(readyPassengerList)
    if len(readyPassengerList) > 0:
        time.sleep(1)
        for readyPassenger in readyPassengerList:  # tell each passenger what time we will arrive
            print("This is receiver of finish time:")
            print((readyPassenger[0],PASSENGER_PORT))
            sock.sendto(msgToPassengers, (readyPassenger,PASSENGER_PORT))
        print("Ride has started!")
        while time.time() - rideStartTime < TRACK_LAP_TIME: continue  # wait until lap time has passed
        return 1
    else:
        print("Ready passenger list failed...")
    return 0


while True:
    #passengerList.clear()
    sock.sendto('I want to join wagon queue'.encode(), srvadr)
    serverResponse, addr = sock.recvfrom(1024)
    print(serverResponse)

    if serverResponse.decode() == "You entered the wagon queue":
        print("We have entered the queue to receive passengers")
        passengerList = []
        passengerList = receivePassengersFromServer()  # receive the passengers and add them to our list
        readyPassengersList = readyCheckPassengers(passengerList)  # check if the received passengers are ready for the ride
        startedRollerCoaster = startRide(time.time(), readyPassengersList)  # start the ride with the ready passengers
        if startedRollerCoaster == 1:
            lapsDoneOnRollerCoaster += 1
            print("We completed the roller coaster ride, we have now done ", str(lapsDoneOnRollerCoaster),
                  " laps on the track.")

