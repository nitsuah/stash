# Power Failure Alarm Circuit

This is a simple electronic circuit that can be used as a power failure alarm. The circuit is powered by a USB power source and contains the following components:

- Diode (D1): 1N4001
- Transistor (Q1): 2N2905
- Resistor (R1): 5kΩ
- Resistor (R2): 10kΩ
- Capacitor (C2): 2nF
- Buzzer (BUZZ1): 8Ω

## Circuit Description

When the USB power source is connected, the capacitor C2 charges up through the diode D1 and the resistor R1. The transistor Q1 is turned off, so no current flows through the buzzer BUZZ1. When the USB power source is disconnected, the capacitor C2 discharges through the buzzer BUZZ1, producing a sound.

## Disclaimer

Please note that while this circuit can be used as a power failure alarm, it may not be as reliable as a dedicated power failure alarm circuit. Alarm duration is limited by the capacitor and buzzers used. The circuit may not work with some USB power sources. Use at your own risk.
