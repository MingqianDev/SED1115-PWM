from machine import Pin, PWM, I2C, UART
import time
from lib.ads1x15 import ADS1015

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
adc = ADS1015(i2c, address=0x48)

uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))




while True:
    uart.write("20000" + '\n')

    if uart.any():
        print("received:", uart.read())
    
    time.sleep(1)