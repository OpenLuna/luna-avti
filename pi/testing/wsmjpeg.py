import io
import time
import picamera
import httplib
import os
from multiprocessing import Process

def streaming():
    print __name__, os.getpid()
    camera = picamera.PiCamera()
    camera.resolution = (400, 300)
    camera.framerate = 60
    stream = io.BytesIO()
    cnt = 0

    try:
        conn = httplib.HTTPConnection("193.2.177.238", 4114)
        #conn.set_debuglevel(1)
        conn.putrequest("GET", "/")
        conn.putheader("Content-Length", "4000000000")
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
            print FPS
    except:
        camera.close()
        conn.close()
  
print __name__, os.getpid()
p = Process(target = streaming)
p.daemon = True
p.start()
p.join()
    

