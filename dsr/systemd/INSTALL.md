# TIPI raspbian service 

To use tipi headless, you need to install the fileserver service that responds to the DSR.
This service is designed to auto-restart when the TI-99/4A experiences hardware reset LOW
signal. The systemd script will auto-restart it if it exists due to a reset, or crashes for any other reason.

# systemd service installation

## This wraps the fileserver.py script. 
```
cp tipi.service /lib/systemd/system/

systemctl enable tipi.service
systemctl start tipi.service
```

## And monitors the reset pin to trigger restarting the service. 
```
cp tipiwatchdog.service /lib/systemd/system/

systemctl enable tipiwatchdog.service
systemctl start tipiwatchdog.service
```

## And monitors the log for OLED worthy messages.
```
cp tipioled.service /lib/systemd/system/

systemctl enable tipioled.service
systemctl start tipioled.service
```

