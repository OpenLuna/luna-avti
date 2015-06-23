#!/usr/bin/python
'''
  A Simple mjpg stream http server for the Raspberry Pi Camera
  inspired by https://gist.github.com/n3wtron/4624820
'''
from websocket import create_connection, ssl
import io
import time
import picamera
import threading
import errno
import socket     

camera=None
streamLock = threading.Lock()
readyImg = False
runThread = True

def capture():
    global readyImg
    start = time.time()
    stream = io.BytesIO()
    for image in camera.capture_continuous(stream, format='jpeg', use_video_port=True, quality = 20):
        streamLock.acquire()
        readyImg = stream.getvalue()
        streamLock.release()
        stream.seek(0)
        stream.truncate()
        if not runThread:
            break
        start = time.time()
    camera.close()

def sendPic(conn):
    start=time.time()
    cnt = 0
    global readyImg
    global runThread
    import struct
    while True:
        if streamLock.acquire(False):
            if readyImg != False:
                #conn.send(struct.pack("!L", len(readyImg)))
                #print len(readyImg)
                conn.send("--jpgboundary\n")
                conn.send("Content-type: image/jpeg\n")
                conn.send("Content-length: " + str(len(readyImg)) + "\n\n")
                conn.send(readyImg)
                camera.annotate_text = ("%.2f" % (cnt / float(time.time() - start))) + "FPS"
                cnt += 1
                print "%.2f" % (cnt / float(time.time() - start)), "FPS"
                readyImg = False
            streamLock.release()

def main():
    global camera
    global runThread
    camera = picamera.PiCamera()
    camera.resolution = (400, 300)
    camera.framerate = 60
    t = threading.Thread(target=capture)
    t.setDaemon(True)
    t.start()
  
    try:
        import httplib
        conn = httplib.HTTPConnection("193.2.177.238", 4114)
        #conn.set_debuglevel(1)
        conn.putrequest("GET", "/")
        conn.putheader("Content-Length", "4000000000")
        conn.endheaders()
        sendPic(conn)
    except KeyboardInterrupt:
        streamLock.acquire(False)
        streamLock.release()
        runThread = False
        conn.close()

if __name__ == '__main__':
  main()
