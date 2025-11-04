from machine import Pin, PWM, UART, I2C, ADC
import time
from lib.ads1x15 import ADS1015


# init PWM
pwm = PWM(Pin(16), freq=1000) # Connect Pin 16 to the PWM pin on the other Pico board

# init I2C and ADC
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
adc = ADS1015(i2c, address=0x48)


r1 = ADC(Pin(26))

# init UART
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
    
while True:
    send_duty = r1.read_u16()
    time.sleep(0.1)
    pwm.duty_u16(send_duty)

    print(f"PWM send duty set to: {send_duty} ({send_duty / 65535 * 3.3}v, {send_duty / 65535 * 100}%)")

    # read the pwm signal
    raw = adc.read(channel1=2)  # read AIN2
    voltage = adc.raw_to_v(raw)
    recv_duty = int(voltage / 3.3 * 65535)
    print("ADC voltage:", voltage, "V")

    # send data via UART
    uart.write(f"{send_duty},{recv_duty}\n")

    # check if any data is avaliable to read
    if uart.any():
        line = uart.readline() # read the line from the UART
        if line:
            try:
                line = line.decode().strip()

                # Split into two integer values: send_duty, recv_duty
                UART_send_duty, UART_recv_duty = map(int, line.split(','))

                print(f"[UART] Received from other Pico send_duty={UART_send_duty}, recv_duty={UART_recv_duty}")

                print("error % for the signal sent from this Pico:", abs(UART_recv_duty - send_duty) / send_duty * 100, "%")
                print("error % for the signal recevied from this Pico:", abs(UART_send_duty - recv_duty) / UART_send_duty * 100, "%")


            except ValueError:
                print("[UART] Could not interpret received data:", line)
            except Exception as e:
                print("[UART] Unexpected error while parsing:", e)
  
    else:
        print("Pico disconnected")
    
    print("-------------------------------------------------------")
    
    time.sleep(1)