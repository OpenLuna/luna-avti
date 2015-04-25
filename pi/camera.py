import io
import picamera
import time
from PIL import Image
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor
from twisted.internet import task

class WebsocketServer(WebSocketServerProtocol):
    def onConnect(self, request):
        print "Got connection from", request.peer
    
    def onOpen(self):
        print "Connection open"
        self.s = task.LoopingCall(self.skljoc)
        self.s.start(0)
        print "askdajsd"
    
    def onMessage(self, payload, isBinary):
        print "here"
        
    def onClose(self, wasClean, code, reason):
        print "Connection CLOSED"
        self.s.stop()
    
    def skljoc(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 60
            start = 0
            stream = io.BytesIO()
            time.sleep(2)
            for a in camera.capture_continuous(stream, format='jpeg', use_video_port=True, resize = (400, 300)):
                print time.time() - start
                self.sendMessage(stream.getvalue(), True, sync=True)
                stream.seek(0)
                stream.truncate()
                yield
                start=time.time()

IP = "192.168.1.109"
PORT = 12345
from twisted.python import log
import sys
log.startLogging(sys.stdout)

websocketURI = "ws://" + str(IP) + ":" + str(PORT)
print "Openning websocket at", websocketURI
factory = WebSocketServerFactory(websocketURI, debug = False)
factory.protocol = WebsocketServer

reactor.listenTCP(PORT, factory)
reactor.run()
