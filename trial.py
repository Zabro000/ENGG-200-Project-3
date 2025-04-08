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
motor_a_correction = .94 # Adjust so both motors have same speed

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
    sleep(1)

def stop_2():
    motor_a()
    motor_b()
    sleep(.5)
    
def stop():
    motor_a()
    motor_b()
    print('stop')
    
def go_straight_2():
    motor_a('forward', speed)
    motor_b('forward', speed)
    sleep(.2)    

# Code for wall folowing
def go_to_payload():
    but = []
    average_front = []
    average_right = []
    average_left = []
    ir_sensor = []
    reed_average = []
    front_dis = 50
    right_dis = 15
    i = 0
    reed = 0 
    ir = 0

    while True:
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

        # Front Sensor
        try:
            distance = sensor.distance_cm()
            print('Distance:', distance, 'cm')
            if distance > 0 :
                average_front.append(distance)
        
            if len(average_front) == 10:
                front_dis = sum(average_front) / 10
                print(front_dis, "average front")
                average_front = []

        except OSError as ex:
            print('ERROR getting distance:', ex)
            break

        # Right Sensor
        try:
            distance_r = sensor_r.distance_cm()
            print('Distance Right:', distance_r, 'cm')
            average_right.append(distance_r)

            if len(average_right) == 10:
                right_dis = sum(average_right) / 10
                print(right_dis, "average right")
                average_right = []

        except OSError as ex:
            print('ERROR getting distance:', ex)
            break

        # Left Sensor
        '''
        try:
            distance_l = sensor_l.distance_cm()
            print('Distance Left:', distance_l, 'cm')
            sleep(0.01) # sensor doesn't work well without delay
            average_left.append(distance_l)

            if len(average_left) == 5:
                left_dis = sum(average_left) / 5
                print(left_dis, "average left")
                average_left = []
        '''

        # Photodiode
        ir_sensor.append(ir.read_u16())
        if len(ir_sensor) == 5:
            if sum(ir_sensor) > 40000:
                print("Dropoff Detected")
                reed = 1
            else:
                print("Dropoff not detected")
                reed = 0

            ir_sensor = []

        reed_average.append(reed_switch.value())

        if len(reed_average) == 5:
            if sum(reed_average) == 5:
                reed = 1
                print("Payload detected")

            else:
                print("Payload not Detected")
                reed = 0
            reed_average = []
        
        sleep(0.002)  # Short delay for all sensors

        if reed == 0:
            if front_dis >= 19 and right_dis <= 30:
                if right_dis >= 12.5 and right_dis <= 17.5:
                    motor_a('forward', speed)
                    motor_b('forward', speed)
                    print('go straight')
                elif right_dis > 17.5:
                    motor_a('forward', 35)
                    motor_b('forward', 38)
                    print('drift right')
                else:
                    motor_a('forward', 38)
                    motor_b('forward', 35)
                    print('drift left')

            elif front_dis < 20 and right_dis <= 30:
                motor_b()
                motor_a()
                print('stop')
                sleep(2)
                turn_left()
                front_dis = 50
                right_dis = 5

            elif right_dis > 20:
                stop()
                print('stop')
                sleep(2)
                if i == 0:
                    go_straight_2()
                    print('go')
                    stop()
                    sleep(1)
                    
                turn_right()
                stop()
                sleep(1)
                go_straight()
                print('go')
                stop()
                right_dis = 15
                front_dis = 50
                i+= 1

            else:
                motor_a()
                motor_b()
                print('Error')
                return

        else:
            return
        

def pickup():
    # servo with reed pull back
    servo_reed.move(0)
    print('move reed out of the way')
    sleep(1)
    # drive backward for 1 second
    motor_a('backward', speed)
    motor_b('backward', speed)
    print('move backward')
    sleep(1)

    # lower arm by servo pushing up
    servo_payload.move(90)
    servo_step.move(0)
    print('push the arm down')
    sleep(1)

    # drive til limit switch is hit
    but = []
    while True:
        but.append(button.value())
        if len(but) == 5:
            if sum(but) == 5:
                print("Payload on")
                motor_a()
                motor_b()
                print('stop')
                break
                
            else:
                print('Payload not on')
                motor_a('forward', 30)
                motor_b('forward', 30)
                print('go forward')
            but = []
        sleep(.001)

    # stepper motor rotate back and pickup
    servo_payload.move(0)
    print('move servo for payload out the way')
    sleep(1)
    servo_step(18)
    print('pickup the pay load')
    sleep(1)
    go_straight1()
    sleep(1)
    stop()
    return

