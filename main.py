# Find the average distances for the front, right, and left sensors
from hcsr04 import HCSR04 # Must have this library saved on Pico to work
from time import sleep

# Front Sensor
# Initialize sensor with trigger and echo pins
sensor = HCSR04(trigger_pin=21, echo_pin=20)

average_front = []
while True:
    try:
        distance = sensor.distance_cm()
        print('Distance:', distance, 'cm')
        sleep(0.1) # sensor doesn't work well without delay
        average_front.append(distance)

        if len(average_front) == 10:
            front_dis = sum(average_front) / 10
            print(front_dis, "average front")
            average_front = []

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break

#Sensor right
sensor_r = HCSR04(trigger_pin=19, echo_pin=18)

average_right = []
while True:
    try:
        distance_r = sensor.distance_cm()
        print('Distance:', distance_r, 'cm')
        sleep(0.1) # sensor doesn't work well without delay
        average_right.append(distance_r)

        if len(average_right) == 10:
            right_dis = sum(average_right) / 10
            print(right_dis, "average right")

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break

#Sensor Left
sensor_r = HCSR04(trigger_pin=17, echo_pin=16)

average_left = []
while True:
    try:
        distance_l = sensor.distance_cm()
        print('Distance:', distance_l, 'cm')
        sleep(0.1) # sensor doesn't work well without delay
        average_left.append(distance_l)

        if len(average_left) == 10:
            left_dis = sum(average_left) / 10
            print(left_dis, "average left")

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break
    
from machine import Pin
from time import sleep

# Reed swich on pin 0 using internal pull down resistor, other wire of switch connects to 3.3V
reed_switch = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin('LED', Pin.OUT)

reed_average = []
while True:

    if reed_switch.value() == 1:  # Check if the magnet is near
        led.value(1)# Turn on the LED

        
    else:
        led.value(0)  # Turn off the LED
       
    
    print(reed_switch.value())
    sleep(0.1)  # Short delay




if __name__ == "__main__":
    main()
