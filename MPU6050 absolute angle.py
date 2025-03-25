from machine import I2C, Pin 
from imu import MPU6050 # Save this library on Pico
import time

# Pins according the schematic https://heltec.org/project/wifi-kit-32/
# Replace with proper scl and sda pins
i2c = I2C(1, scl=Pin(3), sda=Pin(2))

# Accelerometer / Gyroscope
imu = MPU6050(i2c)

while True:
    
    # print all values
    print('Accelerometer',(imu.accel.xyz))
    print('Gyroscope',(imu.gyro.xyz))
    print('Temperature',(imu.temperature))

    #print a single value, e.g. x value of acceleration and z gyro
    print(imu.accel.x)
    print(imu.gyro.z)
    time.sleep(1)
    