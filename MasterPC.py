# get Data stream from GamaSpace Swing
# gaet data stream from Main galerry swing
# if both data are equal then do something


"""  Use this mode if you have a main program loop that needs to run without being blocked by the server. 
The below example runs init_main() once, which creates the serve endpoint and adds it to the asyncio event loop. 
The transport object is returned, which is required later to clean up the endpoint and release the socket. 
Afterwards we start the main loop with await loop(). The example loop runs 10 times and sleeps for a second on every iteration. 
During the sleep the program execution is handed back to the event loop which gives the serve endpoint a chance to handle incoming OSC messages. 
Your loop needs to at least do an await asyncio.sleep(0) every iteration, otherwise your main loop will never release program control back to the event loop.
"""

from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client
import asyncio

GamaSpace_Rotation = 0
MainGalleryRotation = 0


def GamaSpace_handler(address, *args):
    global GamaSpace_Rotation
    GamaSpace_Rotation = round(args[0],2)

def MainGallery_handler(address, *args):
    global MainGalleryRotation
    MainGalleryRotation = round(args[0],2)


dispatcher = Dispatcher()
dispatcher.map("/GamaSpaceRot", GamaSpace_handler)
dispatcher.map("/MainGalleryRot", MainGallery_handler)

ip = "192.168.0.186"
port = 3000


GammaSpace_SSU = udp_client.SimpleUDPClient("192.168.0.228", 4005)
#MainGallery_SSU = udp_client.SimpleUDPClient("192.168.0.2280", 6005)

# main Function of the loop
# here constantly check if both values are equal
async def loop():
    """ Compare the Numbers coming from Raspberry pi"""
    while 1:
        
        print("GamaSpaceRotation: ", GamaSpace_Rotation)
        print("MainGalleryRotation: ", MainGalleryRotation)
        
        if GamaSpace_Rotation == MainGalleryRotation :
            print("were facing the same way")
            GammaSpace_SSU.send_message("/inSync", 1)
            #send a response to both SSU
            
        await asyncio.sleep(0.01)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())




"""
map Amplitude to Z_Acc or Y_ACC and X_ACC
based on the displacment the sound will go up

"""