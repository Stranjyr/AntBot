hsvG = eval (input ("Enter a Python list: "))
hsvG[0] = hsvG[0]/360*179
hsvG[1] = hsvG[1]/100*255
hsvG[2] = hsvG[2]/100*255
print(hsvG)
input("press enter to quit")