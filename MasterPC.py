from pythonosc import dispatcher
from pythonosc import osc_server





def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass



MainPC_IP = "192.168.0.10"
MainPC_Port = 6000

GamaSpcae_IP = "192.168.0.37"
GamaSpace_Port = 3000


dispatcher = dispatcher.Dispatcher()
dispatcher.map("/Data", print)
#dispatcher.map("/volume", print_volume_handler, "Volume")
#dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

server = osc_server.ThreadingOSCUDPServer((MainPC_IP, MainPC_Port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()