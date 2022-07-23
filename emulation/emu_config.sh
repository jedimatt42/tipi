#!/bin/bash

function badinput {
	echo "error unrecognized response, use 'y' or 'n' only"
	exit 1
}

function enableNFS {
echo -n "enable NFS mount of tipi_disk (y/n) "
read yn
if [ ${yn:-} = "y" ]; then
	echo "NFS_ENABLED=1" >> ~/.emulation
	echo "NFS TIPI volume will be mounted"
else
if [ ${yn:-} = "n" ]; then
	echo "NFS_ENABLED=0" >> ~/.emulation
	echo "NFS will NOT be mounted"
else
	badinput
fi
fi
}

function enablePDF {
echo -n "enable PI.PIO PDF conversion (answer 'n' if using QEMU) (y/n) "
read yn
if [ ${yn:-} = "y" ]; then
	echo "PDF_ENABLED=1" >> ~/.emulation
	echo "PI.PIO PDF conversion enabled"
else
if [ ${yn:-} = "n" ]; then
	echo "PDF_ENABLED=0" >> ~/.emulation
	echo "PI.PIO PDF conversion disabled"
else
	badinput
fi
fi
}

function enableWebsocket {
echo -n "enable emulation websocket mode? (y/n) "
read yn
if [ ${yn:-} = "n" ]; then
	echo "websocket disabled"
	rm -f ~/.emulation
else
if [ ${yn:-} = "y" ]; then
	echo "websocket enabled"
	echo "# TIPI Websocket" > ~/.emulation
	enableNFS
	enablePDF
else
	badinput
fi
fi
}

enableWebsocket

