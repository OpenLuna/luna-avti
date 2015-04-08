import RPi.GPIO as GPIO
import time

class Control:
    """constants for easy reading DO NOT TOUCH"""
    DRIVE_FORWARD, DRIVE_BACKWARD, DRIVE_STOP = 0, 1, 2
    STEER_LEFT, STEER_RIGHT, STEER_STOP = 3, 4, 5

    """
    Pins on PI that are connected to motor driver
    enable and input pins. 
    ENABLE_A enables/disables INPUT_1/2 
    ENABLE_B enables/disables INPUT_3/4

    Steering motor is connected to INPUT_1/2. 
    INPUT_1 = GND
    INPUT_2 = Vs

    Drive motor is connected to INPUT_3/4.
    INPUT_3 = GND
    INPUT_4 = Vs

    """
    ENABLE_A = 19
    ENABLE_B = 15
    INPUT_1 = 23
    INPUT_2 = 21
    INPUT_3 = 13
    INPUT_4 = 11
    
    LED_GREEN = 33
    LED_RED = 37
    """
    Internal state of the car
    steerState: -1 left, 0 stop, 1 right
    driveState: -1 backward, 0 stop, 1 forward
    """
    driveState = 0
    steerState = 0
    
    timeGreenLED = 0
    timeRedLED = 0

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup((self.ENABLE_A, self.INPUT_1, self.INPUT_2), GPIO.OUT)
        GPIO.setup((self.ENABLE_B, self.INPUT_3, self.INPUT_4), GPIO.OUT)
        GPIO.setup((self.LED_GREEN, self.LED_RED), GPIO.OUT)
        GPIO.output(self.ENABLE_A, GPIO.LOW)
        GPIO.output(self.ENABLE_B, GPIO.LOW)

    def __del__(self):
        GPIO.output((self.ENABLE_A, self.INPUT_1, self.INPUT_2), GPIO.LOW)
        GPIO.output((self.ENABLE_B, self.INPUT_3, self.INPUT_4), GPIO.LOW)
        GPIO.output((self.LED_GREEN, self.LED_RED), GPIO.LOW)
        GPIO.cleanup()
    
    #zasveti z ledico za timeOn sekund
    def LED(self, color, timeOn = -1):
        if timeOn != -1:
            if color == "green":
                if timeOn != 0:
                    self.timeGreenLED = time.time() + timeOn
                GPIO.output(self.LED_GREEN, GPIO.HIGH)
            else:
                if timeOn != 0:
                    self.timeRedLED = time.time() + timeOn
                GPIO.output(self.LED_RED, GPIO.HIGH)
        else:
            if self.timeGreenLED != 0 and self.timeGreenLED < time.time():
                GPIO.output(self.LED_GREEN, GPIO.LOW)
                self.timeGreenLED = 0
            if self.timeRedLED != 0 and self.timeRedLED < time.time():
                GPIO.output(self.LED_RED, GPIO.LOW)
                self.timeRedLED = 0
    
    def drive(self, cmd):
        if cmd == self.DRIVE_STOP:
            GPIO.output(self.ENABLE_B, GPIO.LOW)
            driveState = 0
        else:
            GPIO.output(self.ENABLE_B, GPIO.HIGH)
            if cmd == self.DRIVE_FORWARD:
                GPIO.output(self.INPUT_3, GPIO.HIGH)
                GPIO.output(self.INPUT_4, GPIO.LOW)
                driveState = 1
            elif cmd == self.DRIVE_BACKWARD:
                GPIO.output(self.INPUT_3, GPIO.LOW)
                GPIO.output(self.INPUT_4, GPIO.HIGH)
                driveState = -1
            else:
                raise Exception("unknown driving command")
    
    def steer(self, cmd):
        if cmd == self.STEER_STOP:
            GPIO.output(self.ENABLE_A, GPIO.LOW)
            steerState = 0
        else:
            GPIO.output(self.ENABLE_A, GPIO.HIGH)
            if cmd == self.STEER_LEFT:
                GPIO.output(self.INPUT_1, GPIO.LOW)
                GPIO.output(self.INPUT_2, GPIO.HIGH)
                steerState = -1
            elif cmd == self.STEER_RIGHT:
                GPIO.output(self.INPUT_1, GPIO.HIGH)
                GPIO.output(self.INPUT_2, GPIO.LOW)
                steerState = 1
            else:
                raise Exception("unknown steering command")
    
    def toggleForward(self):
        if self.driveState < 1:
            self.drive(self.DRIVE_FORWARD)
        else:
            self.drive(self.DRIVE_STOP)
        
    def toggleBackward(self):
        if self.driveState > -1:
            self.drive(self.DRIVE_BACKWARD)
        else:
            self.drive(self.DRIVE_STOP)
            
    def toggleLeft(self):
        if self.steerState > -1:
            self.steer(self.STEER_LEFT)
        else:
            self.steer(self.STEER_STOP)
            
    def toggleRight(self):
        if self.steerState < 1:
            self.steer(self.STEER_RIGHT)
        else:
            self.steer(self.STEER_STOP)
    
    def stopMotors(self):
        self.steer(self.STEER_STOP)
        self.drive(self.DRIVE_STOP)
        self.steerState = 0
        self.driveState = 0
