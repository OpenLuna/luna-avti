import socket
import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 24
    
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(0)
    
    connection = server_socket.accept()[0].makefile("wb")
    #print "read:", connection.read(1024)
    connection.write("HTTP/1.1 200 OK\nContent-Type: multipart/x-mixed-replace; boundary=--jpgboundary\n\n")
    
    try:
        print "start recording"
        camera.start_recording(connection, format="mjpeg")
        camera.wait_recording(1)
        camera.stop_recording()
        print "stop recording"
    finally:
        connection.close()
        server_socket.close()
