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
i2c = I2C(22, scl=Pin(26), sda=Pin(27))
 

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

#Motor Driver Sample Code
from machine import Pin, PWM
from time import sleep

# === L298N Motor Driver ===
# Motor A
motor_a_in1 = Pin(6, Pin.OUT)
motor_a_in2 = Pin(7, Pin.OUT)
motor_a_en = PWM(Pin(8))
motor_a_en.freq(1000)
motor_a_correction = 1.0 # Adjust so both motors have same speed

# Motor B
motor_b_in3 = Pin(4, Pin.OUT)
motor_b_in4 = Pin(3, Pin.OUT)
motor_b_en = PWM(Pin(2))
motor_b_en.freq(1000)
motor_b_correction = 1.0 # Adjust so both motors have same speed

# Function to control Motor A
def motor_a(direction = "stop", speed = 0):
    adjusted_speed = int(speed * motor_a_correction)  # Apply correction
    if direction == "forward":
        motor_a_in1.value(0)
        motor_a_in2.value(1)
    elif direction == "backward":
        motor_a_in1.value(1)
        motor_a_in2.value(0)
    else:  # Stop
        motor_a_in1.value(0)
        motor_a_in2.value(0)
    motor_a_en.duty_u16(int(adjusted_speed * 65535 / 100))  # Speed: 0-100%

# Function to control Motor B
def motor_b(direction = "stop", speed = 0):
    adjusted_speed = int(speed * motor_b_correction)  # Apply correction
    if direction == "forward":
        motor_b_in3.value(1)
        motor_b_in4.value(0)
    elif direction == "backward":
        motor_b_in3.value(0)
        motor_b_in4.value(1)
    else:  # Stop
        motor_b_in3.value(0)
        motor_b_in4.value(0)
    motor_b_en.duty_u16(int(adjusted_speed * 65535 / 100))  # Speed: 0-100%

#Stepper Motor
import stepper # must have this file saved on Pico
from time import sleep

# Define the stepper motor pins
IN1 = 12
IN2 = 13
IN3 = 14
IN4 = 15

# Initialize the stepper motor
stepper_motor = stepper.HalfStepMotor.frompins(IN1, IN2, IN3, IN4)

# Set the current position as position 0
stepper_motor.reset()

#Main Code

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
            magnet = 1
            print("Payload detected")

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
        limit = 1
    else:
        print("Not Pressed")
        limit = 0
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
        if sum(ir_sensor) > 40000:
            print("Dropoff Detected")
        else:
            print("Dropoff not detected")

        ir_sensor = []
    
    sleep(0.1)


#asasdas

