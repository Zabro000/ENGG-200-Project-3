from machine import Pin, PWM
from time import sleep

# === L298N Motor Driver ===
# Motor A
motor_a_in1 = Pin(6, Pin.OUT)
motor_a_in2 = Pin(9, Pin.OUT)
motor_a_en = PWM(Pin(8))
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

from machine import Pin
from time import sleep
from servo import Servo # Save this file on pico

sg90 = Servo(Pin(1))


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

from machine import Pin
from time import sleep

# Initialize input with internal pull down resistor on pin 10
# When using internal pull down resistor on Pico, pin will have logic level 1 (3.3 V) when button pushed and 0 when released
# FOr internal pull up resistor, pin will have logic level 0 when button pushed and 1 (3.3 V) when released
button = Pin(10, Pin.IN, Pin.PULL_DOWN)

# Initialize on board LED
led = Pin('LED', Pin.OUT)
but = []
payload = 0

while True:
    if button.value() == 1:
        print("Button Pressed!")
        led.on()
        limit = 1
    else:
        print("Not Pressed")
        limit = 0
        led.off()
        
        
    but.append(limit)
    
    if len(but) == 5:
        if sum(but) == 5:
            print("Payload on")
            payload = 1
            
        but = []
        

    if payload == 1:
        motor_a()
        motor_b()
        print('stop')
        sg90.move(0) # move to 0 degree postion
        sleep(.1)
        print('pickup')
        break
    else:
        motor_a('forward', 50)
        motor_b('forward', 50)
        print('find payload')
    
i = 0
        
while True:       
    if i < 1:
        motor_a("forward", 50)
        motor_b("forward", 50)
        print('move forward')
        sleep(4)
        i += 1
    else:
        motor_a()
        motor_b()
        print('stop')
        sg90.move(90) # move to 0 degree postion
        sleep(.1)
        print('drop')
        break

while True:
    motor_a("backward", 45)
    motor_b("backward", 45)
    print('move backward')
    sleep(2)
    j += 1
    break
        
motor_a()
motor_b()
print('stop')
sleep(1) # delete
