import serial

import io

import time

class rfid(object):

	ser = serial.Serial()

	def __init__(self, port, baud, t=.1):

		 print(self.setup(port, baud, t))


	
#this sets up the serial device called in this library.
	
#always call this function first

	#if it returns true, then your serial port opened correctly

	def setup(self, port, baud, t):

		self.ser.port = port

		self.ser.baudrate = baud

		self.ser.timeout = t

		self.ser.open()

		return self.ser.isOpen()



	#sends the seek command to the RFID.
 
	#No inputs

	#Returns the serial number of the tag read in.

	def flush(self):

		self.ser.read(100)


	def seek(self):

		self.flush()

		self.ser.write((255, 0, 1, 130, 131))

		self.ser.read(6)

		return self.ser.read(11)



	#Authenticates block b of a tag

	#Input: integer b as the block

	#returns the bytearray reply of the tag
	def auth(self, b):

		self.flush()

		ck = 3+0x85+b+255

		self.ser.write((255, 0, 3, 0x85, b, 0xFF, ck%256))

		return self.ser.read(7)



	#reads an authenticated block

	#Input: integer b as the block

	#returns the 16 bit bytearray on block b of tag

	#If read fails, returns RFID response
	def readBlock(self, b):

		self.flush()

		ck = 0x02+0x86+b

		self.ser.write((0xFF, 0x00, 0x02, 0x86, b, ck%256))

		return self.ser.read(21)



	#Writes the entered array(tuple) to block b

	#Inputs: integer b as block, bytearray msg as thing to write

	#Returns the written message

	#If write fails, returns the RFID response

	def writeBlock(self, b, msg):

		self.flush()

		ck = 0x12+0x89+b

		self.ser.write((0xFF, 0x00, 0x12, 0x89,b))

		i = len(msg)

		while(i>0):

			i-=1

			ck+=msg[i]

		for j in range(len(msg), 16):

			self.ser.write((0x00, ))

		self.ser.write(msg)

		self.ser.write((ck%256,))

		return self.ser.read(21)


	#reads the position digits of a tag, as defined in documentation

	#returns the position of the tag as an tuple (x, y)

	#if fails, returns (-1, -1)

	def readPos(self):

		self.auth(1)

		b = self.readBlock(1)

		if(len(b) == 21):
			#check that a tag was read

			return b[17:19]

		return (-1, -1)


	#writes the last found position to a tag, as defined in the docs

	#returns the position written

	#if fails, returns (-1, -1)

	def writePos(self, x, y, lx, ly):

		self.auth(1)

		b = self.writeBlock(1, (x, y, lx, ly))

		if(len(b) == 21):

			return b[19:21]

		return (-1, -1)



	#depreciated - can be used for debuging.

	#these methods call seek each time they write, which is unneeded

	def writeFull(self, b, msg):

		self.seek()

		self.auth(b)

		return self.writeBlock(b, msg)

	def readFull(self, b):

		self.seek()

		self.auth(b)

		return self.readBlock(b)
