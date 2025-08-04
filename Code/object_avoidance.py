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
    print("The car is turning right")
    PWM.turn_left_90()
    PWM.setMotorModel(0,0)

THRESH_EMERGENCY = 15    # cm
THRESH_SLOW      = 25    # cm
THRESH_MEDIUM    = 50    # cm
MAX_RANGE      = 180   # cm


def stop_all():
    PWM.setMotorModel(0, 0)
    led.colorWipe(led.strip, Color(0,0,0))

def select_surface():
    """Simple surface selection for turn timing"""
    print("\nSelect surface type:")
    surfaces = ["carpet", "hardwood", "tile", "concrete", "rubber", "grass"]
    
    for i, surface in enumerate(surfaces, 1):
        timing = PWM.surface_timings[surface]
        print(f"  {i}. {surface.capitalize()} ({timing}s)")
    
    while True:
        try:
            choice = int(input("Enter choice (1-6): "))
            if 1 <= choice <= 6:
                selected = surfaces[choice - 1]
                PWM.set_surface_type(selected)
                return selected
            else:
                print("Please enter 1-6")
        except (ValueError, KeyboardInterrupt):
            print("Using default: carpet")
            PWM.set_surface_type("carpet")
            return "carpet"

if __name__ == '__main__':
    print('Obstacle avoidance starting')
    
    # Select surface type
    surface = select_surface()
    print(f"Surface: {surface}")
    time.sleep(1)
    
    # Stuck detection variables
    distance_history = []
    stuck_threshold = 5  # Number of identical readings to trigger failsafe
    stuck_tolerance = 2  # Allow 2cm difference to account for sensor noise
    
    try:
        #blink white when starting
        for i in range(3):
           led.colorWipe(led.strip, Color(255,255,255))
           time.sleep(0.2)
           led.colorWipe(led.strip, Color(0,0,0))
           time.sleep(0.1)
           
        
        #object avoidance loop
        while True:
            try:
                raw_distance = ultrasonic.get_distance()
                if raw_distance is None:
                    print("No distance reading")
                    continue
                distance = int(raw_distance)
                if distance <= 0:
                    print("Invalid distance reading")
                    continue
            except (ValueError, TypeError) as e:
                print(f"Distance measurement error: {e}")
                continue
            except Exception as e:
                print(f"Ultrasonic sensor error: {e}")
                continue
            
            print("Obstacle distance is {}CM".format(distance))
            
            # Stuck detection
            if distance < MAX_RANGE:
                distance_history.append(distance)
                if len(distance_history) > stuck_threshold:
                    distance_history.pop(0)
            
            if len(distance_history) >= stuck_threshold:
                distances_similar = all(
                    abs(d - distance_history[0]) <= stuck_tolerance 
                    for d in distance_history
                )
                if distances_similar and distance_history[0] > THRESH_EMERGENCY:
                    print("Same distance readings - executing failsafe")
                    led.colorWipe(led.strip, Color(255,165,0))  # Orange
                    time.sleep(0.5)
                    reverse_and_turn()
                    distance_history.clear()
                    continue
            
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
