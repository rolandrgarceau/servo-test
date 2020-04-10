import RPi GPIO as GPIO
import time
# we can port this to a ESC for a motor. 3 lines. Direction Duration Frequency?
# this is a servo linear test for an automated min to max sweeping test. 
# remember cleanup not like arduino
# 2 pin refrences numerical or BCM
GPIO.setmode(GPIO.BOARD)
#PWM used pin 11 check for specific pin tied to register for timer or pwm
servoPin=11
GPIO.setup(servoPin, GPIO.OUT)
# pwm=GPIO.PWM(servoPin,50) # sets a 50 Hz frequency
#duty cycle use start(val)
#look for full left position if it were a servo
#pwm.start(5)
#pwm.ChangeDutyCycle() after initial start
#goto 180 different positions then come back
#see notes on tweaking the position via duty cycle formula
#DC cast as int? no, force the slope to convert to floating point with dot ('.')
#to make it go slow add a sleep and import time- yup?
#might have issues with () in formula
for i in range(0,180):
    #allow for user to test it with desired... input from stdin?
    #desiredPosition=input("what position you wish to place from 0-180 degrees? ")
    #DC=(1./18.)*(desiredPosition)+2
    #now just automate it with i
    DC=(1./18.)*(i)+2
    pwm.ChangeDutyCycle(DC)
    time.sleep(.05)#sleep is in seconds can handle faster at .01 but not much more
#might need -1 (one) to decrement 180 iterations does it pre-decrement? --i or i--?
for i in range(180,0,-1):#needed 3rd param to decrement- silent fail....ssshhh!
    DC=(1./18.)*(i)+2
    pwm.ChangeDutyCycle(DC)
    time.sleep(.05)
#clear out the board for next test or remove these two in prod if needed.
#arduino days we did if(DEV_MODE flag was set){stop;cleanup;}else;....
pwm.stop()
GPIO.cleanup()
