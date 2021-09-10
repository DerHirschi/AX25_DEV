import time
import os
import pickle
import ax25enc as ax

axip_clientList = 'data/axip_clientList.pkl'
client_db = 'data/clientDB.pkl'


class Client(object):
    def __init__(self, call):
        self.call_str = call
        self.call = ax.get_ssid(call)[0]
        self.ssid = ax.get_ssid(call)[1]
        self.name = ''
        self.qth = ''
        self.loc = ''
        self.axip_addr = ()
        self.last_axip_addr = ()
        self.is_new = True
        self.copy_fm = ''
        self.last_seen = time.time()
        ########
        # self.filter
        # self.mode
        # self.aprs_mode
        # self.language


class ClientDB:
    def __init__(self):
        self.db = {}
        try:
            with open(client_db, 'rb') as inp:
                self.db = pickle.load(inp)
        except FileNotFoundError:
            os.system('touch {}'.format(client_db))
            default_client = Client('ALL')
            default_client.is_new = False
            default_client.name = 'Beacon'
            self.db = {
                'ALL': default_client
            }
        except EOFError:
            pass

    def get_entry(self, call):
        if call not in self.db.keys():
            print('# Client DB: New User added > ' + call)
            self.db[call] = Client(call)
        return self.db[call]

    def save_data(self):
        try:
            with open(axip_clientList, 'wb') as outp:
                pickle.dump(self.db, outp, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError as e:
            print("ERROR SAVE ClientDB: " + str(e))


class AXIPClients(object):
    def __init__(self, port):
        self.port = port
        self.clients = {
            # 'call_str': {
            #       'addr': (),
            #       'lastsee': 0.0,
            # }
        }
        try:
            with open(axip_clientList, 'rb') as inp:
                self.clients = pickle.load(inp)
        except FileNotFoundError:
            os.system('touch {}'.format(axip_clientList))
        except EOFError:
            pass

    def cli_cmd_out(self):
        out = ''
        out += '\r                       < AXIP - Clients >\r\r'
        out += '-Call-----IP:Port---------------Timeout------------------\r'
        for ke in self.clients.keys():
            out += '{:9} {:21} {:8}\r'.format(
                ke,
                self.clients[ke]['addr'][0] + ':' + str(self.clients[ke]['addr'][1]),
                round(time.time() - self.clients[ke]['lastsee'])
            )
        out += '\r'
        return out

    def save_data(self):
        try:
            with open(axip_clientList, 'wb') as outp:
                pickle.dump(self.clients, outp, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError as e:
            print("ERROR SAVE AXIPClients: " + str(e))

