import RFIDlib

r = RFIDlib.rfid(str(raw_input("Enter your port::  ")), 19200, 1)


#writes the initial position to a tag. For setup use.
def quick(x, y):
	r.writeFull(1, (x, y, 0, 0))
	return r.readFull(1)
#reset the tag to status quo
def reset():
	b = r.readFull(1)
	quick(b[17:19])
	for i in range(2,5):
		r.writeFull(i, (0,))
	return 1

	
