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
motor_a_in1 = Pin(6, Pin.OUT)
motor_a_in2 = Pin(9, Pin.OUT)
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

sleep(10)

lim = 0
magnet = 0
# Example
# turn to start the sequence
motor_a('forward', 50)
print('move')
sleep(1.4)
motor_a()
print("stop")
sleep(2)

front_dis = 100
right_dis = 5
left_dis = 4
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
    
    if front_dis > 6:
        motor_a('forward', 50)
        motor_b('forward', 50)
        print('go to wall')

    else:
        motor_a()
        motor_b()
        sleep(2)
        print('at wall')
        break

# turn to start the sequence
motor_a('forward', 50)
sleep(.7)
motor_a()
print('turn left')

while True:
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
        print('Distance_right:', distance_r, 'cm')
        sleep(0.1) # sensor doesn't work well without delay
        average_right.append(distance_r)

        if len(average_right) == 5:
            right_dis = sum(average_right) / 5
            print(right_dis, "average right")
            average_right = []

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break

    #Left Sensor
    try:
        distance_l = sensor_l.distance_cm()
        print('Distance_left:', distance_l, 'cm')
        sleep(0.1) # sensor doesn't work well without delay
        average_left.append(distance_l)

        if len(average_left) == 5:
            left_dis = sum(average_left) / 5
            print(left_dis, "average left")
            average_left = []

    except OSError as ex:
        print('ERROR getting distance:', ex)
        break
    
    if lim == 0 and magnet == 0:
        if front_dis > 10:
            """if right_dis > 5:
                motor_a('forward', 55)
                motor_b('forward', 45)
            elif right_dis < 5:
                motor_a('forward', 45)
                motor_b('forward', 55)
                """
            
            motor_a('forward', 50)
            motor_b('forward', 50)
            print('forward')
            
        elif right_dis > 15:
            motor_a('forward', 50)
            sleep(.5)
            motor_a()
            sleep(.5)
            print("turn right")
            
        elif left_dis > 5 and front_dis < 10:
            motor_a()
            motor_b()
            sleep(.5)
            motor_b('forward', 50)
            sleep(.5)
            motor_b()
            print('turn left')
                
      

