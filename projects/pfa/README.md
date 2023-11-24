# Power Failure Alarm Circuit

![pfa_pcb.png](https://raw.githubusercontent.com/nitsuah/stash/develop/projects/pfa/pfa_pcb.png)

A nifty electronic circuit designed for a power failure alarm, fueled by a USB power source. Components include:

- `Diode (D1): 1N4001` - Ensures one-way current flow, preventing capacitor discharge into the power source.
- `Transistor (Q1): 2N2905` - Acts as a switch; turned off when power is connected, allowing alarm activation upon power disconnection.
- `Resistor (R1): 5kΩ` - Limits charging current for capacitor C2, ensuring a smooth charging process.
- `Resistor (R2): 10kΩ` = Controls current to the transistor's base, influencing its switching behavior.
- `Capacitor (C2): 2nF` = Stores energy; discharges through the buzzer, producing an alarm sound when power is cut.
- `Buzzer (BUZZ1): 8Ω` - Produces audible alert when powered by the discharged capacitor upon power failure.

## Circuit Description

Upon USB connection, the capacitor (C2) charges via D1 and R1, keeping Q1 off, and BUZZ1 silent. When power disconnects, C2 discharges through BUZZ1, generating a sound alert until fully discharged.

## Disclaimer

While effective, note that this circuit may not match the reliability of dedicated power failure alarms. Alarm duration depends on capacitor and buzzer specifics, and compatibility issues may arise with certain USB power sources. Use at your own discretion.
