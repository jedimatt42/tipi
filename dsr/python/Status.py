import netifaces


class Status(object):

    def __init__(self):
        self.__records = []
        for name in netifaces.interfaces():
            if not name.startswith("lo"):
                iface = netifaces.ifaddresses(name)
                self.__records.append("interface: {}".format(name))
                if netifaces.AF_LINK in iface:
                    self.__records.append(
                        "mac-address: {}".format(iface[netifaces.AF_LINK][0]['addr']))
                if netifaces.AF_INET in iface:
                    self.__records.append("ip: {}".format(
                        iface[netifaces.AF_INET][0]['addr']))

    def record(self, idx):
        return self.__records[idx]

    def len(self):
        return len(self.__records)
