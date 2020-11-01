FROM ubuntu:xenial

ENV DEBIAN_FRONTEND noninteractive

# Update
RUN apt-get update -y && apt-get install socat -y gdb python-pip vim tmux

# General things needed for pwntools and pwndbg to run
RUN apt-get install git python-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev patchelf -y 

RUN pip install pwn

# Install pwndbg
RUN git clone https://github.com/pwndbg/pwndbg && cd pwndbg && ./setup.sh && cd ../

# Challenge files to ADD
RUN git clone https://github.com/mdulin2/house-of-muney 

# Fixes the loader and recompiles the binary for us :) 
RUN cd house-of-muney && ./compile.sh

