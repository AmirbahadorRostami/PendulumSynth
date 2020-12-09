from pythonosc import dispatcher
from pythonosc import osc_server
import csv
import time as Time



def InComingRow(*args):

    Time.sleep(1.0)
    t = Time.time()
    with open('test.csv', 'a', newline='') as csvfile:
        writer_ = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_.writerow( [t , args[1] , args[2] , args[3]] )
    print(args)

MainPC_IP = "192.168.0.10"
MainPC_Port = 6000

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/Data", InComingRow)

with open('test.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Time']+['CurrentNote(GammaSpace)']+['isMathced']+['CurrentNote(MainGallery)'])


server = osc_server.ThreadingOSCUDPServer((MainPC_IP, MainPC_Port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()