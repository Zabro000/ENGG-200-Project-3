from machine import Pin
from time import sleep

# Reed swich on pin 0 using internal pull down resistor, other wire of switch connects to 3.3V
reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
led = Pin('LED', Pin.OUT)

while True:
    if reed_switch.value() == 1:  # Check if the magnet is near
        led.value(1)# Turn on the LED
        
    else:
        led.value(0)  # Turn off the LED
       
    
    print(reed_switch.value())
    sleep(0.1)  # Short delay