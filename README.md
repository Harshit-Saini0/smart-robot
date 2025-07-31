# smart-robot
 
Hello! This is a joint project between @Harshit-Saini0 and @Noah-Philip.

We are currently working on creating a Raspberry-Pi robot that is able to navigate through a home, detects and reports the current temperatures, and is able to leverage this information using ML learning to adjust a thermostat to the user's specifications. We built this using Freenove's Tank Robot Kit as a base as well as a DHT22 temperature and humidity sensor.

**Hardware Used**
- Rasperry Pi 3
- Freenove Tank Robot Kit for Raspberry Pi
- DHT22 Temperature and Humidity Sensor
- HC-SR04 Ultrasonic Sensor
- Jumper Wires

**Software Used**
- Raspberry Pi OS
- Python 3
- pigpio daemon (to interface with robot controls)
- virtual environment

**Python Libraries**
- pigpio
- adafruit-blinka
- adafruit-circuitpython-dht
- colorama
- ... (full list in requirements.txt)

## Credits and Copyright Licensing
- Built using the [Freenove Tank Robot Kit for Raspberry Pi](http://www.freenove.com/)
- Robot control code (Motor, Led, Ultrasonic, etc.) is adapted from Freenove's original open source Python code and documentation.
- This repository and all derivations follow the [CC BY-NC-SA 3.0 license](http://creativecommons.org/licenses/by-nc-sa/3.0/).
- "Freenove" brand and logo are trademarks of Freenove Creative Technology Co., Ltd., used here for identification only.
