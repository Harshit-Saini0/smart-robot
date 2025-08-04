# Adapted from Freenove Tank Robot Kit for Raspberry Pi
# (c) Freenove Creative Technology Co., Ltd., used under CC BY-NC-SA 3.0 license

import RPi.GPIO as GPIO
import pigpio
import time


class Motor:
    def __init__(self, left_motor_calibration=0.9):
        self.pwm1 = 24
        self.pwm2 = 23
        self.pwm3 = 5
        self.pwm4 = 6
        
        self.surface_timings = {
            "carpet": 0.93,
            "hardwood": 0.75,
            "tile": 0.70,
            "concrete": 0.85,
            "rubber": 0.80,
            "grass": 1.10,
            "default": 0.68
        }

        self.left_motor_calibration = left_motor_calibration
        
        self.PwmServo = pigpio.pi()
        self.PwmServo.set_mode(self.pwm1,pigpio.OUTPUT) 
        self.PwmServo.set_mode(self.pwm2,pigpio.OUTPUT) 
        self.PwmServo.set_mode(self.pwm3,pigpio.OUTPUT) 
        self.PwmServo.set_mode(self.pwm4,pigpio.OUTPUT)         
        self.PwmServo.set_PWM_frequency(self.pwm1,50)
        self.PwmServo.set_PWM_frequency(self.pwm2,50)
        self.PwmServo.set_PWM_frequency(self.pwm3,50)
        self.PwmServo.set_PWM_frequency(self.pwm4,50)        
        self.PwmServo.set_PWM_range(self.pwm1, 4095)
        self.PwmServo.set_PWM_range(self.pwm2, 4095)
        self.PwmServo.set_PWM_range(self.pwm3, 4095)
        self.PwmServo.set_PWM_range(self.pwm4, 4095)
    
    def set_left_motor_calibration(self, calibration):
        self.left_motor_calibration = max(0.1, min(1.5, calibration))
        print(f"Left motor calibration set to: {self.left_motor_calibration}")
    
    def set_surface_type(self, surface):
        """Set the surface type for turn timing calibration"""
        if surface.lower() in self.surface_timings:
            self.current_surface = surface.lower()
            print(f"Surface type set to: {self.current_surface} (turn time: {self.surface_timings[self.current_surface]}s)")
        else:
            available_surfaces = ", ".join(self.surface_timings.keys())
            print(f"Unknown surface '{surface}'. Available surfaces: {available_surfaces}")
    
    def get_turn_time(self, surface=None):
        """Get the turn time for a specific surface or current surface"""
        if surface:
            return self.surface_timings.get(surface.lower(), self.surface_timings["default"])
        return self.surface_timings.get(getattr(self, 'current_surface', 'default'), self.surface_timings["default"])
    
    def duty_range(self,duty1,duty2):
        if duty1>4095:
            duty1=4095
        elif duty1<-4095:
            duty1=-4095        
        if duty2>4095:
            duty2=4095
        elif duty2<-4095:
            duty2=-4095
        return duty1,duty2
    
    def left_Wheel(self,duty):
        calibrated_duty = int(duty * self.left_motor_calibration)
        if calibrated_duty>0:
            self.PwmServo.set_PWM_dutycycle(self.pwm1,0)
            self.PwmServo.set_PWM_dutycycle(self.pwm2,calibrated_duty)
        elif calibrated_duty<0:
            self.PwmServo.set_PWM_dutycycle(self.pwm1,abs(calibrated_duty))
            self.PwmServo.set_PWM_dutycycle(self.pwm2,0)
        else:
            self.PwmServo.set_PWM_dutycycle(self.pwm1,0)
            self.PwmServo.set_PWM_dutycycle(self.pwm2,0)

    def right_Wheel(self,duty):
        if duty>0:
            self.PwmServo.set_PWM_dutycycle(self.pwm3,0)
            self.PwmServo.set_PWM_dutycycle(self.pwm4,duty)
        elif duty<0:
            self.PwmServo.set_PWM_dutycycle(self.pwm3,abs(duty))
            self.PwmServo.set_PWM_dutycycle(self.pwm4,0)
        else:
            self.PwmServo.set_PWM_dutycycle(self.pwm3,0)
            self.PwmServo.set_PWM_dutycycle(self.pwm4,0)

    def setMotorModel(self,duty1,duty2):
        duty1,duty2=self.duty_range(duty1,duty2)
        self.left_Wheel(duty1)
        self.right_Wheel(duty2)
    
    def turn_left_90(self, surface=None):
        turn_time = self.get_turn_time(surface)
        surface_name = surface or getattr(self, 'current_surface', 'default')
        print(f"Executing 90-degree left turn on {surface_name} surface ({turn_time}s)")
        self.setMotorModel(-3000, 3000)
        time.sleep(turn_time)
        self.setMotorModel(0, 0)

    def turn_right_90(self, surface=None):
        turn_time = self.get_turn_time(surface)
        surface_name = surface or getattr(self, 'current_surface', 'default')
        print(f"Executing 90-degree right turn on {surface_name} surface ({turn_time}s)")
        self.setMotorModel(3000, -3000) 
        time.sleep(turn_time)
        self.setMotorModel(0, 0)

def destroy():
    PWM.setMotorModel(0,0)

if __name__ == "__main__":
    import time

    TURN_DURATION = 2

    PWM = Motor()

    try:
        while(True):
            mode = input("Enter mode ([F]orward, [B]ackward, [T]urn, [C]alibrate, [S]urface, [9L] 90 Left, [9R] 90 Right): ").strip().lower()
            if mode == "f":
                speed = int(input("Enter speed (0-4095): "))
                print(f"Moving forward with speed {speed}")
                PWM.setMotorModel(speed, speed)
            elif mode == "b":
                speed = int(input("Enter speed (0-4095): "))
                print(f"Moving backward with speed {speed}")
                PWM.setMotorModel(-speed, -speed)
            elif mode == "c":
                current_cal = PWM.left_motor_calibration
                print(f"Current left motor calibration: {current_cal}")
                try:
                    new_cal = float(input("Enter new calibration value (0.1-1.5): "))
                    PWM.set_left_motor_calibration(new_cal)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                continue  
            elif mode == "s":
                print("Available surfaces:")
                for surface, timing in PWM.surface_timings.items():
                    print(f"  {surface}: {timing}s")
                surface_choice = input("Enter surface type: ").strip()
                PWM.set_surface_type(surface_choice)
                continue
            elif mode == "9l":
                PWM.turn_left_90()
                continue  # don't sleep here 
            elif mode == "9r":
                PWM.turn_right_90()
                continue  # don't sleep here
            elif mode == "t":
                direction = input("Enter turn direction ([L]eft, [R]ight): ").strip().lower()
                TURN_DURATION = float(input("Enter duration for the turn (in seconds): "))
                speed = 3000
                if direction == "l":
                    print(f"Turning left with ({-speed}, {speed}) for {TURN_DURATION} second(s)")
                    PWM.setMotorModel(-speed, speed)
                elif direction == "r":
                    print(f"Turning right with ({speed}, {-speed}) for {TURN_DURATION} second(s)")
                    PWM.setMotorModel(speed, -speed)
            time.sleep(TURN_DURATION)
            PWM.setMotorModel(0, 0)
            print("-" * 40)
            time.sleep(0.5)
    except KeyboardInterrupt:
        PWM.setMotorModel(0, 0)
    except Exception as e:
        PWM.setMotorModel(0, 0)
        print(e)

