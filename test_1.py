# IR Photodiode on analog pin 28
# NOTE: It may help to use Thonny's built in plotter to see how the values change. Find it under 'View'
from machine import Pin, PWM, ADC
from time import sleep

led = Pin(11, Pin.OUT)   
ir = ADC(28)
# You can also use the IR Photodiode as a digital input.
ir_sensor = []
#IR sensor
while True:
    print(ir.read_u16())

    ir_sensor.append(ir.read_u16())
    if len(ir_sensor) == 5:
        if sum(ir_sensor) > 40000:
            print("Dropoff Detected")
            led.value(1)# Turn on the LED

        else:
            print("Dropoff not detected")
            led.value(0)  # Turn off the LED

        ir_sensor = []

    sleep(0.1)