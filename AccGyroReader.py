import smbus
import time
import math
import RPi.GPIO as gpio
 
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
Device_Address = 0x68   # device address
 
AxCal=0
AyCal=0
AzCal=0
GxCal=0
GyCal=0
GzCal=0


z_rotation = 0
time_interval = 0.1
Note_Step = 2.85



#MPU Functions
def InitMPU():
    bus.write_byte_data(Device_Address, DIV, 7)
    bus.write_byte_data(Device_Address, PWR_M, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_EN, 1)
    time.sleep(1)
 
def readMPU(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
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

# Main
while 1:

  GyroData = gyro()
  
  x_Gyro = round(GyroData[0],2)
  y_Gyro = round(GyroData[1],2)
  z_Gyro = round(GyroData[2],2)  

  time.sleep(time_interval)
  z_rotation += z_Gyro * time_interval
  #print(z_rotation)

  if z_rotation >= 0 and z_rotation <= Note_Step:
      print("Play Note C ")
      print("Z_ang = " + str(z_rotation))
  elif z_rotation > Note_Step and (z_rotation <= Note_Step * 2):
      print("Play Note D ")
      print("Z_ang = " + str(z_rotation))
  elif z_rotation > Note_Step * 2 and (z_rotation <= Note_Step * 3):
      print("Play Note E ")
      print("Z_ang = " + str(z_rotation))
  elif z_rotation > Note_Step * 3 and (z_rotation <= Note_Step * 4):
      print("Play Note F")
      print("Z_ang = " + str(z_rotation))
  elif z_rotation > Note_Step * 4 and (z_rotation <= Note_Step * 5):
      print("Play Note G")
      print("Z_ang = " + str(z_rotation))
  elif z_rotation > Note_Step * 5 and (z_rotation <= Note_Step * 6):
      print("play Note A")
      print("Z_ang = " + str(z_rotation))
  elif z_rotation > Note_Step * 6 and (z_rotation <= Note_Step * 7): 
      print("play Note B")
      print("Z_ang = " + str(z_rotation))   












