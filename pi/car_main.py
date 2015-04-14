import car_control as cc
import car_network as cn
import time
import sys
import os

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

def applyCommands(up, down, left, right):
    print "Got state UP:", up, "DOWN:", down, "LEFT:", left, "RIGHT:", right
    
    #driving
    if up == "on":
        control.drive(control.DRIVE_FORWARD)
    elif down == "on":
        control.drive(control.DRIVE_BACKWARD)
    else:
        control.drive(control.DRIVE_STOP)
    #steering
    if left == "on":
        control.steer(control.STEER_LEFT)
    elif right == "on":
        control.steer(control.STEER_RIGHT)
    else:
        control.steer(control.STEER_STOP)

"""
#sample config file
key: value
#this is comment
key2: value2
"""
def loadConfig(fileName = "car.config"):
    config = {}
    lineNo = 0
    with open(fileName) as f:
        for line in f:
            lineNo += 1
            line = line.strip()
            if not len(line) or line.startswith("#"):
                continue
            line = line.split(":")
            if len(line) != 2:
                print "Error reading config: line " + str(lineNo)
                continue
            key = line[0].strip().lower()
            value = line[1].strip()
            if not key or not value:
                print "Error reading config: line " + str(lineNo)
                continue
            config[key] = value
    print "Config file:"
    for k in config:
        print "\t" + k + ": " + config[k]
    print
    return config

#main
#print "Niceness", os.nice(-15)

if len(sys.argv) > 1: config = loadConfig(sys.argv[1])
else: config = loadConfig()

control = cc.Control()
network = cn.NetworkConnection(config["server ip"])

lastPacketID = -1
IP = ""
PORT = 12345

while True:
    IP = getLocalIP()
    if IP: break
    print "Error getting local IP: check network connection"
    time.sleep(2)
    
config["car ip"] = IP
config["port"] = PORT

print "Advertising car to server (" + config["server ip"] + ")"
while not network.sendGETRequest("/advertise.php", config):
    print "Error executing GET"
    time.sleep(2)

#file for timing program execution
logTimerFile = open("logs/program_timer.log", "a") #EXECUTION TIMING

class WebsocketServer(WebSocketServerProtocol):
    def onConnect(self, request):
        print "Connected", request
    def onOpen(self):
        print "websocket connection open"
    def onMessage(self, payload, isBinary):
        print payload
    def onClose(self, wasClean, code, reason):
        print "websocket closed"


log.startLogging(sys.stdout)

factory = WebSocketServerFactory("ws://" + IP + ":" + PORT, debug = False)
factory.protocol = WebsocketServer

reactor.listenTCP(9000, factory)

control.LED("green", True)
print "Car is ready for driving!\n"

reactor.run()

while True:
    #EXECUTION TIMING - start
    programTimerStart = time.time()
    
    while not network.hasNetworkConnection():
        print "Lost network connection"
        control.stopMotors()
        control.LED("red", True)
        time.sleep(1)
        control.LED("red", False);
        time.sleep(1)
    
    #EXECUTION TIMING - config, logTimerFile
    requests = server.receive(config, logTimerFile)
    
    #test if up, down, left, right appear in requests
    ok = True
    for r in ["up", "down", "left", "right"]:
        if r not in requests:
            ok = False
            break
    if not ok:
        if requests != {}:
            print "Got invalid commands"
        continue
    
    packetID = int(requests["time"])
    if packetID < lastPacketID:
        print "Got late packet with id " + str(packetID)
        #EXECUTION TIMING - stop
        logTimerFile.write(config["name"] + "," + requests["time"] + ",PI-all," + str(time.time() - programTimerStart) + "\n")
        continue
    lastPacketID = packetID
    
    applyCommands(requests["up"], requests["down"], requests["left"], requests["right"]) 
    
    #EXECUTION TIMING - stop
    logTimerFile.write(config["name"] + "," + requests["time"] + ",PI-all," + str(time.time() - programTimerStart) + "\n")
    #logTimerFile.flush()
