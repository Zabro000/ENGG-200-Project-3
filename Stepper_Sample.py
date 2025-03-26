import stepper # must have this file saved on Pico
from time import sleep

# Define the stepper motor pins
IN1 = 2
IN2 = 3
IN3 = 4
IN4 = 5

# Initialize the stepper motor
stepper_motor = stepper.HalfStepMotor.frompins(IN1, IN2, IN3, IN4)

# Set the current position as position 0
stepper_motor.reset()

while True:
    #Move 500 steps in clockwise direction
    stepper_motor.step(-300)
    sleep(5) # stop for a while
    stepper_motor.step(300)
    sleep(5)
    