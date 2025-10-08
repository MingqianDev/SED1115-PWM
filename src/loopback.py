from machine import Pin, PWM, I2C
import time
from lib.ads1x15 import ADS1015

# init I2C and PWM
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
adc = ADS1015(i2c, address=0x48)
pwm = PWM(Pin(16), freq=1000)

for duty in range(0, 65536, 8192):
    pwm.duty_u16(duty)
    time.sleep(0.3)  # wait for low pass filter is stable
    raw = adc.read(channel1=2)  # read AIN2
    voltage = adc.raw_to_v(raw)
    print("Duty:", duty/65535, "ADC voltage:", voltage)
