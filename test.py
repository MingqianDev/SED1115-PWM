from machine import PWM, Pin
import time

pwm = PWM(Pin(6), freq=1000)

pwm.duty_u16(10000)