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

from machine import Pin
from time import sleep

# Initialize input with internal pull down resistor on pin 10
# When using internal pull down resistor on Pico, pin will have logic level 1 (3.3 V) when button pushed and 0 when released
# FOr internal pull up resistor, pin will have logic level 0 when button pushed and 1 (3.3 V) when released
button = Pin(10, Pin.IN, Pin.PULL_DOWN)

# Initialize on board LED
led = Pin('LED', Pin.OUT)
but = []

while True:
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
            payload = 1
        but = []
        
        sleep(0.1) # Short delay

    if payload == 1:
        stepper_motor.step(260)
        i = 0
        if i < 1:
            motor_a("forward", 50)
            motor_b("forward", 50)
            sleep(1)
            i += 1
        else:
            motor_a()
            motor_b()
            stepper_motor.step(-260)
            j = 0
            if j < 1:
                motor_a("backward", 50)
                motor_b("backward", 50)
                j += 1
            else:
                motor_a()
                motor_b()