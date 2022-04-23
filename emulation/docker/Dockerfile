FROM python:bullseye

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get -y upgrade 

RUN apt-get -y install --no-install-recommends \
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
libffi-dev \
liblzma-dev

RUN apt-get -y install --no-install-recommends \
python3 \
python3-dev \
python3-virtualenv \
libcurl4-openssl-dev \
sqlite3 \
libsqlite3-dev \
php

RUN useradd -ms /bin/bash tipi

USER tipi
WORKDIR /home/tipi

COPY entrypoint.sh /entrypoint.sh

CMD ["/entrypoint.sh"]

EXPOSE 9900/tcp
EXPOSE 9901/tcp
