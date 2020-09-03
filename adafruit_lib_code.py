from time import sleep

import board
import busio
import adafruit_mpu6050

import math
import argparse
import random
import time
from pythonosc import udp_client


#init MPU Object
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

z_ang = 0
time_interval = 0.1



parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)




while True:
    # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    rotation = mpu.gyro
    [x_accel, y_accel, z_accel] = mpu.acceleration
    #print(x_accel)
    #print(z_accel)
    #print()
    
    x_rot = round(rotation[0], 2)
    y_rot = round(rotation[1], 2)
    z_rot = round(rotation[2] - 0.6, 2)

    # print('{0: <6}  {1: <6}  {2: <6}'.format(x_rot, y_rot, z_rot))
    sleep(time_interval)

    z_ang += z_rot * time_interval
    print(z_ang)
    client.send_message("/z_Rot", z_ang)


    
