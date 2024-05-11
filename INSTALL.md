# Setting up...

## If using the SD-Card image the steps in this document have already been performed.

SD Card image is available for download: 

[www.jedimatt42.com](https://www.jedimatt42.com/downloads.html)

Go to the [Wiki](https://github.com/jedimatt42/tipi/wiki) for end user installation.

# Only follow these instructions if you are setting up an SD Card from scratch.

Assumes base image is Raspbian Lite (bookworm)

## Pre-boot setup

Before booting the Raspbian SD image, create a createuser.txt, enable ssh, enable wifi by
following the instructions from [raspberrypi.com](https://raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi)
The user you create should be named: tipi
The tipi user password should be: tipi

Use raspi-config to install locales and set default, en_US_utf8.
Note: installing all locales takes forever, and slows future updates.
install en-US-UTF8, en-GB-UTF8, de-DE-UTF8, and en-CA-UTF8

Use raspi-config to disable i2c so that gpio-shutdown can be enabled.

Use raspi-config to enable ssh, and grow the root filesystem.
reboot.

## Replace log and tmp folders with tmpfs to prolong SD card life

Add the following to /etc/fstab:

```
tmpfs    /tmp    tmpfs    defaults,noatime,nosuid,size=100m    0 0
tmpfs    /var/log    tmpfs    defaults,noatime,nosuid,mode=0755,size=100m    0 0
```

Cleanup files under those subdirectories, and mount the tmpfs filesystems.

```
sudo rm -r /tmp/*
sudo rm -r /var/log/*
```

Reboot

```
sudo reboot now
```


## Install Software

Make sure git is installed (after setting up tmpfs folders, update will be required)

```
sudo apt update
sudo apt upgrade
sudo apt install git
```

## Install services

Setup the services, by becoming the 'tipi' user, cloning the git repository 
within the 'tipi' user home directory, and running the setup.sh script.

While executing the following, when prompted for a 'sudo' password, it 
is for the 'tipi' user.

Install the tipi kernel module

```
cd /home/tipi
git clone https://github.com/jedimatt42/tipi_kernel_module.git
cd tipi_kernel_module
sudo apt install raspberrypi-kernel-headers
./build.sh
sudo ./install.sh
sudo reboot now
```

NOTE: The ./install.sh step will fail to copy the overlay on a Le Potato
      Check the Le Potato section of the tipi_kernel_module/README.md 

Install the tipi services

```
cd /home/tipi
git clone https://github.com/jedimatt42/tipi.git tipi
cd /home/tipi/tipi
git checkout bookworm_release
git submodule update --init
./setup.sh
```

And run the post-upgrade to finish all the incremental configuration

```
cd setup
sudo ./post-upgrade.sh
```

NOTE: On Le Potato some parts of post-upgrade do not work. Completely...

## Other items to setup

* (for distributing an image, I don't do this) change the password for user pi
* change the hostname (raspi-config)
* install samba share for /home/tipi/tipi_disk
* add telnetd for localhost access

   edit /etc/hosts.allow: 

```
in.telnetd: localhost
```

   edit /etc/hosts.deny: 

```
in.telnetd: ALL
```


Use raspi-config to set hostname to: `tipi`

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
create mask=0644
directory mask=0755
force user=tipi
```

## Test WIFI Connectivity

Make sure wifi was working before archiving the image. 

## Disable apache2.service

I don't know why this keeps coming back... but disable it as it fails to start and is 
not used.

```
sudo systemctl disable apache2.service
```

### Set the system to grow on boot

-- To be nice, set the image to resize on next boot 
```
sudo raspi-config nonint do_expand_rootfs
```

or edit the init in boot
```
init=/usr/lib/raspi-config/init_resize.sh
```

Don't reboot, just shutdown.

### Capture SD Card Image

On a linux system dump the sdcard to an image. Then mount the image and clear unused blocks before zipping.

run dmesg to see what device sd card mounted as... presuming it was /dev/sdb:

```
sudo dd status=progress if=/dev/sdb of=sdimage.img bs=4M
sudo kpartx -a sdimage.img
```

You should be able to now mount the rootfs, or /dev/mapper/loop??p2.  On ubuntu like desktops the volume names will show up in the UI for removable media... 

Edit and Remove personal settings found in
- /home/tipi/tipi.config
- /etc/wpa_supplicant/wpa_supplicant.conf
- /home/tipi/.ssh/*

Then clear the space:

```
cd /media/`whoami`/rootfs
sudo dd status=progress if=/dev/zero of=zeroes bs=4M
sudo sync
sudo rm zeroes
cd
umount /media/`whoami`/rootfs
```

Now zip it up!
