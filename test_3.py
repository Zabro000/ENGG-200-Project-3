from machine import Pin, PWM
from time import sleep

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

# === L298N Motor Driver ===
# Motor A
motor_a_in1 = Pin(13, Pin.OUT)
motor_a_in2 = Pin(15, Pin.OUT)
motor_a_en = PWM(Pin(14))
motor_a_en.freq(1000)
motor_a_correction = .96 # Adjust so both motors have same speed

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

sleep(5)

# Example
# turn to start the sequence

front_dis = 100
# find the distance from the wall once turned around
while True:
    # Front Sensor
    try:
        distance = sensor.distance_cm()
        print('Distance:', distance, 'cm')
        sleep(0.01) # sensor doesn't work well without delay
        average_front.append(distance)
    
        if len(average_front) == 5:
            front_dis = sum(average_front) / 5
            print(front_dis, "average front")
            average_front = []

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break
    
    if front_dis > 25:
        motor_a('forward', 50)
        motor_b('forward', 50)
        print('go to wall')

    else:
        motor_a()
        motor_b()
        print('at wall')
        break
