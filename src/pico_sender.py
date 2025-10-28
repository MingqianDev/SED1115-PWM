from machine import Pin, PWM, UART, I2C
import time
from lib.ads1x15 import ADS1015


# init PWM
pwm = PWM(Pin(16), freq=1000) # Connect Pin 16 to the PWM pin on the other Pico board

# init I2C and ADC
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
adc = ADS1015(i2c, address=0x48)

# init UART
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# set the duty cycle and send the pwm signal to the other Pico board
send_duty = int(0.1 * 65535)
pwm.duty_u16(send_duty)
    
while True:
    print(f"PWM send duty set to: {send_duty} ({send_duty / 65535 * 3.3}v)")
    # send data via UART
    # uart.write("PWM duty: " + str(duty) + "\n")
    # print("UART sent: ", str(duty))

    # read the pwm signal
    raw = adc.read(channel1=2)  # read AIN2
    voltage = adc.raw_to_v(raw)
    recv_duty = int(voltage / 3.3 * 65535)
    print("ADC voltage:", voltage, "V")

    # send the measurement back
    # uart.write("Reveived: " + str(duty) + "\n")

    # send data via UART
    uart.write(f"{send_duty},{recv_duty}\n")

    # check if any data is avaliable to read
    if uart.any():
        line = uart.readline() # read the line from the UART
        if line:
            try:
                line = line.strip()

                # Split into two integer values: send_duty, recv_duty
                send_duty, recv_duty = map(int, line.split(','))

                print(f"[UART] Received from other Pico → send_duty={send_duty}, recv_duty={recv_duty}")

            except ValueError:
                print("[UART] Could not interpret received data:", line)
            except Exception as e:
                print("[UART] Unexpected error while parsing:", e)

    
    time.sleep(1)

