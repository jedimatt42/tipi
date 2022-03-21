# TIPI support of popular emulators

TIPI is not an emulation of TI-99/4A hardware. It is a unique and independent implementation of storage, network, and other peripherals. Emulation in this context refers to TI-99/4A emulators that support TIPI features.

Classic99 implements some TIPI device and message level protocols directly. It is baked in. 

js99er.net supports connecting to a running set of TIPI services either on a real Raspberry PI or through a QEMU based PI emulation running the real TIPI services.

## Using QEMU

Run the emulation with the latest TIPI hardware sdimage.

1. Enable emulation mode, by running `/home/tipi/emulation/emu-setup.sh` and responding to the prompts

2. Edit the `/etc/fstab` and delete the 3 TMPFS entries. The QEMU configuration does not have enough RAM for so much TMPFS usage.

3. Disable tipiwatchdog.service - it's not needed, and may crash since GPIO isn't actually available: `sudo systemctl disable tipiwatchdog.service`

4. exit the emulation clean: `sudo shutdown now`

### Options in the standard image that might need fixing

raspi-config should be run to change the locale, and 
keyboard defaults for the system

## Using a real PI

You can use a real PI, and the latest SD image. You will have to setup the networking following the Raspberry PI documentation: [headless network setup](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi)

Be sure to touch the `ssh` file in the `boot` partition so sshd is enabled. Then you can get in and use raspi-config to setup locale, hostname, and other items.

Enable emulation mode, by running `/home/tipi/emulation/emu-setup.sh` and responding to the prompts. On a real Raspberry PI, PDF conversion can be enabled, and you probably don't want tipi_disk mounted via NFS.

You should leave the tmpfs and other services as they are for a normal PI setup.

