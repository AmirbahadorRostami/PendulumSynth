import smbus
import time
import math
import RPi.GPIO as gpio
import argparse
from pythonosc import udp_client

PWR_M   = 0x6B
DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_EN   = 0x38
ACCEL_X = 0x3B
ACCEL_Y = 0x3D
ACCEL_Z = 0x3F
GYRO_X  = 0x43
GYRO_Y  = 0x45
GYRO_Z  = 0x47
TEMP = 0x41
bus = smbus.SMBus(1)
Device_MainGallery = 0x68   # device address
Device_GammaSpace = 0x69   # device address


AxCal=0
AyCal=0
AzCal=0
GxCal=0
GyCal=0
GzCal=0

z_rotation = 0
time_interval = 0.1

Note_Step_1 = 2.85
Note_Step_2 = Note_Step_1 * 2
Note_Step_3 = Note_Step_1 * 3
Note_Step_4 = Note_Step_1 * 4
Note_Step_5 = Note_Step_1 * 5
Note_Step_6 = Note_Step_1 * 6
Note_Step_7 = Note_Step_1 * 7 
Note_Step_8 = Note_Step_1 * 8
Note_Step_9 = Note_Step_1 * 9
Note_Step_10 = Note_Step_1 * 10
Note_Step_11 = Note_Step_1 * 11
Note_Step_12 = Note_Step_1 * 12
Note_Step_13 = Note_Step_1 * 13
Note_Step_14 = Note_Step_1 * 14

C_MajorScale = [36,38,40,41,43,45,47]
trigTresh = 0.1

#MPU Functions
def InitMPU():
    bus.write_byte_data(Device_MainGallery, DIV, 7)
    bus.write_byte_data(Device_MainGallery, PWR_M, 1)
    bus.write_byte_data(Device_MainGallery, CONFIG, 0)
    bus.write_byte_data(Device_MainGallery, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_MainGallery, INT_EN, 1)
    time.sleep(1)
 
def readMPU(addr):
    high = bus.read_byte_data(Device_MainGallery, addr)
    low = bus.read_byte_data(Device_MainGallery, addr+1)
    value = ((high << 8) | low)

    if(value > 32768):
        value = value - 65536
    return value

def accel():
    x = readMPU(ACCEL_X)
    y = readMPU(ACCEL_Y)
    z = readMPU(ACCEL_Z)
    
    Ax = (x/16384.0-AxCal) 
    Ay = (y/16384.0-AyCal) 
    Az = (z/16384.0-AzCal)
    
    #print "AccX="+str(Ax)
    #print "AccY="+str(Ay)
    #print "AccZ="+str(Az)
    
    result = [Ax,Ay,Az]
    return result

    time.sleep(.01)
 
def gyro():
      global GxCal
      global GyCal
      global GzCal
      
      x = readMPU(GYRO_X)
      y = readMPU(GYRO_Y)
      z = readMPU(GYRO_Z)
      
      Gx = x/131.0 - GxCal
      Gy = y/131.0 - GyCal
      Gz = z/131.0 - GzCal

      #print "GyroX="+str(Gx)
      #print "GyroY="+str(Gy)
      #print "GyroZ="+str(Gz)

      result = [Gx,Gy,Gz]
      return result
      
      time.sleep(.01)

def calibrate():

  global AxCal
  global AyCal
  global AzCal
  x=0
  y=0
  z=0
  for i in range(50):
      x = x + readMPU(ACCEL_X)
      y = y + readMPU(ACCEL_Y)
      z = z + readMPU(ACCEL_Z)
  x= x/50
  y= y/50
  z= z/50
  AxCal = x/16384.0
  AyCal = y/16384.0
  AzCal = z/16384.0
  
  print (AxCal)
  print (AyCal)
  print (AzCal)
 
  global GxCal
  global GyCal
  global GzCal
  x=0
  y=0
  z=0
  for i in range(50):
    x = x + readMPU(GYRO_X)
    y = y + readMPU(GYRO_Y)
    z = z + readMPU(GYRO_Z)
  x= x/50
  y= y/50
  z= z/50
  GxCal = x/131.0
  GyCal = y/131.0
  GzCal = z/131.0
  
 
  print (GxCal)
  print (GyCal)
  print (GzCal)

def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


