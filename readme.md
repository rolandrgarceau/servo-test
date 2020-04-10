# Servo Test In Python

My first take at using Python and RPi GPIO was a bit different than using an Arduino and C. The same general principles hold true for PWM. There is a frequency and a duty cycle. The time for each to achieve full actuation is what needed to be learned here. The R&D of this script was for the movement of a camera gimbal in an underwater housing.

## Further video series with [Paul McWhorter](https://www.youtube.com/channel/UCfYfK0tzHZTpNFrc_NDKfTA)

His high school team building weather balloons which use [servos](https://www.youtube.com/watch?v=SGwhx1MYXUs) is truly amazing. Their use of Raspberry Pis were for data collection at 110K feet using radio telemetry. their project used 2.39 GHz microwave signal radio transmissions to track GPS emitted from a balloon via HAM over ethernet. This allowed their team to maintain down range connection of 70 miles. 

## How to read this repo

If one is looking at this repo for guidance or refresher, go back to Paul's lesson 27 on PWM that describes how to use GPIO on the Pi.

## Notes on how this testing happened

### tl;dr:

```py
pwm.start(value) # will initiate the "write" to pin
# values are the duty cycle percentage
pwm.ChangeDutyCycle(val) # is used after initial call to start
# dont forget to cleanup the GPIO on pi when done with tests.
pwm.stop()
GPIO.cleanup()
```

### Choose the OS and distribution

We will need to test operation of the servo with python in shell with sudo if working directly on a Pi. sudo will be able to write to pins- where the default pi user may not do it, depending on the OS version. The main consideration is that we have the RPi GPIO available so upgrade and update the install and verify all python tooling needed. I believe I had used Noobs and Raspbian Stretch or Jesse, but if working this project today, one should consult the documentation and do the needed footwork to get a suitable distro for controlling motors with a Pi. 

## Basic operation and testing notes

* Most basic servos like to see 50 Hz frequency PWM control signal.
* Check specs of your servo for your details- it might be 60Hz
* duty cycle "on" dictates the position (in percentage on)
* for board you have to pwm.start(val) with a duty cycle (val) parameter

pwm.start(val) with val in percentage of 100 & calculated as followed. This may not be an exact science here as I was pulling a servo off a shelf from hobby projects from *years* ago and had no data sheet on it.

If we want to change the cycle after its started use:

```py
changeDutyCycle(val)
```

## A little math

period = 1/frequency for one full period
period = 1/50Hz or around .02 or 20 milliseconds

For full left position it may need 5% duty cycle. The duty cycle 5% (in percentage, as '%' prog char is modulo) is calculated like this:

.05(five percent)x20(milliseconds)=1 millisecond

* Most servos are full left at 1 msec pulse width (check yours might be different)

Run the `pwm.start(5)` and see if it is full left.

* If it didn't do it try 1, then 2, then 3.

* Don't forget changeDutyCycle after the first start.

* cleanup GPIO on pi if you are done in python shell/interactive/IDLE or venv
* You may have to restart or try a few times to see it get to the middle position
* My middle position at about 1.5msec pulse width (period above) with duty cycle 7.5%

This translates with:

.075(percentage to use)x20 = 1.5

And we would be running `pwm.start(7.5)` but it may round (7) or (8) only or take int param see doc for current implementation details.

Full right @ 2msec needs a 10% duty cycle

.1(duty)x20millisec=2msec (pulse @ 50 Hz)

### Recap actual testing

In actual test the `pwm.ChangeDutyCycle(1)` and `pwm.ChangeDutyCycle(2)`
were really the full left (at 3 we noticed a movement from all the way left)
center was 7 and right was 12. 1 as far left then 12 as far right etc...

One could go back, change the 50 Hz and then re-test, or live with that so long as it wont do harm to the components- verify against specs. Paul approached this by choosing to take inner boundary numbers 2 and 11 to continue building on.

We can look at the test as our "map" to the actual hardware and then figure
out how we will hard-code the ROV to say, move the camera gimbal if we wanted to incorporate that functionality- or better yet an extendable arm- yeah. And waterproof...

Paul's notes looked at making degree settings and points
using 0 to 180 degrees as input and it outputs the proper duty cycle to achieve this desired position.

0 degrees = full left = point(0,2)
180 degrees = full right = point(180,11)

using point slope formula we get about 1/18:

m = (y2-y1)/(x2-x1) = (11 (or 12 was far right) - 2)/(180-0) = 9/180 or 10/180
then plug it in to the
y - y1 = m(x - x1)
for point(0,2)
y - 2 = 1/18(x - 0)
y = 1/18x + 2

So if we put in the degree desired position as x the resulting y is the
duty cycle which will yield that position. Now the formula should look like this:

DutyCycle = 1/18 * (desired angle) + 2.

### Final thought
It's ironic how I considered this a mindless task at one point- like painting a wall- when there are many of us out there that struggle to ever get to be able to understand what PWM or input pullup for pinmode would do in the first place... After you do it enough it becomes second nature regardless of language or platform.

Happy hacking y'all...:)




