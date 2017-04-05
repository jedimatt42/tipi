# TIPI raspbian service 

To use tipi headless, you need to install the fileserver service that responds to the DSR.
This service is designed to auto-restart when the TI-99/4A experiences hardware reset LOW
signal. The systemd script will auto-restart it if it exists due to a reset, or crashes for any other reason.

# systemd service installation

cp tipi.service to /lib/systemd/system/

systemctl enable tipi.service
systemctl start tipi.service

This wraps the fileserver.py script. 

