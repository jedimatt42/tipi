# Preparing Emulation bundle

Include the files in this directory in a zip with a modified sd card.

## To modify the sd image

Run the emulation with the standard TIPI hardware sdimage

1. Enable emulation mode:

```
touch /home/tipi/.emulation
```

2. Edit the /etc/fstab and delete the 3 TMPFS entries

3. Disable tipiwatchdog.service

4. exit the emulation clean: `sudo shutdown now`

## Errors in the standard image that might need fixing

raspi-config should be run to change the locale, and 
keyboard defaults for the system

# Using a real PI

You can use a real PI, and the latest SD image. You will have to setup the networking following the Raspberry PI documentation: [headless network setup](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi)

Be sure to touch the `ssh` file in the `boot` partition so sshd is enabled. Then you can get in and use raspi-config to setup other things.

To enable the websocket mode of talking to js99er, you just need to perform the `touch /home/tipi/.emulation` and then reboot or restart the tipi.service. 

You should leave the tmpfs and other services as they are for a normal PI setup.

