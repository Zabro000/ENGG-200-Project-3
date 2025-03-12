from machine import Pin
from time import sleep

line_sen = Pin(10, Pin.IN)

# You may need to change the sensitivity of the IR Proximity sensor using the built in potentiometer.
# NOTE: Test the sensor using the built in LED to determine the actvation range.

while True:
    print(line_sen.value())
    
    if line_sen.value() == 0:
        print("black line found!")
    
    sleep(0.1)