#!/usr/bin/python
'''
  A Simple mjpg stream http server for the Raspberry Pi Camera
  inspired by https://gist.github.com/n3wtron/4624820
'''
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import io
import time
import picamera
import threading

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

class CamHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path.endswith('.mjpg'):
        self.send_response(200)
        self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
        self.end_headers()
        start=time.time()
        cnt = 0
        global readyImg
        global runThread
        try:
            while True:
                if streamLock.acquire(False):
                    if readyImg != False:
                        self.wfile.write("--jpgboundary")
                        self.send_header('Content-type','image/jpeg')
                        self.send_header('Content-length', len(readyImg))
                        self.end_headers()
                        self.wfile.write(readyImg)
                        camera.annotate_text = ("%.2f" % (cnt / float(time.time() - start))) + "FPS"
                        cnt += 1
                        print "%.2f" % (cnt / float(time.time() - start)), "FPS"
                        readyImg = False
                    streamLock.release()
        except KeyboardInterrupt:
            streamLock.acquire(False)
            streamLock.release()
        """for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True, quality = 30):
          self.wfile.write("--jpgboundary")
          self.send_header('Content-type','image/jpeg')
          self.send_header('Content-length', stream.tell())
          self.end_headers()
          #start = time.time()
          self.wfile.write(stream.getvalue())
          stream.seek(0)
          stream.truncate()
          camera.annotate_text = str(time.time())
          cnt += 1
          print "%.2f" % (cnt / float(time.time() - start)), "FPS"""
    else:
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      self.wfile.write("""<html><head></head><body>
        <img src="/cam.mjpg"/>
      </body></html>""")
      return

def main():
  global camera
  global runThread
  camera = picamera.PiCamera()
  #camera.resolution = (1280, 960)
  camera.resolution = (400, 300)
  camera.framerate = 60
  t = threading.Thread(target=capture)
  t.start()
  try:
    server = HTTPServer(('',8080), CamHandler)
    print "server started"
    server.serve_forever()
  except KeyboardInterrupt:
    runThread = False
    server.socket.close()

if __name__ == '__main__':
  main()
