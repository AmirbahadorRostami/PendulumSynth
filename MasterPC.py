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


def filter_handler(address, *args):
    print(f"{address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/rot", filter_handler)

ip = "192.168.0.186"
port = 3000

# main Function of the loop
# here constantly check if both values are equal
async def loop():
    """ Log the Numbers coming from Raspberry pi"""
    for i in range(10):
        print(f"Loop {i}")
        await asyncio.sleep(1)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())