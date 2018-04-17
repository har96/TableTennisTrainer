import serial
dev = serial.Serial("/dev/ttyACM0")
dev.close()
dev.open()
dev.close()