InitMPU()
calibrate()
time.sleep(1)


parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient("127.0.0.1" ,5005)

MasterPC = udp_client.SimpleUDPClient("192.168.0.186", 3000)


# Main
while 1:

  GyroData = gyro()
  AccData = accel()
  
  x_Gyro = round(GyroData[0],2)
  y_Gyro = round(GyroData[1],2)
  z_Gyro = round(GyroData[2],2)  

  x_Acc = round(AccData[0],2)
  y_Acc = round(AccData[1],2)
  z_Acc = round(AccData[2],2)

  #print("X_Acc: " + x_Acc)

  time.sleep(time_interval)
  z_rotation += z_Gyro * time_interval
 
  MasterPC.send_message("/MainGalleryRot",z_rotation)

  if ((z_rotation >= 0) and (z_rotation <= Note_Step_1)) or ((z_rotation <= 0) and (z_rotation >= -Note_Step_1)):
      print("Play Note C ")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[0])
  elif ((z_rotation > Note_Step_1) and (z_rotation <= Note_Step_2)) or ((z_rotation < -Note_Step_1) and (z_rotation >= -Note_Step_2)):
      print("Play Note D ")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh :  client.send_message("/z_Rot", C_MajorScale[1])
  elif ((z_rotation > Note_Step_2) and (z_rotation <= Note_Step_3)) or ((z_rotation < -Note_Step_2) and (z_rotation >= -Note_Step_3)):
      print("Play Note E ")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[2])
  elif ((z_rotation > Note_Step_3) and (z_rotation <= Note_Step_4)) or ((z_rotation < -Note_Step_3) and (z_rotation >= -Note_Step_4)):
      print("Play Note F")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[3])
  elif ((z_rotation > Note_Step_4) and (z_rotation <= Note_Step_5)) or ((z_rotation < -Note_Step_4) and (z_rotation >= -Note_Step_5)):
      print("Play Note G")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[4])
  elif ((z_rotation > Note_Step_5) and (z_rotation <= Note_Step_6)) or ((z_rotation < -Note_Step_5) and (z_rotation >= -Note_Step_6)):
      print("play Note A")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[5])
  elif ((z_rotation > Note_Step_6) and (z_rotation <= Note_Step_7)) or ((z_rotation < -Note_Step_6) and (z_rotation >= -Note_Step_7)): 
      print("play Note B")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[6])
  elif ((z_rotation > Note_Step_7) and (z_rotation <= Note_Step_8)) or ((z_rotation < -Note_Step_7) and (z_rotation >= -Note_Step_8)): 
      print("play Note C")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[0]) 
  elif ((z_rotation > Note_Step_8) and (z_rotation <= Note_Step_9)) or ((z_rotation < -Note_Step_8) and (z_rotation >= -Note_Step_9)): 
      print("play Note D")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[1])
  elif ((z_rotation > Note_Step_9) and (z_rotation <= Note_Step_10)) or ((z_rotation < -Note_Step_9) and (z_rotation >= -Note_Step_10)): 
      print("play Note E")
      print("Z_ang = " + str(z_rotation))
      client.send_message("/z_Rot", C_MajorScale[2])
  elif ((z_rotation > Note_Step_10) and (z_rotation <= Note_Step_11)) or ((z_rotation < -Note_Step_10) and (z_rotation >= -Note_Step_11)): 
      print("play Note F")
      print("Z_ang = " + str(z_rotation)) 
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[3])  
  elif ((z_rotation > Note_Step_11) and (z_rotation <= Note_Step_12)) or ((z_rotation < -Note_Step_11) and (z_rotation >= -Note_Step_12)): 
      print("play Note G")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[4])
  elif ((z_rotation > Note_Step_12) and (z_rotation <= Note_Step_13)) or ((z_rotation < -Note_Step_12) and (z_rotation >= -Note_Step_13)): 
      print("play Note A")
      print("Z_ang = " + str(z_rotation))  
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[5])  
  elif ((z_rotation > Note_Step_13) and (z_rotation <= Note_Step_14)) or ((z_rotation < -Note_Step_13) and (z_rotation >= -Note_Step_14)): 
      print("play Note B")
      print("Z_ang = " + str(z_rotation))
      if z_Acc > trigTresh : client.send_message("/z_Rot", C_MajorScale[6])













