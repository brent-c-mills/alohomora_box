# This code is written for a QTPYRP2040 as the primary board, a VCNL4040 as the primary light and proximity sensor,
# a micro servo motor, and a series of LEDs (I used 4x nOOds flexible LED filaments).
# Also used in this project but not visible in the code are a 5v wireless induction charging coil, a wireless LED, 
# a custom-made wooden box, a custom-made wooden wand, a small brass latch, and some braided fishing line. Diagram to follow

import time
import board
import busio
import adafruit_vcnl4040
import pwmio
import adafruit_motor
from adafruit_motor import servo
import digitalio
from digitalio import DigitalInOut, Direction

i2c = board.STEMMA_I2C()
exteriorsensor = adafruit_vcnl4040.VCNL4040(i2c)
led = digitalio.DigitalInOut(board.A0)
led.direction = Direction.OUTPUT
timer = 0
pwm = pwmio.PWMOut(board.A3, duty_cycle=2 ** 15, frequency=50)
latch = servo.Servo(pwm)

while True:
    # print statements for debugging on the console if this thing ever goes sideways
    print("Proximity:", exteriorsensor.proximity)
    print("Light: %d lux" % exteriorsensor.lux)
    
    # Proximity must be close enough to trigger the wireless LED, which would also block light on the sensor. 
    # Only the wireless LED (or a flashlight) at the correct distance will open the lock.
    if exteriorsensor.proximity > 75 and exteriorsensor.lux > 500:
        # Turn on the interior LEDs
        led.value = True
        # Start the timer
        timer = 0
        # rotate the servo briefly to unlock the hidden latch
        latch.angle = 60
        time.sleep(0.5)
        # reset the servo so the box can close again
        latch.angle = 0

    if timer > 20:
        # Turn off the LEDs to preserve battery
        # Eventually I'll add a second light sensor on the interior of the box to start this timer
        led.value = False
    time.sleep(1.0)
    
    # increment the timer
    timer += 1
