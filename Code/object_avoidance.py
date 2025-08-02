import time
from Motor import *
from Led import *
from Ultrasonic import *

PWM = Motor()
led = Led()
ultrasonic = Ultrasonic()

LED_FAR = 0x02      # green LED
LED_MEDIUM = 0x04   # blue LED 
LED_CLOSE = 0x01    # red LED

def indicate_distance(distance):
    """Light LED according to the distance from the obstacle."""
    if distance > THRESH_MEDIUM:
        # Far: Green
        led.colorWipe(led.strip, Color(0,255,0))
    elif THRESH_SLOW < distance <= THRESH_MEDIUM:
        # Medium: Yellow
        led.colorWipe(led.strip, Color(255,128,0))
    else:
        # Close: Red
        led.colorWipe(led.strip, Color(255,0,0))

def forward(speed=2000, duration=0.05):
    PWM.setMotorModel(speed, speed)
    print(f"The car is moving forward at speed {speed}")
    time.sleep(duration)

def forward_slow():
    forward(speed=1200, duration=0.05)

def forward_medium():
    forward(speed=1600, duration=0.05)

def forward_fast():
    forward(speed=2000, duration=0.05)

def reverse_and_turn():
    # Blink red while reversing
    for _ in range(3):
        led.colorWipe(led.strip, Color(255,0,0))
        PWM.setMotorModel(-1200, -1200)
        time.sleep(0.15)
        led.colorWipe(led.strip, Color(0,0,0))
        time.sleep(0.08)
    PWM.setMotorModel(0,0)
    time.sleep(0.1)
    PWM.setMotorModel(4000, -4000)
    print("The car is turning right")
    time.sleep(1)
    PWM.setMotorModel(0,0)

THRESH_EMERGENCY = 15    # cm
THRESH_SLOW      = 25    # cm
THRESH_MEDIUM    = 50    # cm


def stop_all():
    PWM.setMotorModel(0, 0)
    led.colorWipe(led.strip, Color(0,0,0))

if __name__ == '__main__':
    print('Obstacle avoidance starting')
    #allow time for robot to be unplugged from peripherals
    time.sleep(20)
    #blink white as a warning
    start_time = time.time()
    
    try:
        #blink white when starting
        for _ in range(3):
           led.colorWipe(led.strip, Color(255,255,255))
           time.sleep(0.2)
           led.colorWipe(led.strip, Color(0,0,0))
           time.sleep(0.1)
           
        
        #object avoidance loop
        while time.time() - start_time < 10:
            distance = int(ultrasonic.get_distance())
            print("Obstacle distance is {}CM".format(distance))
            indicate_distance(distance)

            if distance > THRESH_MEDIUM:
                forward_fast()
            elif distance > THRESH_SLOW:
                forward_medium()
            elif distance > THRESH_EMERGENCY:
                forward_slow()
            else:
                reverse_and_turn()
            time.sleep(0.05)
    
    except KeyboardInterrupt:
        pass
    finally:
        stop_all()
        print("\nEnd of program")
