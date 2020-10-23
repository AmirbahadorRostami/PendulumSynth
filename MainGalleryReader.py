import smbus
import time
import math
import RPi.GPIO as gpio
import numpy as np
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio

Device_Adress = 0x68   # device address

AxCal=0
AyCal=0
AzCal=0
GxCal=0
GyCal=0
GzCal=0


x_Movment = 0
y_Movment = 0
time_interval = 0.01

Note_Step_1 = 0.0333
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

trigTresh = 0.03

GammaSpcaeCurrentNote = 0

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


GamaSpcae_IP = "192.168.0.209"
GamaSpace_Port = 3000

MainGallery_IP = "192.168.0.201"
MainGallery_Port = 4000

#MPU Functions
def InitMPU():
    bus.write_byte_data(Device_Adress, DIV, 7)
    bus.write_byte_data(Device_Adress, PWR_M, 1)
    bus.write_byte_data(Device_Adress, CONFIG, 0)
    bus.write_byte_data(Device_Adress, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Adress, INT_EN, 1)
    time.sleep(1)
 
def readMPU(addr):
    high = bus.read_byte_data(Device_Adress, addr)
    low = bus.read_byte_data(Device_Adress, addr+1)
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
    
    result = [Ax,Ay,Az]
    return result

    time.sleep(time_interval)
 
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

      result = [Gx,Gy,Gz]
      return result
      
      time.sleep(time_interval)

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

def rolling_mean(arr, val , n = 5):
    arr.append(val)
    if len(arr) > n:
        arr = arr[1:]
    return arr,np.mean(np.array(arr))

def InComingNote_handler(address, *args):
    global GammaSpcaeCurrentNote
    GammaSpcaeCurrentNote = args[0]



InitMPU()
calibrate()

SuperCollider = udp_client.SimpleUDPClient("127.0.0.1" ,5005)
GammaSpaceSSU = udp_client.SimpleUDPClient(GamaSpcae_IP, GamaSpace_Port)

dispatcher = Dispatcher()
dispatcher.map("/GamaSpaceCurrentNote", InComingNote_handler)



time.sleep(1)

