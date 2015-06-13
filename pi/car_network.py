import socket
import httplib
import urllib

import fcntl
import os
import struct

#send GET request to IP/path with params
#params = {k1:v2, k2:v2,...} get
#encoded in url (k1=v1&k2=v2&...)
def sendGETRequest(ip, path, params):
    connection = httplib.HTTPConnection(ip, 8080)
    request = path + "?" + urllib.urlencode(params)
    connection.request("GET", request)
    response = connection.getresponse()
    print response.read(), "\n"
    return response.status == 200

#returns local WLAN IP or empty string if WLAN IP doesn't exist
def getLocalIP():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127."):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack("256s", "wlan0"))[20:24])
        except IOError:
            ip = ""
    return ip
