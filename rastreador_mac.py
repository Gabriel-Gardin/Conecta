import time, threading


class Rastreador:
    def __init__(self, mac_addr):
        self.mac = mac_addr
        self.beacons_list = {}
        self.is_beacon_on()
        self.active_beacons_count
        self.max_tracking_time = 15


    def is_beacon_on(self):
        for item in list(self.beacons_list): #Faz uma cópia dos elementos do dicionário para evitar que o mesmo seja alterado pela main thread.
            if(time.time() - (float(self.beacons_list[item])) > self.max_tracking_time): #Se um beacon não da sinal de vida em um certo intervalo de tempo o retira da lista.
                del self.beacons_list[item]
        self.active_beacons_count = len(self.beacons_list)
        threading.Timer(1, self.is_beacon_on).start()


    def new_packet_data(self, data):
       self.bt_adress = data["bt_addr"]
       self.beacons_list[self.bt_adress] = time.time()


    def __str__(self):
        return self.mac

    def get_beacons_count(self):
        return self.active_beacons_count
