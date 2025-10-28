from machine import Pin, I2C, UART
import time
from lib.ads1x15 import ADS1015

# init I2C and ADC
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
adc = ADS1015(i2c, address=0x48)

# init UART
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

while True:
    # read the signal 
    raw = adc.read(channel1=2)  # read AIN2
    voltage = adc.raw_to_v(raw)
    duty = int(voltage / 3.3 * 65535)
    print("ADC voltage:", voltage, "V")

    # send the measurement back
    uart.write(str(duty) + "\n")
    # print("UART sent: ", str(duty))

    if uart.any():
        line = uart.readline() # read the line from the UART
        if line:
            try:
                text = line.strip() # strip the whitespace
                received_value = int(text) # between 0-635535
                print("UART Received:", received_value)

                error = abs(received_value - duty) / received_value * 100 # calculate the error as a percentage
                print("Error:", error, "%")
            except ValueError:
                print("Could not interpret received data.")
    
    print("-------------------------------------")
        
    time.sleep(1)