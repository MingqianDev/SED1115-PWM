# Software Licensing and Tool Justification

## 1. Software and Module License Documentation

| Module      | Subcomponents                        | License     | Reference                                                                             | Usage Justification                                                                                                                                                                                                                                                                                        |
| ----------- | ------------------------------------ | ----------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **machine** | `Pin`, `PWM`, `ADC`, `UART`, `Timer` | MIT License | [MicroPython License](https://github.com/micropython/micropython/blob/master/LICENSE) | Provides access to Raspberry Pi Pico hardware. These functions are necessary for low-level I/O control, PWM signal generation, analog input conversion (ADC), serial communication (UART), and timed execution (Timer). They are officially supported and well-documented as part of the MicroPython core. |


**Evidence of Permission:**
All MicroPython core libraries are distributed under the MIT License, which allows reuse, modification, and distribution for both educational and commercial purposes with attribution.

---

## 2. Reuse Justification

### Feature Set

* machine module: provides essential hardware interface functions:
  * `Pin` – controls GPIO direction and logic level.
  * `PWM` – generates configurable pulse-width-modulated digital signals.
  * `ADC` – reads analog voltage from RC-filtered PWM signal.
  * `UART` – handles serial communication between Pico devices.
  * `Timer` – provides periodic callbacks for sampling or data exchange.
### Reliability and Code Quality

* MicroPython has been in active development since 2013, with a wide range of usage.  
* Modules such as `machine` and `time` are part of the official MicroPython firmware, tested extensively by community.
- Reliability is considered high.
* Documentation: detailed and consistent, available on the official [MicroPython documentation site](https://docs.micropython.org/en/latest/).

The following modules and scripts will be developed by the us:

* PWM generation control logic (to vary duty cycle and transmit setpoints).
* UART communication routines (to send and receive PWM data between two Pico boards).
* ADC reading and scaling functions.
* RC filter compensation and result comparison logic.
* Data display and difference calculation functions.

---

## 3. Tool Flow and Programming/Testing Environment

| Tool                        | License       | Purpose                         | Justification                                                                                                           |
| --------------------------- | ------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Visual Studio Code (VSCode) | MIT License   | Code editing and debugging      | Widely used, stable, and extensible IDE. Provides syntax highlighting, version control, and MicroPython plugin support. |
| Git                         | GPLv2 License | Version control and code backup | Ensures traceable development history and safe code management. Suitable for collaborative development workflows.       |
| MicroPython Firmware        | MIT License   | Runtime environment on Pico     | Required for executing Python code on embedded hardware.                                                                |

**Testing Flow:**

1. Develop and version control source files using VSCode and Git.
2. Upload and run scripts on Pico boards via MicroPython
3. Validate PWM and analog output with multimeter and print function.
