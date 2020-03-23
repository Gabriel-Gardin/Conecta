import paho.mqtt.subscribe as subscribe
import json, threading, time, weakref
from rastreador_mac import Rastreador
import matplotlib.pyplot as plt
import multiprocessing as mp


rastreadores = weakref.WeakValueDictionary() #Keep track dos rastreadores.
queue1 = mp.Queue()
queue2 = mp.Queue()

def data_receiver(client, userdata, message):
    received_data = json.loads(message.payload)
    mac_addr = received_data["mac"]
    #print("Total de rastreadores = ", len(rastreadores))

    if(mac_addr not in rastreadores):
        mac_tracking_class = Rastreador(mac_addr)
        rastreadores[mac_tracking_class.__str__()] = mac_tracking_class

    elif(mac_addr in rastreadores):
        #make_graph()
        instance = rastreadores.get(mac_addr)
        instance.new_packet_data(received_data)


def worker(q1, q2):
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    plt.show(block = False)
    fig.canvas.draw()
    while True:
        if(q1.qsize() > 0):
            obj1 = q1.get()
            obj2 = q2.get()
            ax1.clear()
            rects = ax1.bar(obj1, obj2,  align = 'center', color=(0.2, 0.4, 0.6, 0.6))
            for rect, h in zip(rects, obj2):
                rect.set_height(h)
                fig.canvas.draw()
                #plt.pause(0.001)
                fig.canvas.flush_events()
        time.sleep(0.1)


def update_graph():
    mac_address = []
    beacons_count = []
    a = 0
    for item in list(rastreadores):
        if(item not in mac_address):
            mac_address.append(item)
            beacons_count.append(rastreadores[item].get_beacons_count())
        else:
            beacons_count[a] = rastreadores[item].get_beacons_count()
        a = a + 1
    queue1.put(mac_address)
    queue2.put(beacons_count)
    threading.Timer(1, update_graph).start()


if __name__ == "__main__":
    p = mp.Process(target=worker, args=(queue1, queue2))
    p.start()
    update_graph()
    subscribe.callback(data_receiver, "/topic/subdev/#", hostname="192.168.0.223")

    
