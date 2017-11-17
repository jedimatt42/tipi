# Setting up...

## Replace log and tmp folders with tmpfs to prolong SD card life

Add the following to /etc/fstab:

```
tmpfs    /tmp    tmpfs    defaults,noatime,nosuid,size=100m    0 0
tmpfs    /var/tmp    tmpfs    defaults,noatime,nosuid,size=30m    0 0
tmpfs    /var/log    tmpfs    defaults,noatime,nosuid,mode=0755,size=100m    0 0
```

Cleanup files under those subdirectories, and mount the tmpfs filesystems.

```
sudo rm -r /tmp/*
sudo rm -r /var/tmp/*
sudo rm -r /var/log/*
sudo mount /tmp
sudo mount /var/tmp
sudo mount /var/log
```

## Create the tipi service user

Login to the Raspberry PI as user 'pi'. 
Create a service user 'tipi' with the following commands:

```
sudo useradd --create-home --system --user-group tipi
sudo adduser tipi gpio
sudo adduser tipi input
sudo adduser tipi i2c
sudo passwd tipi
```

## Install prerequisites

```
sudo apt-get install python-dev
sudo apt-get install python-virtualenv
sudo apt-get install python-imaging
sudo apt-get install libcurl4-openssl-dev
sudo apt-get install libssl-dev
sudo apt-get install libjpeg-dev
```

## Install services

Setup the services, by becoming the 'tipi' user, cloning the git repository 
within the 'tipi' user home directory, and running the setup.sh script.

Become the tipi user

```
sudo su tipi
```

While executing the following, when prompted for a 'sudo' password, it 
is for the 'tipi' user.

```
cd /home/tipi
git clone https://github.com/jedimatt42/tipi.git tipi
cd /home/tipi/tipi
./setup.sh
```

## Other items to setup

* change the password for user pi
* install samba share for /home/tipi/tipi_disk


