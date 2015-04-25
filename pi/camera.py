import io
import picamera
import time
from PIL import Image

stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.capture(stream, format='jpeg')

stream.seek(0)
image = Image.open(stream)
image.save("test.jpg")
