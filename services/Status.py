import netifaces
import logging

from subprocess import check_output
import os
from tipi_paths import TIPI_REPO, TIPI_UUID

logger = logging.getLogger(__name__)


class Status(object):
    def __init__(self):
        self.__records = []
        try:
            for name in netifaces.interfaces():
                if not name.startswith("lo"):
                    iface = netifaces.ifaddresses(name)
                    if netifaces.AF_LINK in iface:
                        self.__records.append(
                            "MAC_{}={}".format(
                                str(name).upper(), iface[netifaces.AF_LINK][0]["addr"]
                            )
                        )
                    if netifaces.AF_INET in iface:
                        self.__records.append(
                            "IP_{}={}".format(
                                str(name).upper(), iface[netifaces.AF_INET][0]["addr"]
                            )
                        )
        except:
            self.__records.append("ERROR=netifaces")

        # TIPICFG shows IP_WLAN0 or IP_ETH0, which only Linux names. Elsewhere (the macOS
        # emulation) report where the TIPI is reached: loopback when bound there, else the
        # default route's interface.
        if not any(r.startswith(("IP_WLAN0=", "IP_ETH0=")) for r in self.__records):
            try:
                if os.environ.get("TIPI_BIND_LOCAL"):
                    addr = "127.0.0.1"
                else:
                    iface = netifaces.gateways()["default"][netifaces.AF_INET][1]
                    addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["addr"]
                self.__records.insert(0, f"IP_ETH0={addr}")
            except Exception:
                pass

        with open(os.path.join(TIPI_REPO, "version.txt"), "r") as fh_in:
            for line in fh_in.readlines():
                parts = line.split("=")
                self.__records.append(
                    "{}={}".format(str(parts[0]).strip().upper(), str(parts[1]).strip())
                )

        with open(TIPI_UUID, "r") as fh_in:
            self.__records.append("UUID={}".format(fh_in.readline().strip()))

        # This needs to work even if there is no network.. thus a catch all.
        try:
            upgradeCheck = str(check_output([os.path.join(TIPI_REPO, "setup", "upgrade.sh")]), 'ascii')
            latest = upgradeCheck.split("\n")[1]
            if latest.startswith("Latest Version: "):
                gitver=latest.split(":")[1].strip()
                self.__records.append(f'LATEST={gitver}')
        except Exception as e:
            logger.warn("failed to fetch latest version info")

    def record(self, idx):
        return self.__records[idx]

    def __len__(self):
        return len(self.__records)

if __name__ == "__main__":
    status = Status()
    max = status.__len__()
    idx = 0
    while idx < max:
        print(status.record(idx))
        idx += 1

