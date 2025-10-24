from machine import Pin, PWM, UART
import time

# init PWM
pwm = PWM(Pin(16), freq=1000) # Connect Pin 16 to the PWM pin on the other Pico board

# init UART
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# set the duty cycle and send the pwm signal to the other Pico board
duty = int(0.375 * 65535)
pwm.duty_u16(duty)
    
while True:
    # send data
    uart.write(str(duty) + "\n")

    # check if any data is avaliable to read
    if uart.any():
        line = uart.readline() # read the line from the UART
        if line:
            try:
                text = line.strip() # strip the whitespace
                received_value = int(text)
                print("Received:", received_value)

                error = abs(received_value - duty) / duty * 100 # calculate the error as a percentage
                print("Error:", error, "%")
            except ValueError:
                print("Could not interpret received data.")

    print("-------------------------------------")

    time.sleep(1)