async def loop():
    #print("im starting from here")


    X_ACC_Buff = []
    Y_ACC_Buff = []
    Z_ACC_Buff = []
    z_rotation = 0

    # Main
    while 1:

        GyroData = gyro()
        AccData = accel()
        
        x_Gyro = round(GyroData[0],2)
        y_Gyro = round(GyroData[1],2)
        z_Gyro = round(GyroData[2],2)  

        x_Acc = AccData[0]
        y_Acc = AccData[1]
        z_Acc = AccData[2]
        
        #print("Z_ACC ", z_Acc)
        #print("Y_ACC ", y_Acc)
        #print("X_ACC ", x_Acc)

        X_ACC_Buff , X_Acc_smooth = rolling_mean(X_ACC_Buff , x_Acc,3)
        #Y_ACC_Buff , Y_Acc_smooth = rolling_mean(Y_ACC_Buff , y_Acc,7)
        #Z_ACC_Buff , Z_Acc_smooth = rolling_mean(Z_ACC_Buff , z_Acc,7)
        #print("X_ACC_Buff: ", X_ACC_Buff)
        #print("X_ACC_Smooth: " , round(X_Acc_smooth,2))
        #print("Y_ACC_Smooth: " , round(Y_Acc_smooth,2))
        #print("Z_ACC_Smooth: ", abs(round(Z_Acc_smooth,2)))


        #time.sleep(time_interval)

        Y_ACC = abs(round(X_Acc_smooth,2)) #change the varible name to X_ACC
        z_rotation += z_Gyro * time_interval

        #print("YACC: ", Y_ACC)
        #print("My rotation ", z_rotation)
        #print("this my partners note " ,GammaSpcaeCurrentNote)
        #GammaSpaceSSU.send_message("/MainGalleryCurrentNote", z_rotation)
        
        if ((z_rotation >= 0) and (z_rotation <= Note_Step_1)) or ((z_rotation <= 0) and (z_rotation >= -Note_Step_1)):
            
            
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 1
            #print("scale Degree ", myCurrentNote)
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else: 
                SuperCollider.send_message("/SC_Control", SC_Control)

        elif ((z_rotation > Note_Step_1) and (z_rotation <= Note_Step_2)) or ((z_rotation < -Note_Step_1) and (z_rotation >= -Note_Step_2)):
            
            #print("Play Note D ")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 2
            #print("scale Degree ", myCurrentNote)
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote, Y_ACC, GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else: 
                SuperCollider.send_message("/SC_Control", SC_Control)

        elif ((z_rotation > Note_Step_2) and (z_rotation <= Note_Step_3)) or ((z_rotation < -Note_Step_2) and (z_rotation >= -Note_Step_3)):

            #print("Play Note E ")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 3
            #print("scale Degree ", myCurrentNote)
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC ,GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else : 
                SuperCollider.send_message("/SC_Control", SC_Control) 

        elif ((z_rotation > Note_Step_3) and (z_rotation <= Note_Step_4)) or ((z_rotation < -Note_Step_3) and (z_rotation >= -Note_Step_4)):

            #print("Play Note F")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 4
            #print("scale Degree ", myCurrentNote)
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]

            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else: 
                SuperCollider.send_message("/SC_Control", SC_Control)
            
        elif ((z_rotation > Note_Step_4) and (z_rotation <= Note_Step_5)) or ((z_rotation < -Note_Step_4) and (z_rotation >= -Note_Step_5)):

            #print("Play Note G")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 5
            #print("scale Degree ", myCurrentNote)
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]

            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else: 
                SuperCollider.send_message("/SC_Control", SC_Control)

        elif ((z_rotation > Note_Step_5) and (z_rotation <= Note_Step_6)) or ((z_rotation < -Note_Step_5) and (z_rotation >= -Note_Step_6)):
            
            #print("play Note A")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 6
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC ,GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else:
                SuperCollider.send_message("/SC_Control", SC_Control)

        elif ((z_rotation > Note_Step_6) and (z_rotation <= Note_Step_7))  or ((z_rotation < -Note_Step_6) and (z_rotation >= -Note_Step_7)):

            #print("play Note B")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 7
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else:
                SuperCollider.send_message("/SC_Control", SC_Control)

        elif ((z_rotation > Note_Step_7) and (z_rotation <= Note_Step_8)) or ((z_rotation < -Note_Step_7) and (z_rotation >= -Note_Step_8)):

            #print("play Note C")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 1
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)#'C')
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else:
                SuperCollider.send_message("/SC_Control", SC_Control)  
        
        elif ((z_rotation > Note_Step_8) and (z_rotation <= Note_Step_9))  or ((z_rotation < -Note_Step_8) and (z_rotation >= -Note_Step_9)):

            #print("play Note D")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 2
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]

            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else:
                SuperCollider.send_message("/SC_Control", SC_Control)
        
        elif ((z_rotation > Note_Step_9) and (z_rotation <= Note_Step_10)) or ((z_rotation < -Note_Step_9) and (z_rotation >= -Note_Step_10)):

            #print("play Note E")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 3
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)#'E')
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else : 
                SuperCollider.send_message("/SC_Control", SC_Control) 
        
        elif ((z_rotation > Note_Step_10) and (z_rotation <= Note_Step_11)) or ((z_rotation < -Note_Step_10) and (z_rotation >= -Note_Step_11)):

            #print("play Note F")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 4
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else : 
                SuperCollider.send_message("/SC_Control", SC_Control) 

        elif ((z_rotation > Note_Step_11) and (z_rotation <= Note_Step_12)) or ((z_rotation < -Note_Step_11) and (z_rotation >= -Note_Step_12)):

            #print("play Note G")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 5
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC , GammaSpcaeCurrentNote]
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else : 
                SuperCollider.send_message("/SC_Control", SC_Control) 

        elif ((z_rotation > Note_Step_12) and (z_rotation <= Note_Step_13)) or ((z_rotation < -Note_Step_12) and (z_rotation >= -Note_Step_13)):

            #print("play Note A")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 6
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            SC_Control = [myCurrentNote , Y_ACC ,GammaSpcaeCurrentNote]
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else : 
                SuperCollider.send_message("/SC_Control", SC_Control)

        elif ((z_rotation > Note_Step_13) and (z_rotation <= Note_Step_14)) or ((z_rotation < -Note_Step_13) and (z_rotation >= -Note_Step_14)):

            #print("play Note B")
            #print("Z_ang = " + str(z_rotation))
            myCurrentNote = 7
            SC_Control = [myCurrentNote , Y_ACC ,GammaSpcaeCurrentNote]
            GammaSpaceSSU.send_message("/MainGalleryCurrentNote", myCurrentNote)
            
            if GammaSpcaeCurrentNote == myCurrentNote : 
                print("we are alligned")
            else: 
                SuperCollider.send_message("/SC_Control", SC_Control)  
        
        await asyncio.sleep(time_interval)  



async def init_main():
    server = AsyncIOOSCUDPServer((MainGallery_IP, MainGallery_Port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())







