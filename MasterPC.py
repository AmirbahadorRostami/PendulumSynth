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
import asyncio

GamaSpace_Rotation = 0
MainGalleryRotation = 0


def GamaSpace_handler(address, *args):
    print(f"{address}: {args}")
    GamaSpace_Rotation = args[0]

def MainGallery_handler(address, *args):
    print(f"{address}: {args}")
    MainGalleryRotation = args[0]


dispatcher = Dispatcher()
dispatcher.map("/GamaSpaceRot", GamaSpace_handler)
dispatcher.map("/MainGalleryRot", GamaSpace_handler)

ip = "192.168.0.186"
port = 3000


GammaSpace_SSU = udp_client.SimpleUDPClient("192.168.0.228", 4005)
MainGallery_SSU = udp_client.SimpleUDPClient("192.168.0.2280", 6005)

# main Function of the loop
# here constantly check if both values are equal
async def loop():
    """ Compare the Numbers coming from Raspberry pi"""
    while 1:
        
        print("GamaSpaceRotation: ", GamaSpace_Rotation)
        print("MainGalleryRotation: ", MainGalleryRotation)
        
        if GamaSpace_Rotation == MainGalleryRotation :
            print("were facing the same way")
            #send a response to both SSU

        await asyncio.sleep(1)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())