import time
import serial
ser = serial.Serial("/dev/ttyS0", baudrate = 9600, parity = serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
counter = 0
time_p = 0

while counter < 21:
    ser.write(b'Time: %d \n Time Diff: %d \n'%(time.time(),(time.time() - time_p)))
    print("Printed")
    time.sleep(1)
    counter +=1
    time_p = time.time()
