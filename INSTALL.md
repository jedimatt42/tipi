# Setting up...

## Service User

Create a service user 'tipi' with the following commands:

```
sudo useradd --create-home --system --user-group tipi
```

## Install services

Setup the services, by cloning the git repository within the 'tipi' user home
directory, and running the setup.sh script.

```
sudo su tipi
cd /home/tipi
git clone https://github.com/jedimatt42/tipi.git tipi
cd /home/tipi/tipi
./setup.sh
```

## Other items to setup

* set a password for user tipi
* change the password for user pi
* change /var/log and /tmp and some others to tmpfs
* adjust mount parameters for sd, eliminate updating access time
* install samba share for /home/tipi/tipi_disk


