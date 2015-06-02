import io
import picamera
import time
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor
from twisted.internet import task

class WebsocketServer(WebSocketServerProtocol):
    def __init__(self):
        self.s = task.LoopingCall(self.skljoc)
    
    def onConnect(self, request):
        print "Got connection from", request.peer
    
    def onOpen(self):
        print "Connection open"
        self.s.start(0)
    
    def onMessage(self, payload, isBinary):
        print "here"
        
    def onClose(self, wasClean, code, reason):
        print "Connection CLOSED"
        self.s.stop()
    
    def skljoc(self):
        start = time.time()
        camera.capture(stream, format='jpeg', use_video_port=True, quality = 50)
        self.sendMessage(stream.getvalue(), True, doNotCompress=True)
        print time.time() - start, stream.tell()
        stream.seek(0)
        stream.truncate()

IP = "192.168.1.109"
PORT = 12345
from twisted.python import log
import sys
log.startLogging(sys.stdout)

try:
    websocketURI = "ws://" + str(IP) + ":" + str(PORT)
    print "Openning websocket at", websocketURI
    factory = WebSocketServerFactory(websocketURI, debug = False)
    factory.protocol = WebsocketServer

    camera = picamera.PiCamera()
    camera.resolution = (200, 150)
    camera.framerate = 60
    stream = io.BytesIO()

    reactor.listenTCP(PORT, factory)
    reactor.run()
finally:
    camera.close()
