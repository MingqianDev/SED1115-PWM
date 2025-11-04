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

    # print(f"PWM send duty set to: {send_duty} ({send_duty / 65535 * 3.3}v, {send_duty / 65535 * 100}%)")

    # read the pwm signal
    raw = adc.read(channel1=2)  # read AIN2
    voltage = adc.raw_to_v(raw)
    recv_duty = int(voltage / 3.3 * 65535)
    # print("ADC voltage:", voltage, "V")

    # send data via UART
    uart.write(f"{send_duty},{recv_duty}\n")

    print("\n========== CYCLE REPORT ==========")
    print(f"PWM Output: {send_duty:<6d}  | {send_duty / 65535 * 3.3:>5.3f} V  | {send_duty / 65535 * 100:>6.2f} %")
    print(f"ADC Input:  {recv_duty:<6d}  | {voltage:>5.3f} V")
    print("----------------------------------")

    # check if any data is avaliable to read
    if uart.any():
        line = uart.readline() # read the line from the UART
        if line:
            try:
                line = line.decode().strip()

                # Split into two integer values: send_duty, recv_duty
                UART_send_duty, UART_recv_duty = map(int, line.split(','))

                err_send = abs(UART_recv_duty - send_duty) / send_duty * 100
                err_recv = abs(UART_send_duty - recv_duty) / UART_send_duty * 100


                print("[UART] RX Data:")
                print(f"  Peer send_duty = {UART_send_duty:<6d}  |  recv_duty = {UART_recv_duty:<6d}")
                print(f"  Error % (send): {err_send:>6.3f} %")
                print(f"  Error % (recv): {err_recv:>6.3f} %")

            except ValueError:
                print("[UART] Could not interpret received data:", line)
            except Exception as e:
                print("[UART] Unexpected error while parsing:", e)
  
    else:
        print("[UART] Pico UART disconnected")
    
    print("-------------------------------------------------------")
    
    time.sleep(1)