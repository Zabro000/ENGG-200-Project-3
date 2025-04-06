from machine import Pin
from time import sleep

# Reed swich on pin 0 using internal pull down resistor, other wire of switch connects to 3.3V
reed_switch = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin(11, Pin.OUT)
reed_average = []

while True:
    #Take average 
    reed_average.append(reed_switch.value())
    if len(reed_average) == 5:
        if sum(reed_average) == 5:
            print("Payload not Detected")
            magnet = 0
            led.value(0)

        else:
            magnet = 1
            print("Payload detected")
            led.value(1)
        reed_average = []
    
    sleep(0.05)  # Short delay