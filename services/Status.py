import netifaces


class Status(object):

    def __init__(self):
        self.__records = []
        for name in netifaces.interfaces():
            if not name.startswith("lo"):
                iface = netifaces.ifaddresses(name)
                if netifaces.AF_LINK in iface:
                    self.__records.append(
                        "MAC_{}={}".format(str(name).upper(), iface[netifaces.AF_LINK][0]['addr']))
                if netifaces.AF_INET in iface:
                    self.__records.append("IP_{}={}".format(str(name).upper(), iface[netifaces.AF_INET][0]['addr']))

        with open("/home/tipi/tipi/version.txt", 'r') as fh_in:
            for line in fh_in.readlines():
                parts = line.split('=')
                self.__records.append("{}={}".format( 
                        str(parts[0]).strip().upper(),
                        str(parts[1]).strip()))

    def record(self, idx):
        return self.__records[idx]

    def len(self):
        return len(self.__records)
