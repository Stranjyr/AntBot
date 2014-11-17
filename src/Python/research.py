import create
import sys
from random import *

#have the robot move to a destination based on the sample and processSample: both combined to make a number(-1,0,1) to move the robot left,forward,or right
class Movement():
    def __init__(self,port):
        self._port = port

    def rotate(self,rotation):
        if rotation == -1:
            bot.go(0,-5)
            sleep(1)
            bot.stop()
            #rotate left 5degrees
        elif rotation == 0:
            bot.go(5,0)
            sleep(1)
            bot.stop()
            #move forward 5cm/sec
        else:
            bot.go(0,5)
            sleep(1)
            bot.stop()
            #rotate right 5degrees

    def sensors(self,rotation):
        sensors = bot.sensors([create.LEFT_BUMP, create.RIGHT_BUMP])
        if sensors[create.LEFT_BUMP] == 1:  #hit something to the left
            bot.go(0,-60)
            sleep(2)
            bot.stop()
        elif sensors[create.RIGHT_BUMP] == 1:   #hit something to the right
            bot.go(0,60)
            sleep(2)
            bot.stop()
        else:       
            bot.go(15,0)
            rotate(rotation)

#main for testing purposes        
def main():
    bot = create.Create("COM4")
    print("-1 is left")
    print("1 is right")
    print("0 is straight")
    x = int(input("Where to rotate?"))
    bot.rotate(1)
    print("test is 1, meaning the robot should turn right")
    bot.rotate(-1)
    print("test is -1, meaning the robot should turn left")
    bot.rotate(0)
    print("test is 0, meaning the robot should go straight")
    bot.sensors(x)
    print("test of your input, meaning the robot should go according to what you gave it")

main()
