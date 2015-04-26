import socket
import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (400, 300)
    camera.framerate = 24
    
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 8000))
    server_socket.listen(0)
    
    connection = server_socket.accept()[0].makefile("wb")
    connection.write("HTTP/1.1 200 OK\nContent-Type:video/mp4\n\n")
    try:
        camera.start_recording(connection, format="h264", quality=30)
        camera.wait_recording(60)
        camera.stop_recording()
    finally:
        connection.close()
        server_socket.close()
