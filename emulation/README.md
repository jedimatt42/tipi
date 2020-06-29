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

