# Setting up...

## Service User

Create a service user 'tipi' with the following commands:

```
sudo useradd --create-home --system --user-group tipi
sudo adduser tipi gpio
sudo adduser tipi input
sudo adduser tipi i2c
```

## File paths

The services are expected to run as user 'tipi' and
for consistency, files are expected to be deployed
under /home/tipi ( the tipi user's home directory )

* /home/tipi/services - link or copy of tipi/dsr/python folder
* /home/tipi/tipi_disk - root of tipi filesystem for the TI-99/4A

## Install services

Setup the python prerequisites:
```
cd /home/tipi/services
./setup.sh
```

```
cd /home/tipi
git clone https://github.com/endlos99/xdt99.git
```

There are a number of systemd services that provide the function
of TIPI. Follow these commands to install:

```
cd /home/tipi/services/systemd
sudo cp *.service /lib/systemd/service/
sudo systemctl enable tipiboot.service
sudo systemctl start tipiboot.service
sudo systemctl enable tipiwatchdog.service
sudo systemctl start tipiwatchdog.service
sudo systemctl enable tipi.service
sudo systemctl start tipi.service
sudo systemctl enable tipioled.service
sudo systemctl start tipioled.service
sudo systemctl enable tipisuper.service
sudo systemctl start tipisuper.service
sudo systemctl enable tipiweb.service
sudo systemctl start tipiweb.service
```

These services will auto restart when the Raspberry PI is booted.

The tipiboot.service runs once, as root, to setup some filesystem permissions.
The other services run as user 'tipi'


