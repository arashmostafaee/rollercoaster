PASSENGER_PORT = 4321 # which port will the wagon and passenger use
RANDOM_DELAY_TIME = (1,2) # random delay time between a & b seconds
srvadr = ('130.243.104.236', 12345)

#############################################
######## DO NOT EDIT BELOW THIS LINE ########
#############################################


import socket
import time
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lapsDoneOnRollerCoaster = 0
sock.settimeout(10)
wagonSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
wagonSocket.bind(('', 4321))
wagonSocket.settimeout(10)


def randomDelay():
    waitTime = random.randrange(RANDOM_DELAY_TIME[0], RANDOM_DELAY_TIME[1])
    time.sleep(waitTime)

	
def enterPassengerQueue():
    try:
        sock.sendto('I want to join passenger queue'.encode(), srvadr)
    except socket.error as e:
        print("Error from socket: " + str(e))
		
    try:
        serverResponse, serverAddress = sock.recvfrom(1024)
    except socket.error as e:
        print("Error from socket: " + str(e))
    else:
        if serverResponse.decode() == "You entered the passenger queue":
            return True
    return False


def waitForWagonFromServer():
    #print("Waiting for a message from the server about an available wagon")
    try:
        socketMsg, socketAddress = sock.recvfrom(1024)
    except socket.error as e:
        print("Waited too long for wagon, restarting program...")
        #enterPassengerQueue()
        #waitForWagonFromServer()
    else:
        #print(socketMsg)
        msgParts = socketMsg.decode().split(',')

        if msgParts[0] == "This is the ip of your wagon":
            print("Received message from the server about an available wagon, ")
            
            return msgParts[1]
    return ""


def waitForWagonResponse(wagonIP):
    if wagonIP == "": return -1 # if wait for wagon failed
    try:
        socketMsg, socketAddress = wagonSocket.recvfrom(1024)
    except socket.error as e:
        print("Error from socket: " + str(e))
    else:
        waitUntilTime = time.time() + 3 # wait 3 seconds else wagon is faulty
        #while True:
        #print(socketMsg)
        if socketMsg.decode() == "Hello are you ready for a ride with me?":
            #print("Received message from the available wagon! Sending a response to receive time of arrival.")
            #we got stuck here once ....
            try:
                sock.sendto("I am ready for a ride with you".encode(), socketAddress)
            except socket.error as e:
                print("Error sending message to " + str(socketAddress) + "  error: " + e)
            else:
                try:
                    socketMsg2, socketAddress = wagonSocket.recvfrom(1024)
                except socket.error as e:
                    print("Waited too long for wagon, restarting program...")
                else:
                    socketMsg2 = socketMsg2.decode().split(',')
                    #print("Time of arrival message received lets go for a ride...")
                    if socketMsg2[0] == "The ride has started and will arrive at time":
                        print("Wagon told us the ride is soon starting!")
                        return float(socketMsg2[1])
            #if time.time() > waitUntilTime:
                #return -1
    return -1

def i_am_disembarking():
    #print("Me the passenger is disembarking from the wagon and getting in queue again")  
    global lapsDoneOnRollerCoaster
    lapsDoneOnRollerCoaster += 1    
    print("We have arrived at the end of the ride, we have done ", str(lapsDoneOnRollerCoaster) , " laps now!")
    
def startRide(rideFinishTime):
    if rideFinishTime < 0:
        print("Failed to setup ride with wagon....")
        return
    print("We are starting the ride weee", end='')
    #print(rideFinishTime)
    rideFinishTime = time.time() + 5 # we need "new" arrival time since we could wait up to 10 seconds for wagon response...
    while rideFinishTime - time.time() > 0:
        print("e", end='')
        time.sleep(0.1)
    print("")
    try:
        msg, addr = wagonSocket.recvfrom(1024)
    except socket.error as e:
        print("Error from socket: " + str(e))
    else:
        if msg.decode() == "We have arrived":
            i_am_disembarking()
        else:
            print("We should have arrived, but received wrong message")
    
    
   
print("Passenger started!\n")
while True:

    if enterPassengerQueue():
        print("We have entered the queue for the rollercoaster")
        wagonToRide = waitForWagonFromServer()
        randomDelay()
        
        rideFinishTime = waitForWagonResponse(wagonToRide)
        startRide(rideFinishTime)
        randomDelay()
    print("")







