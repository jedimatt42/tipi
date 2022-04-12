import os
import netifaces
import logging

from subprocess import check_output

logger = logging.getLogger(__name__)

tipi_dir = os.getenv("TIPI_DIR")
tipi_conf = os.getenv("TIPI_CONF")

class Status(object):
    def __init__(self):
        self.__records = []
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

        with open(f"{tipi_dir}/version.txt", "r") as fh_in:
            for line in fh_in.readlines():
                parts = line.split("=")
                self.__records.append(
                    "{}={}".format(str(parts[0]).strip().upper(), str(parts[1]).strip())
                )

        if os.path.exists(f"{tipi_conf}/tipi.uuid"):
            with open(f"{tipi_conf}/tipi.uuid", "r") as fh_in:
                self.__records.append("UUID={}".format(fh_in.readline().strip()))

        # This needs to work even if there is no network.. thus a catch all.
        try:
            upgradeCheck = str(check_output([f"{tipi_dir}/setup/upgrade.sh"]), 'ascii')
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
