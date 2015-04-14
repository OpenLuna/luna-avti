import socket
import httplib
import urllib
import os
import datetime as dt
import time

class NetworkConnection:
    lastPing = 0
    lastConnectionCheck = 0
    
    def __init__(self, ip, minPingInterval = 1):
        self.IP = ip #car server ip
        self.LOG_FILE_NAME = "log_" + dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        self.MIN_PING_INTERVAL = minPingInterval
        
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        print "Server IP: " + self.IP
        print "Log file: " + self.LOG_FILE_NAME
        print "Minimum req interval: " + str(self.MIN_PING_INTERVAL)
        print
        
    def ping(self):
        if time.time() - self.lastPing > self.MIN_PING_INTERVAL:
            self.lastPing = time.time()
            response = os.system("ping -Dc1 " + self.IP + " | head -n2 | tail -n1 >> logs/" + self.LOG_FILE_NAME)
            if response != 0:
                print "Unsuccessful ping request to " + self.IP
    
    def hasNetworkConnection(self):
        if time.time() - self.lastConnectionCheck > self.MIN_PING_INTERVAL:
            self.lastConnectionCheck = time.time()
            if getLocalIP(): return True
            else: return False
        return True
    
    def sendGETRequest(self, path, params):
        connection = httplib.HTTPConnection(self.IP)
        request = path + "?" + urllib.urlencode(params)
        #print "Sending GET request to " + self.IP + ": " + request
        connection.request("GET", request)
        response = connection.getresponse()
        print response.read()
        print
        return response.status == 200

#TODO time analysis
class Server:
    HTML_HEADER = "HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: * \nContent-Type: text/html\n\n"
    
    def __init__(self, config, ip = None, port = 12345):
        if not ip:
            while True:
                self.IP = getLocalIP()
                if self.IP: break
                print "Error getting local IP: check network connection"
                time.sleep(2)
        else: self.IP = ip
        
        self.PORT = port

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.serverSocket.bind((self.IP, self.PORT))
            except socket.error as e:
                if e.errno == 98: print "Waiting for old socket to release"
                else: print e
                time.sleep(2)
            else:
                print "Listening on", self.IP + ":" + str(self.PORT)
                print
                break
        self.serverSocket.setblocking(False)
        self.serverSocket.listen(20)
    
    def __del__(self):
        self.serverSocket.close()
    
    def receive(self, config, lf):
        requests = {}
        try:
            #EXECUTION TIMING - start
            programTimerStart = time.time() 
            clientSocket, address = self.serverSocket.accept()
            
            """buff = []
            clientSocket.setBlocking(True)
            while True:
                try:
                    time.sleep(1)
                    data = clientSocket.recv(1024)
                    print "data:", data
                    buff.append(data)
                except socket.error:
                    print "here"
                    break
                
            data = "".join(buff)"""
            
            data = clientSocket.recv(1024)
            #EXECUTION TIMING - stop
            programTimerStop = time.time()
            requests = getRequests(data)
            
            if "nd" in requests:
                lf.flush()
                with open(lf.name, "r") as f:
                    clientSocket.sendall(self.HTML_HEADER)
                    clientSocket.sendall(f.read())
                    clientSocket.close()
            else:
                lf.write(config["name"] + "," + requests["time"] + ",PI-receive," + str(programTimerStop - programTimerStart) + "\n")
                #EXECUTION TIMING - start
                programTimerStart = time.time()
                clientSocket.sendall(self.HTML_HEADER + "OKK\n")
                #clientSocket.shutdown(socket.SHUT_RDWR)
                clientSocket.close()

                #EXECUTION TIMING - stop
                lf.write(config["name"] + "," + requests["time"] + ",PI-send," + str(time.time() - programTimerStart) + "\n")     
        except socket.error:
            pass
        
        return requests

def getLocalIP():
    import fcntl
    import os
    import struct
    
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127."):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack("256s", "wlan0"))[20:24])
        except IOError:
            ip = ""
    return ip

#TODO handle errors
def getRequests(html):
    #GET request in form /xxx?a1=d1&a2=d2...
    requests = {"time": "-1"} #EXECUTION TIMING
    #print "HTML\n", html
    try:
        s = html.split("\n")[0].split()[1]
        s = s[s.find("?")+1:] #a1=d1&a2=d2...
        
        for r in s.split("&"):
            r = r.split("=")
            requests[r[0].lower()] = r[1].lower()
    
    except IndexError:
        print "Got empty REQUEST"    
    
    return requests
