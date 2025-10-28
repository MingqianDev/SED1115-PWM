from machine import Pin, PWM, I2C, UART, ADC
import time
from lib.ads1x15 import ADS1015

# init I2C and PWM
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
adc = ADS1015(i2c, address=0x48)
pwm = PWM(Pin(16), freq=1000) # Connect Pin 16 to PWM

r1 = ADC(Pin(26))

# init UART
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9)) # connect tx and rx together


def loopback_pwm():
    for duty in range(0, 65536 + 8192, 8192):
        pwm.duty_u16(duty)
        time.sleep(0.3)  # wait for low pass filter is stable
        raw = adc.read(channel1=2)  # read AIN2
        voltage = adc.raw_to_v(raw)
        print("Duty:", duty/65535, "ADC voltage:", voltage)

def loopback_uart():
    while True:
        # send data
        value = int(0.375 * 65535)
        uart.write(str(value) + "\n")
        time.sleep(1)

        # check if any data is avaliable to read
        if uart.any():
            line = uart.readline() # read the line from the UART
            if line:
                try:
                    text = line.strip() # decode the line to a string and strip the whitespace
                    received_value = int(text)
                    print("Received:", received_value)
                except ValueError:
                    print("Could not interpret received data.")


def loopback_whole():

    while True:
        # set the duty cycle
        duty = r1.read_u16()
        pwm.duty_u16(duty)
        print("PWM duty cycle set to: ", duty / 65535 * 100, "%")

        # send data
        uart.write(str(duty) + "\n")

        # read the signal 
        raw = adc.read(channel1=2)  # read AIN2
        voltage = adc.raw_to_v(raw)
        print("ADC voltage:", voltage, "V")
        print("ADC raw data: ", raw)

        if uart.any():
            line = uart.readline() # read the line from the UART
            if line:
                try:
                    text = line.strip() # strip the whitespace
                    received_value = int(text) # between 0-65535
                    print("Received:", received_value)

                    error = abs(received_value - raw) / received_value * 100 # calculate the error as a percentage
                    print("Error:", error, "%")
                except ValueError:
                    print("Could not interpret received data.")

        print("-------------------------------------")
        
        time.sleep(1)

loopback_whole()