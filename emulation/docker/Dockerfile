FROM debian:bullseye-slim

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install \
git \
build-essential \
cmake \
libssl-dev \
zlib1g-dev \
libbz2-dev \
libreadline-dev \
libsqlite3-dev \
wget \
curl \
llvm \
libncurses5-dev \
libncursesw5-dev \
xz-utils \
tk-dev \
libffi-dev \
liblzma-dev \
python3 \
python3-dev \
python-dev \
python3-virtualenv \
libcurl4-openssl-dev \
samba \
sqlite3 \
libsqlite3-dev \
php

RUN useradd -ms /bin/bash tipi

USER tipi
WORKDIR /home/tipi

RUN git clone https://github.com/jedimatt42/tipi.git && \
    cd tipi && \
    git checkout jm42/docker && \
    git submodule update --init && \
    mkdir /home/tipi/tipi_disk && \
    cd /home/tipi && \
    git clone https://github.com/endlos99/xdt99.git && \
    git clone https://github.com/dnotq/tidbit.git

RUN cd tipi/services && \
    ./setup.sh

RUN echo "# TIPI WEBSOCKET" >/home/tipi/.emulation
RUN echo "NFS_ENABLED=0" >>/home/tipi/.emulation
RUN echo "PDF_ENABLED=1" >>/home/tipi/.emulation

CMD ["/home/tipi/tipi/services/tipi-emu.sh"]

EXPOSE 9901/tcp
