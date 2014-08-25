from create import *
import create
from random import *
from serial import *
import RFIDlib 
import datetime
import time
import struct



def main():

 bot = create.Create("/dev/ttyUSB0")
  

 objectivefound = False

 rf = RFIDlib.rfid('/dev/ttyUSB1', 19200, 0.01)

 lastX =0
 lastY =0
 
 random = Random()
 found = 0 #how many tags found
 count1 = 0
 count2 = 0

 #file to be examined after experimentation
 f=open('logs/{0!s}_workfile'.format(datetime.datetime.today()), 'a')
 f.write("*"*20)
 f.write("\n")
 f.write("NEW TRIAL at {0!s}\n".format(datetime.datetime.today()))
 while not objectivefound:
     #Obstacle response algorithm. Tells the module to start searching for RFIDs
     sensors = bot.sensors([create.LEFT_BUMP, create.RIGHT_BUMP])
     #rf.ser.write((255,0,1,130,131))  #no longer needed
     #rf.seek()
     #time.sleep(.1)
     #f.write("PAST\n")
     
     if (sensors[create.LEFT_BUMP] == 1):
         bot.go(0,-18)
         count1 += 1
	 #f.write("HIT\n")
         
     elif (sensors[create.RIGHT_BUMP]== 1):
         bot.go(0,18)
         count2 += 1
	 #f.write("HIT\n")
         
     elif ((count1 > 50) or (count2 > 50)):
         for i in range((random.randint(5,15)),random.randint(0,10)):
           bot.go(0,random.randint(-180,180))
           count1 = 0
           count2 = 0
     else:

        bot.go(15,0)
        a = 0
	#f.write("ELSE\n")
	thing = rf.seek()
	#f.write(byteout(thing))
	
	
	if len(thing)>=3  and int(thing[2].encode('hex'), 16) == 6:
        	#f.write("IF\n")
		rf.auth(1)
		
		a = toInt(rf.readBlock(1))
		#time.sleep(.01)
		
		
		#f.write(str(found)+"\n")
		#f.write(byteout(a))
		
		
		time.sleep(1) 
        	if len(a) < 21:
          		continue
		found+=1
         	if a[19] == lastX:
             		if a[20] == lastY:
                 		for i in range (0,3):
                     			bot.go(0,random.randint(-180,180))
         	if a[19] == lastX:
             		if a[20] != lastY:
                 		for i in range(3):
                     			bot.go(0,-30)
         	if a[19] != lastX:
             		if a[20] == lastY:
                 		for i in range(3):
                     			bot.go(0,30)
		
		#debug - make sure that robot responds to tags
		#else:
		#	for i in range(3):
		#		bot.go(0, random.randint(-180, 180))
         
         	tempX = lastX
         	tempY = lastY
		#f.write(byteout(a[17:19]))
         	lastX = a[17]
         	lastY = a[18]
		
	 	f.write("{0:d}: X = {1:d}, Y = {2:d}".format(found, lastX, lastY))
		f.write("  --{!s}\n".format(datetime.datetime.today()))
         	num = tempX + tempY + 2
         	rf.writeBlock(1, ((lastX),int(lastY),int(tempX),int(tempY)))
	rf.flush()


def byteout(x):
	a = len(x)
	z = ""
	for i in range(a):
		z+=str(x[i])
		z+='/'
	z+='\n'	
	return z
def toInt(x):
	a = len(x)
	z = []
	for i in range(a):
		z.append(int(x[i].encode('hex'), 16))
	return z

#not currently used
#def findIndex(x, y, index)
#	f = open("positions.txt", "r")
#	n = int(f.read(2))
#	ind = 0
#	for i in range(0, n):
#		mx = 0
#		my = 0
#		a = 0
#		j = f.read(1)
#		while(j!=":"):
#			a+=j
#			j=f.read(1)
#		f.read(1)
#		j = f.read(1)
#		while(j!=' '):
#			mx+=j
#			j = f.read(1)
#		j = f.read(1)
#		while(j!=' '):
#			my+=j
#			j = f.read(1)
#		mx = int(mx)
#		my = int(my)
#		if(mx == x && my == y):
#			ind = int(a)
#			break
#	newDex = index[0:ind] + [1] + index[ind+1:]
#	return newDex	       
main()

