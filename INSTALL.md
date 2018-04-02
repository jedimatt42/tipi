# Setting up...

## If using the SD-Card image the following has already been performed.

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
sudo adduser tipi sudo
sudo passwd tipi
```

## Install Software

Make sure git is installed (after setting up tmpfs folders, update will be required)

```
sudo apt-get update
sudo apt-get install git
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
* change the hostname
* install samba share for /home/tipi/tipi_disk
* add telnetd for localhost access
   /etc/hosts.allow: in.telnetd: localhost
   /etc/hosts.deny: in.telnetd: ALL



Changing hostname: /etc/hostname & /etc/hosts

Recommended Samba configuration for /etc/samba/smb.conf:

```
[TIPI]
comment=TI-99/4A Files
path=/home/tipi/tipi_disk
public=no
browseable=Yes
writeable=Yes
only guest=no
guest ok=Yes
valid user=tipi
create mask=0644
directory mask=0755
force user=tipi
```

### Capture SD Card Image

run dmesg to see what device sd card mounted as... /dev/sdb?
dd if=/dev/sdb of=sdimage.img bs=4M

