from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging
import time
import numpy as np

addresses = ['10.19.96.157','10.19.96.158']

class Gantry():

    def __init__(self): # initializes the gantry class
        self.coms = []
        self.mots = []
        self.center = [0,0]
        self.currentAbs = [0,0]
        self.currentRel = [0,0]
        
    def connect(self, addresses): # connects to the gantry and references the motors
        self.coms = [ComModbus(ip_address=add) for add in addresses]
        self.mots = [MotionHandler(com) for com in self.coms]
        for mot in self.mots:
            mot.acknowledge_faults()
            mot.enable_powerstage()
            if not mot.referenced():
                mot.referencing_task()
        while True:
            target_positions_reached = [mot.target_position_reached() for mot in self.mots]
            if all(target_positions_reached):
                break
            time.sleep(0.1)
        self.positionAbs()    
        self.positionRel()    

    def positionAbs(self): # returns the absolute position of the gantry
        self.currentAbs = [mot.current_position() for mot in self.mots]
        return self.currentAbs
    
    def positionRel(self): # returns the relative position of the gantry with respect to the zero-position
        self.currentRel = [mot.current_position()-c for [mot,c] in zip(self.mots,self.center)]
        return self.currentRel
        
    def moveRelative(self, position, velocity=[300,300]): # moves the gantry to the specified relative position with the specified velocity
        for [mot,pos,vel,absPos] in zip(self.mots,position,velocity,self.positionAbs()):
            if absPos + pos < 0:
                pos = absPos
            elif absPos + pos > 500:
                pos = 500-absPos
            mot.position_task(pos, vel, nonblocking=True, absolute=False)
        while True:
            currentPosition = [mot.current_position() for mot in self.mots]
            print(currentPosition)
            target_positions_reached = [mot.target_position_reached() for mot in self.mots]
            if all(target_positions_reached):
                break
            time.sleep(0.1)
        self.positionAbs()
        self.positionRel()
            
    def moveAbsolute(self, position, velocity=[300,300]): # moves the gantry to the specified absolute position with the specified velocity
        for [mot,pos,vel,c] in zip(self.mots,position,velocity,self.center): #,self.positionAbs(),self.zero
            
            pos = pos+c
            if pos < 0:
                pos = 0
            elif pos > 495:
                pos = 495
            print("from 'moveAbsolute': Moving to position: " + str(pos - c))
            mot.position_task(pos, vel, nonblocking=True, absolute=True)
        while True:
            currentPosition = [mot.current_position() for mot in self.mots]
            # print(currentPosition)
            target_positions_reached = [mot.target_position_reached() for mot in self.mots]
            if all(target_positions_reached):
                break
            time.sleep(0.1)
        self.positionAbs()
        self.positionRel()

    def stop(self):
        for mot in self.mots:
            mot.stop_motion_task()
        self.positionAbs()
        self.positionRel()

    def setCenter(self): # sets user-defined zero-position of the gantry
        self.center = [mot.current_position() for mot in self.mots]

    def close(self):
        for mot in self.mots:
            mot.disable_powerstage()
        # for com in self.coms:
        #     com.close()

    def home(self):
        for [mot,c] in zip(self.mots,self.center):
            mot.position_task(c, 300, nonblocking=True, absolute=True)

    def toCorner(self):
        for mot in self.mots:
            mot.position_task(0, 300, nonblocking=True, absolute=True)
        while True:
            currentPosition = [mot.current_position() for mot in self.mots]
            print(currentPosition)
            target_positions_reached = [mot.target_position_reached() for mot in self.mots]
            if all(target_positions_reached):
                break
            time.sleep(0.1)
        self.positionAbs()
        self.positionRel()
        

    def pattern(self, width, length, numStepsWidth, numStepsLength, restTime):
        widthPos = np.linspace(-width/2, width/2, numStepsWidth)
        print(widthPos)
        
        lengthPos = np.linspace(-length/2, length/2, numStepsLength)
        print(lengthPos)
        for w in widthPos:
            for l in lengthPos:
                self.moveAbsolute([int(round(w)),int(round(l))])
                print("width position = ", w)
                print("length position = ", l)
                print(self.positionAbs())
                print(self.positionRel())
                time.sleep(restTime)

    # def connect(self, address):
    #     self.coms = [ComModbus(ip_address=add) for add in address]
    #     self.mots = [MotionHandler(com) for com in self.coms]
        
    #     for mot in self.mots:
    #         mot.acknowledge_faults()
    #         mot.enable_powerstage()
    #         if not mot.referenced():
    #             mot.referencing_task()

    # def home(self):
    #     for mot in self.mots:
    #         mot.position_task(0, 300, nonblocking=True, absolute=True)
    #     time.sleep(0.1)
    #     while True:
    #         target_positions_reached = [mot.target_position_reached() for mot in self.mots]
    #         Logging.logger.info(f"Target positions reached: {target_positions_reached}")
    #         if all(target_positions_reached):
    #             break
    #         time.sleep(0.1)


    # def move(self, position, velocity):
    #     for [mot,pos] in zip(self.mots,position):
    #         mot.position_task(pos, velocity, nonblocking=True, absolute=True)



    if __name__ == "__main__":
        print("gantry class can  not be used on its own")