def go_to_drop():
    but = []
    average_front = []
    average_right = []
    average_left = []
    ir_sensor = []
    reed_average = []
    front_dis = 50
    right_dis = 15
    i = 0
    reed = 0 
    ir = 0

    while True:
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

        # Front Sensor
        try:
            distance = sensor.distance_cm()
            print('Distance:', distance, 'cm')
            if distance > 0 :
                average_front.append(distance)
        
            if len(average_front) == 10:
                front_dis = sum(average_front) / 10
                print(front_dis, "average front")
                average_front = []

        except OSError as ex:
            print('ERROR getting distance:', ex)
            break

        # Right Sensor
        try:
            distance_r = sensor_r.distance_cm()
            print('Distance Right:', distance_r, 'cm')
            average_right.append(distance_r)

            if len(average_right) == 10:
                right_dis = sum(average_right) / 10
                print(right_dis, "average right")
                average_right = []

        except OSError as ex:
            print('ERROR getting distance:', ex)
            break

        # Left Sensor
        '''
        try:
            distance_l = sensor_l.distance_cm()
            print('Distance Left:', distance_l, 'cm')
            sleep(0.01) # sensor doesn't work well without delay
            average_left.append(distance_l)

            if len(average_left) == 5:
                left_dis = sum(average_left) / 5
                print(left_dis, "average left")
                average_left = []
        '''

        # Photodiode
        ir_sensor.append(ir.read_u16())
        if len(ir_sensor) == 5:
            if sum(ir_sensor) > 40000:
                print("Dropoff Detected")
                ir = 1
            else:
                print("Dropoff not detected")
                ir = 0

            ir_sensor = []

        reed_average.append(reed_switch.value())

        if len(reed_average) == 5:
            if sum(reed_average) == 5:
                reed = 1
                print("Payload detected")

            else:
                print("Payload not Detected")
                reed = 0
            reed_average = []
        
        sleep(0.002)  # Short delay for all sensors

        if ir == 0:
            if front_dis >= 19 and right_dis <= 30:
                if right_dis >= 12 and right_dis <= 18:
                    motor_a('forward', speed)
                    motor_b('forward', speed)
                    print('go straight')
                elif right_dis > 17.5:
                    motor_a('forward', 35)
                    motor_b('forward', 38)
                    print('drift right')
                else:
                    motor_a('forward', 38)
                    motor_b('forward', 35)
                    print('drift left')

            elif front_dis < 20 and right_dis <= 30:
                motor_b()
                motor_a()
                print('stop')
                sleep(2)
                turn_left()
                front_dis = 50
                right_dis = 5

            elif right_dis > 20:
                stop()
                print('stop')
                sleep(2)
                if i == 0:
                    go_straight_2()
                    print('go')
                    stop()
                    sleep(1)
                    
                turn_right()
                stop()
                sleep(1)
                go_straight()
                print('go')
                stop()
                right_dis = 15
                front_dis = 50
                i+= 1

            else:
                motor_a()
                motor_b()
                print('Error')
                return

        else:
            stop()
            return

def drop():
    servo_step(0)
    servo_payload(90)
    sleep(1)
    motor_a('backward', speed)
    motor_b('backward', speed)
    sleep(2)

# Main Code
# Find the wall behind us and turn onto the wall for wall-following
sleep(5)
# Main Code
# Find the wall behind us and turn onto the wall for wall-following
sleep(5)
motor_b('forward', speed)
print('face the wall')
sleep(1.52)
motor_b()
sleep(1)
print('stop')

front_dis = 50
while True:
    # Front Sensor
    try:
        distance = sensor.distance_cm()
        print('Distance:', distance, 'cm')
        sleep(0.005) # sensor doesn't work well without delay
        average_front.append(distance)
    
        if len(average_front) == 10:
            front_dis = sum(average_front) / 10
            print(front_dis, "average front")
            average_front = []

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break
    
    if front_dis >= 26:
        motor_a('forward', 50)
        motor_b('forward', 50)
        print('get to wall')
        
    else: 
        motor_a()
        motor_b()
        sleep(2)
        print('at wall')
        break

turn_left()
sleep(2)

# Main Code P.2
while True:
    go_to_payload()
    pickup()
    go_to_drop()
    drop()
    break