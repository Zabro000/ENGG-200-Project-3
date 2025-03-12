from machine import ADC
from time import sleep

# IR Photodiode on analog pin 28
# NOTE: It may help to use Thonny's built in plotter to see how the values change. Find it under 'View'

ir = ADC(28)
# You can also use the IR Photodiode as a digital input.

while True:
    print(ir.read_u16())
    
    sleep(0.1)