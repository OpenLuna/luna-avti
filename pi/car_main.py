import car_control as cc
import car_network as cn
import picamera
import urlparse
import httplib
import urllib
import time
import sys
import os
import io

from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.internet import reactor
from twisted.internet import task
from multiprocessing import Process

def applyCommands(up, down, left, right):
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
    
    print "Got state UP:", up, "DOWN:", down, "LEFT:", left, "RIGHT:", right

#read config from file
def loadConfig(fileName = None):
    config = {}
    lineNo = 0
    if fileName == None:
        fileName = os.path.dirname(os.path.realpath(__file__)) + "/car.config"
    
    with open(fileName) as f:
        for line in f:
            lineNo += 1
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            line = line.split(":")
            if len(line) != 2:
                raise Exception("Error reading config on line " + str(lineNo))
            key = line[0].strip().lower()
            value = line[1].strip()
            if not key or not value:
                raise Exception("Error reading config on line " + str(lineNo))
            config[key] = value
    return config

#print any dict in form:
#header
#  key1: value1
#  key2: value2 ...
def printDict(header, d):
    print "\n", header
    for k in d:
        print "  " + str(k) + ": " + str(d[k])
    print

#check if car has network connection by getting local IP
def hasNetworkConnection():
    if cn.getLocalIP() == "":
        print "No network connection"
        control.stopMotors()
        control.LED("red", True)
        time.sleep(0.5)
        control.LED("red", False)
        return False
    return True

class WebsocketClient(WebSocketClientProtocol):
    def __init__(self):
        self.pingTask = task.LoopingCall(self.ping)
        self.gotPong = True
    
    def onOpen(self):
        print "Websocket connection opened"
        print "Car is ready for driving"
        control.LED("green", True)
        self.sendMessage(urllib.urlencode({"token": config["secret key"], "name": config["name"]}))
        self.pingTask.start(float(config["ping interval"]))
    
    def onMessage(self, payload, isBinary):
        try:
            request = urlparse.parse_qs(payload)
            applyCommands(request["up"][0].lower(), request["down"][0].lower(), request["left"][0].lower(), request["right"][0].lower())
        except KeyError:
            control.stopMotors()
            print "invalid commands"
        
    def onClose(self, wasClean, code, reason):
        print "Connection closed with code:", code, "and reason:", reason
        try:
            control.stopMotors()
            self.pingTask.stop()
            reactor.connectTCP(config["server ip"], int(config["ws port"]), factory)
        except:
            pass
    
    def ping(self):
        if self.gotPong:
            self.sendPing()
            self.gotPong = False
        else:
            print "Did not get PONG... closing connection"
            control.stopMotors()
            self.sendClose()
    
    def onPong(self, payload):
        self.gotPong = True

def streaming():
    camera = picamera.PiCamera()
    camera.resolution = (400, 300)
    camera.framerate = 60
    stream = io.BytesIO()
    cnt = 0
    print "Streaming started"
    try:
        conn = httplib.HTTPConnection(config["server ip"], int(config["stream port"]))
        #conn.set_debuglevel(1)
        conn.putrequest("GET", "/streamreg?" + urllib.urlencode({"token": config["secret key"], "name": config["name"]}))
        conn.putheader("Content-Length", "4000000000000")
        conn.endheaders()
        
        start=time.time()
        for image in camera.capture_continuous(stream, format='jpeg', use_video_port=True, quality = 20):
            conn.send("--jpgboundary\n")
            conn.send("Content-type: image/jpeg\n")
            conn.send("Content-length: " + str(stream.tell()) + "\n\n")
            conn.send(stream.getvalue())
            stream.seek(0)
            stream.truncate()
            cnt += 1
            FPS =   ("%.2f" % (cnt / (time.time() - start))) + " FPS"
            camera.annotate_text = FPS
            #print FPS
    except Exception as e:
        print "Streaming finished", e
        camera.close()
        conn.close()

#****MAIN****#
print "Process nicesness", os.nice(-20)

#read default config file (car.config) or the one provided as program argument
config = loadConfig(sys.argv[2]) if len(sys.argv) > 2 else loadConfig()
printDict("Config:", config)

#initialize car control
control = cc.Control()

while not hasNetworkConnection():
    time.sleep(1)

#connect websocket
factory = WebSocketClientFactory(debug = False)
factory.protocol = WebsocketClient
reactor.connectTCP(config["server ip"], int(config["ws port"]), factory)
task.LoopingCall(hasNetworkConnection).start(1)

runStreaming = True
if len(sys.argv) > 1:
    runStreaming = sys.argv[1].lower() == "true"
if runStreaming:
    streamProcess = Process(target = streaming)
    streamProcess.daemon = True
    streamProcess.start()

reactor.run()

