srvadr = ('130.243.104.236', 12345)  # Server address and port
WAGON_SIZE = 1  # Amount of passenger seats in the wagon
TRACK_LAP_TIME = 5  # Time for one lap with the wagon in seconds
PASSENGER_PORT = 4321 # which port will the wagon and passenger use
RANDOM_DELAY_TIME = (1,2) #random delay time between a & b seconds

#############################################
######## DO NOT EDIT BELOW THIS LINE ########
#############################################

import socket
import time
import json
import random


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5)
readyPassengerList = []
lapsDoneOnRollerCoaster = 0


def randomDelay():
    waitTime = random.randrange(RANDOM_DELAY_TIME[0], RANDOM_DELAY_TIME[1])
    time.sleep(waitTime)


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

    listOfPassengers = json.loads(passengerListMessage.decode()) #json from server which is a list of passengers
    TCP_socket.close()
    randomDelay()
    return listOfPassengers

def readyCheckPassengers(passengers):
    readyPassengers = []
    print("Checking if every passenger is ready for the ride.")
    while len(passengers) > 0:
        passenger = passengers[0]
        for i in range(0,3):
            try:
                sock.sendto("Hello are you ready for a ride with me?".encode(), (passenger,PASSENGER_PORT))
                print("Checking if a passenger is ready")
            except socket.error as e:
                print("Failed to send ready check to passenger: ", e)
                
            try:
                    passengerResponse, addr = sock.recvfrom(1024)
            except socket.error as e:
                print("Got error from receiving ready check: ", e)
                #passengers.remove(passenger)
            else:
                print("Got a message from him")
                if passengerResponse.decode() == "I am ready for a ride with you":
                    print("A passenger is ready!")
                    #passengers.remove(passenger)
                    readyPassengers.append(passenger)
                    break
        passengers.remove(passenger)
    print("Ready check is done!")
    randomDelay()
    return readyPassengers


def startRide(rideStartTime, listOfPassengers):
    msgToPassengers = ("The ride has started and will arrive at time," + str(rideStartTime + TRACK_LAP_TIME)).encode()
    print("Going to start the ride soon!")
    readyPassengerList = listOfPassengers
    print("this is the passenger list:")
    print(readyPassengerList)
    if len(readyPassengerList) > 0:
        #time.sleep(1)
        for readyPassenger in readyPassengerList:  # tell each passenger what time we will arrive
            print("This is receiver of finish time:")
            print((readyPassenger[0],PASSENGER_PORT))
            sock.sendto(msgToPassengers, (readyPassenger,PASSENGER_PORT))
        print("Ride has started!")
        print("wiii", end='')
        while time.time() - rideStartTime < TRACK_LAP_TIME: # wait until lap time has passed
            print("i", end='')
            time.sleep(0.1)
        print("")
        return 1
    else:
        print("Ready passenger list failed...")
    randomDelay()
    return 0


while True:
    sock.sendto('I want to join wagon queue'.encode(), srvadr)
    try:
        serverResponse, addr = sock.recvfrom(1024)
    except socket.error as e:
        print("Error from socket: " + e)
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
    print("")

