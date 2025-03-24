# Find the average distances for the front, right, and left sensors
from hcsr04 import HCSR04 # Must have this library saved on Pico to work
from time import sleep
from machine import Pin
from time import sleep

# Front Sensor
# Initialize sensor with trigger and echo pins
sensor = HCSR04(trigger_pin=21, echo_pin=20)
#Sensor right
sensor_r = HCSR04(trigger_pin=19, echo_pin=18)
#Sensor Left
sensor_l = HCSR04(trigger_pin=17, echo_pin=16)

average_front = []
average_right = []
average_left = []

# Reed swich on pin 0 using internal pull down resistor, other wire of switch connects to 3.3V
reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
led = Pin('LED', Pin.OUT)
reed_average = []

from machine import Pin
from time import sleep

# Initialize input with internal pull down resistor on pin 10
# When using internal pull down resistor on Pico, pin will have logic level 1 (3.3 V) when button pushed and 0 when released
# FOr internal pull up resistor, pin will have logic level 0 when button pushed and 1 (3.3 V) when released
#ssss
button = Pin(10, Pin.IN, Pin.PULL_DOWN)

# Initialize on board LED
led = Pin('LED', Pin.OUT)
but = []

from machine import I2C, Pin 
from imu import MPU6050 # Save this library on Pico
import time

# Pins according the schematic https://heltec.org/project/wifi-kit-32/
# Replace with proper scl and sda pins
i2c = I2C(1, scl=Pin(3), sda=Pin(2))


'''
# Accelerometer / Gyroscope
imu = MPU6050(i2c)
accel_x = []
accel_y = []
accel_z = []
gyro_x = []
gyro_y = []
gyro_z = []
temp = []
'''

from machine import ADC
from time import sleep

# IR Photodiode on analog pin 28
# NOTE: It may help to use Thonny's built in plotter to see how the values change. Find it under 'View'

ir = ADC(28)
# You can also use the IR Photodiode as a digital input.
ir_sensor = []

#Main Code
#Turn Car around and find the wall behind 


while True:
    # Front Sensor
    try:
        distance = sensor.distance_cm()
        print('Distance:', distance, 'cm')
        sleep(0.1) # sensor doesn't work well without delay
        average_front.append(distance)

        if len(average_front) == 5:
            front_dis = sum(average_front) / 5
            print(front_dis, "average front")
            average_front = []

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break

    #Right Sensor
    try:
        distance_r = sensor_r.distance_cm()
        print('Distance:', distance_r, 'cm')
        sleep(0.1) # sensor doesn't work well without delay
        average_right.append(distance_r)

        if len(average_right) == 5:
            right_dis = sum(average_right) / 5
            print(right_dis, "average right")

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break

    #Left Sensor
    try:
        distance_l = sensor_l.distance_cm()
        print('Distance:', distance_l, 'cm')
        sleep(0.1) # sensor doesn't work well without delay
        average_left.append(distance_l)

        if len(average_left) == 5:
            left_dis = sum(average_left) / 5
            print(left_dis, "average left")

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break

    #Reed Switch
    if reed_switch.value() == 1:  # Check if the magnet is near
        led.value(1)# Turn on the LED
        
    else:
        led.value(0)  # Turn off the LED
       
    print(reed_switch.value())

    #Take average 
    reed_average.append(reed_switch.value())
    if len(reed_average) == 5:
        if sum(reed_average) == 5:
            print("Payload detected")
            magnet = 1
        else:
            print("Payload not Detected")
            magnet = 0
        reed_average = []
    
    sleep(0.1)  # Short delay

    #Limit Switch
    # if button pushed turn on LED
    if button.value() == 1:
        print("Button Pressed!")
        led.on()
    else:
        print("Not Pressed")
        led.off()
    
    but.append(button.value())
    if len(but) == 5:
        if sum(but) == 5:
            print("Payload on")
            payload_stay = 1
        but = []
    
    sleep(0.1) # Short delay

    '''
    # MPU
    accel_x.append(imu.accel.x)
    accel_y.append(imu.accel.y)
    accel_z.append(imu.accel.z)

    gyro_x.append(imu.gyro.x)
    gyro_y.append(imu.gyro.y)
    gyro_z.append(imu.gyro.z)

    temp.append(imu.temperature)

    time.sleep(.1)
    '''
    #IR sensor
    print(ir.read_u16())

    ir_sensor.append(ir.read_u16())
    if len(ir_sensor) == 5:
        if sum(ir_sensor) < 50000:
            print("Dropoff Detected")
        else:
            print("Dropoff not detected")

        ir_sensor = []
    
    sleep(0.1)




#asasdas

