# Adapted from Freenove Tank Robot Kit for Raspberry Pi
# (c) Freenove Creative Technology Co., Ltd., used under CC BY-NC-SA 3.0 license

import RPi.GPIO as GPIO
import time
import pigpio
import threading

from Led import Led

class Motor:
    def __init__(self):
        self.pwm1 = 24
        self.pwm2 = 23
        self.pwm3 = 5
        self.pwm4 = 6         
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
        if duty>0:
            self.PwmServo.set_PWM_dutycycle(self.pwm1,0)
            self.PwmServo.set_PWM_dutycycle(self.pwm2,duty)
        elif duty<0:
            self.PwmServo.set_PWM_dutycycle(self.pwm1,abs(duty))
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
        
PWM=Motor()
LED = Led()

def loop():
    time.sleep(30) #get into position
    light_thread = threading.Thread(target=LED.policeLightsThreaded, args=(10, 0.1))
    light_thread.start()
    for i in range(5):
        PWM.setMotorModel(2000,2000)        #Forward
        time.sleep(1)
        PWM.setMotorModel(-2000,-2000)      #Back
        time.sleep(1)
    PWM.setMotorModel(0,0)          #Stop
    time.sleep(1)
    
    
def destroy():
    PWM.setMotorModel(0,0)

if __name__=='__main__':
    print ('Program is starting ... \n')
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
