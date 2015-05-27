import car_control as cc
import car_network as cn
import time
import sys
import io
import picamera
import os

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor
from twisted.internet import task

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

#read config from file
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
    return config

def checkNetworkConnection():
    if not cn.getLocalIP():
        print "Lost network connection"
        control.stopMotors()
        control.LED("red", True)
        time.sleep(0.5)
        control.LED("red", False);

class WebsocketServer(WebSocketServerProtocol):
    def __init__(self):
        self.lastPacketID = -1
        self.stream = io.BytesIO()
        self.captureTask = task.LoopingCall(self.capture)

    def onConnect(self, request):
        print "Got connection from", request.peer
    
    def onOpen(self):
        print "Connection open"
        self.captureTask.start(0)
    
    def onMessage(self, payload, isBinary):
        requests = {}
        payload = payload[payload.find("?")+1:]
        for r in payload.split("&"):
            r = r.split("=")
            requests[r[0].lower()] = r[1].lower()
        
        for r in ["up", "down", "left", "right"]:
            if r not in requests:
                print "Got invalid commands"
                return
        
        packetID = int(requests["time"])
        if packetID < self.lastPacketID:
            print "Got late packet with id " + str(packetID)
            return
        self.lastPacketID = packetID
        applyCommands(requests["up"], requests["down"], requests["left"], requests["right"])
        self.sendMessage(requests["time"], False)
        
    def onClose(self, wasClean, code, reason):
        print "Connection CLOSED"
        control.stopMotors()
        self.captureTask.stop()
    
    def capture(self):
        camera.capture(self.stream, format='jpeg', use_video_port=True, quality = 50)
        self.sendMessage(self.stream.getvalue(), True)
        self.stream.seek(0)
        self.stream.truncate()

#****MAIN****#

print "Process nicesness", os.nice(-20)

IP = ""
PORT = 12345

#read default config file (car.config) or the one provided
#as program argument
if len(sys.argv) > 1: config = loadConfig(sys.argv[1])
else: config = loadConfig()

#get local IP
while True:
    IP = cn.getLocalIP()
    if IP: break
    print "Error getting local IP: check network connection"
    time.sleep(2)

config["car ip"] = IP
config["port"] = PORT

control = cc.Control()

#output config
print "Config:"
for k in config:
    print "\t" + str(k) + ": " + str(config[k])
print

#send car info to server
print "Advertising car to server (" + config["server ip"] + ")"
while not cn.sendGETRequest(config["server ip"], "/advertise.php", config):
    print "Error executing GET"
    time.sleep(2)

#configure camera
camera = picamera.PiCamera()
camera.resolution = (200, 150)
camera.framerate = 60

websocketURI = "ws://" + str(IP) + ":" + str(PORT)
print "Openning websocket at", websocketURI
factory = WebSocketServerFactory(websocketURI, debug = False)
factory.protocol = WebsocketServer

reactor.listenTCP(PORT, factory)
task.LoopingCall(checkNetworkConnection).start(1)

control.LED("green", True)
print "Car is ready for driving!\n"

try:
    reactor.run()
finally:
    camera.close()
