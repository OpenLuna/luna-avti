import car_control as cc
import car_network as cn
import time
import sys

def applyCommands(up, down, left, right):
    print "Got state UP:", up, "DOWN:", down, "LEFT:", left, "RIGHT:", right
    
    #driving
    if up == "on":
        control.drive(control.DRIVE_FORWARD)
    elif down == "on":
        control.drive(control.DRIVE_BACKWARD)
    else:
        control.drive(control.DRIVE_STOP)
    #steering
    if left == "on":
        control.steer(control.STEER_LEFT)
    elif right == "on":
        control.steer(control.STEER_RIGHT)
    else:
        control.steer(control.STEER_STOP)

"""
#sample config file
key: value
#this is comment
key2: value2
"""
def loadConfig(fileName = "car.config"):
    config = {}
    lineNo = 0
    with open(fileName) as f:
        for line in f:
            lineNo += 1
            line = line.strip()
            if not len(line) or line.startswith("#"):
                continue
            line = line.split(":")
            if len(line) != 2:
                print "Error reading config: line " + str(lineNo)
                continue
            key = line[0].strip().lower()
            value = line[1].strip()
            if not key or not value:
                print "Error reading config: line " + str(lineNo)
                continue
            config[key] = value
    print "Read config file with:"
    for k in config:
        print "\t" + k + ": " + config[k]
    print
    return config    

#main
if len(sys.argv) > 1: config = loadConfig(sys.argv[1])
else: config = loadConfig()

control = cc.Control()
server = cn.Server(config)
network = cn.NetworkConnection(config["server ip"])

lastPacketID = -1

config["car ip"] = server.IP
config["port"] = server.PORT

print "Advertising car to server (" + config["server ip"] + ")"
if not network.sendGETRequest("/advertise.php", config):
    print "Error executing GET"

print "Car is ready for driving!\n"

#file for timing program execution
logTimerFile = open("logs/program_timer.log", "a") #EXECUTION TIMING

while True:
    #EXECUTION TIMING - start
    programTimerStart = time.time()
    
    while not network.hasNetworkConnection():
        print "Lost network connection"
        control.stopMotors()
        time.sleep(2)
    
    #EXECUTION TIMING - config, logTimerFile
    requests = server.receive(config, logTimerFile)
    
    #test if up, down, left, right appear in requests
    ok = True
    for r in ["up", "down", "left", "right"]:
        if r not in requests:
            ok = False
            break
    if not ok:
        if requests != {}:
            print "Got invalid commands"
        continue
    
    if "time" in requests:
        #print "Got time =", requests["time"]
        packetID = int(requests["time"])
        if packetID < lastPacketID:
            print "Got late packet with id " + str(packetID)
            continue
        lastPacketID = packetID
    
    applyCommands(requests["up"], requests["down"], requests["left"], requests["right"])
    
    #EXECUTION TIMING - stop
    logTimerFile.write(config["name"] + "," + requests["time"] + ",PI-all," + str(time.time() - programTimerStart) + "\n")
    
