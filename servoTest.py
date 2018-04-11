import serial
import time

dev = serial.Serial("/dev/ttyACM0", 9600)

data = raw_input()

print dev.write("0 0 0 0 90")
time.sleep(4)

print dev.write("0 0 0 12 90")
time.sleep(4)

print dev.write("0 0 9 12 90")
time.sleep(4)

print dev.write("0 0 9 0 90")
time.sleep(4)

print dev.write("0 0 6 4 90")
time.sleep(4)

print dev.write("0 0 6 4 0")
time.sleep(4)

print dev.write("0 0 6 4 180")
time.sleep(4)

print dev.write("0 0 6 4 90")
time.sleep(4)


dev.close()
