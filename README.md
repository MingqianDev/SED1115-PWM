# Dual Raspberry Pi Pico PWM Communication System

This project demonstrates a **symmetric communication system between two Raspberry Pi Pico boards**.  
Each Pico generates a PWM signal, filters it through an RC low-pass filter (integrated on an extension board), reads the filtered analog voltage via an ADS1015 ADC over I²C, and exchanges data through UART.  
Both boards act as transmitter and receiver simultaneously, forming a closed feedback loop.

## Hardware Connections

| Function        | Pico Pin | Connected To                    |
|-----------------|-----------|---------------------------------|
| PWM Output      | GP16      | Extension board PWM input       |
| UART TX         | GP8      | Other Pico’s RX (GP9)           |
| UART RX         | GP9       | Other Pico’s TX (GP8)           |
| GND             | —         | Common ground between all boards |

*The RC low-pass filter is pre-built on the extension board; no extra wiring is required.*

## Dependencies
- MicroPython
- ADC1x15 library

