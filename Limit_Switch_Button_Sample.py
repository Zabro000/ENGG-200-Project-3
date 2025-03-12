from machine import Pin
from time import sleep

# Initialize input with internal pull down resistor on pin 10
# When using internal pull down resistor on Pico, pin will have logic level 1 (3.3 V) when button pushed and 0 when released
# FOr internal pull up resistor, pin will have logic level 0 when button pushed and 1 (3.3 V) when released

button = Pin(10, Pin.IN, Pin.PULL_DOWN)

# Initialize on board LED
led = Pin('LED', Pin.OUT)

while True:
    
    # if button pushed turn on LED
    if button.value() == 1:
        print("Button Pressed!")
        led.on()
    else:
        led.off()
    
    sleep(0.1) # Short delay