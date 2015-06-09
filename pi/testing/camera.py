import io
import picamera
import time
import threading
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor
from twisted.internet import task

def capture():
    global readyImg
    print readyImg
    start = time.time()
    for image in camera.capture_continuous(stream, format='jpeg', use_video_port=True, quality = 30):
        #print time.time() - start
        streamLock.acquire()
        readyImg = stream.getvalue()
        streamLock.release()
        stream.seek(0)
        stream.truncate()
        if not runThread:
            break
        start = time.time()
        camera.annotate_text = str(time.time() % 10)

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
        runThread = False
        self.s.stop()
    
    def skljoc(self):
        global readyImg
        if streamLock.acquire(False):
            if readyImg != False:
                self.sendMessage(readyImg, True, doNotCompress=True)
                print len(readyImg)
                readyImg = False
            streamLock.release()
    
        """start = time.time()
        camera.capture(stream, format='jpeg', use_video_port=True, quality = 50)
        self.sendMessage(stream.getvalue(), True, doNotCompress=True)
        print time.time() - start, stream.tell()
        stream.seek(0)
        stream.truncate()"""

IP = "192.168.1.111"
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
    streamLock = threading.Lock()
    runThread = True
    readyImg = False
    t = threading.Thread(target=capture)
    t.start()

    reactor.listenTCP(PORT, factory)
    reactor.run()
finally:
    runThread = False
    t.join()
    camera.close()
