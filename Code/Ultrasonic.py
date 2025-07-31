import RPi.GPIO as GPIO
import time

class Ultrasonic:
    def __init__(self, trigger_pin=27, echo_pin=22, max_distance=300):
        GPIO.setwarnings(False)
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.MAX_DISTANCE = max_distance
        self.timeOut = self.MAX_DISTANCE * 60
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
    
    def pulseIn(self, pin, level, timeOut):
        t0 = time.time()
        while GPIO.input(pin) != level:
            if (time.time() - t0) > timeOut * 0.000001:
                return 0
        t0 = time.time()
        while GPIO.input(pin) == level:
            if (time.time() - t0) > timeOut * 0.000001:
                return 0
        pulseTime = (time.time() - t0) * 1000000
        return pulseTime
    
    def get_distance(self):
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, GPIO.LOW)
        pingTime = self.pulseIn(self.echo_pin, GPIO.HIGH, self.timeOut)
        distance = pingTime * 340.0 / 2.0 / 10000.0  # cm
        return distance if distance > 0 else None

    def close(self):
        GPIO.cleanup()

if __name__ == "__main__":
    ultrasonic = Ultrasonic()
    try:
        print("Program is starting ...")
        while True:
            dist = ultrasonic.get_distance()
            if dist is not None:
                print(f"Ultrasonic distance: {dist:.2f} cm")
            else:
                print("No distance measurement")
            time.sleep(0.5)
    except KeyboardInterrupt:
        ultrasonic.close()
        print("\nEnd of program")
