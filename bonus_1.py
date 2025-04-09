# Find the average distances for the front, right, and left sensors
from hcsr04 import HCSR04 # Must have this library saved on Pico to work
from time import sleep
from machine import Pin
from time import sleep

# Front Sensor
# Initialize sensor with trigger and echo pins
sensor = HCSR04(trigger_pin=5, echo_pin=6)
#Sensor right
sensor_r = HCSR04(trigger_pin=19, echo_pin=18)
#Sensor Left
sensor_l = HCSR04(trigger_pin=28, echo_pin=27)

# Reed swich on pin 0 using internal pull down resistor, other wire of switch connects to 3.3V
reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
led = Pin('LED', Pin.OUT)
reed_average = []

# Servos 
from servo import Servo # Save this file on pico

servo_reed = Servo(Pin(15))

servo_payload = Servo(Pin(22))

servo_step = Servo(Pin(10))

from machine import Pin
from time import sleep

# Initialize input with internal pull down resistor on pin 10
# When using internal pull down resistor on Pico, pin will have logic level 1 (3.3 V) when button pushed and 0 when released
# FOr internal pull up resistor, pin will have logic level 0 when button pushed and 1 (3.3 V) when released
#ssss
button = Pin(1, Pin.IN, Pin.PULL_DOWN)

# Initialize on board LED
led = Pin('LED', Pin.OUT)
but = []

from machine import ADC
from time import sleep

# IR Photodiode on analog pin 28
# NOTE: It may help to use Thonny's built in plotter to see how the values change. Find it under 'View'

ir = ADC(26)
# You can also use the IR Photodiode as a digital input.
ir_sensor = []

#Motor Driver Sample Code
from machine import Pin, PWM
from time import sleep

# === L298N Motor Driver ===
# Motor A
motor_a_in1 = Pin(7, Pin.OUT)
motor_a_in2 = Pin(9, Pin.OUT)
motor_a_en = PWM(Pin(8))
motor_a_en.freq(1000)
motor_a_correction = 1 # Adjust so both motors have same speed

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

# Variables
speed = 35
average_front = []
average_right = []
average_left = []

# Preset distances
front_dis = 100
right_dis = 1
left_dis = 25


def turn_left():
    # Turn Left
    motor_a('forward', speed)
    sleep(.72)
    print('turn left')
    motor_a()
    sleep(2)
    return

def turn_right():
    # Turn Right
    motor_b('forward', speed)
    sleep(.74)
    print('Turn Right')
    motor_b()
    sleep(2)
    return

def go_straight():
    motor_a('forward', speed)
    motor_b('forward', speed)
    sleep(.5)
    
def go_straight1():
    motor_a('forward', speed)
    motor_b('forward', speed)
    print('straight')
    sleep(5)

    
def stop():
    motor_a()
    motor_b()
    print('stop')
    sleep(2)

def pickup():
    # stepper motor rotate back and pickup
    servo_payload.move(0)
    print('move servo for payload out the way')
    sleep(1)
    servo_step.move(30)
    print('pickup the pay load')
    sleep(1)
    return

def drop():
    servo_payload.move(30)
    servo_step.move(24)
    sleep(1)
    servo_payload.move(45)
    servo_step.move(15)
    sleep(1)
    servo_payload.move(60)
    servo_step.move(12)
    sleep(1)
    servo_payload.move(90)
    servo_step.move(11)
    sleep(1)
    
    motor_a('backward', speed)
    motor_b('backward', speed)
    sleep(2)

# Main Code
# Find the wall behind us and turn onto the wall for wall-following
sleep(1)
# Main Code
# Find the wall behind us and turn onto the wall for wall-following

# Main Code P.2
while True:
    pickup()
    go_straight1()
    stop()
    drop()
    stop()
    break

