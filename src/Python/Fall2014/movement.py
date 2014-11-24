import create
import seeker
import sys
from random import *
import time

#have the robot move to a destination based on the sample and processSample: both combined to make a number(-1,0,1) to move the robot left,forward,or right
class Movement():
    def __init__(self,port):
        self._port = port
        self.bot = create.Create(port)
        self.degree = 5
        self.distance = 5

    def rotate(self,rotation):
        if rotation == -1:
            self.bot.go(0,-self.degree)
            sleep(1)
            self.bot.stop()
            #rotate left
        elif rotation == 0:
            self.bot.go(self.distance,0)
            sleep(1)
            self.bot.stop()
            #move forward cm/sec
        else:
            self.bot.go(0,self.degree)
            sleep(1)
            self.bot.stop()
            #rotate right

    def sensors(self,rotation):
        sensors = self.bot.sensors([create.LEFT_BUMP, create.RIGHT_BUMP])
        if sensors[create.LEFT_BUMP] == 1:  #hit something to the left
            self.bot.go(0,-60)
            sleep(2)
            self.bot.stop()
        elif sensors[create.RIGHT_BUMP] == 1:   #hit something to the right
            self.bot.go(0,60)
            sleep(2)
            self.bot.stop()
        else:       
            self.bot.go(15,0)
            self.rotate(rotation)

#main for testing purposes        
def main():
    bot = Movement("COM4")
    print("-1 is left")
    print("1 is right")
    print("0 is straight")
    x = int(input("Where to go?"))
    bot.sensors(x)
main()    
