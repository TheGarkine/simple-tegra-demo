#!/bin/bash
set -e

apt-get update
apt-get install software-properties-common -y
add-apt-repository universe
add-apt-repository multiverse
apt-get update
apt-get upgrade -y

DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata

# Install all required basic libraries
apt-get install -y \
    binfmt-support \
    cmake \
    curl \
    device-tree-compiler \
    libasound2 \
    libcairo2 \
    libdatrie1 \
    libegl1 \
    libegl1-mesa \
    libevdev2 \
    libfontconfig1 \
    libgles2 \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer1.0-0 \
    libgtk-3-0 \
    libharfbuzz0b \
    libinput10 \
    libjpeg-turbo8 \
    libpixman-1-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libpng16-16 \
    libssl-dev \
    libunwind8 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libx11-6 \
    libxext6 \
    libxkbcommon0 \
    libxrender1 \
    locales \
    locate \
    nano \
    network-manager \
    nginx \
    openssh-server \
    openssl \
    python \
    python3 \
    python3-pip \
    sudo \
    v4l-utils \
    wget

# We are required to provide libffi6
wget http://ftp.de.debian.org/debian/pool/main/libf/libffi/libffi6_3.2.1-9_arm64.deb
dpkg --install libffi6_3.2.1-9_arm64.deb

# This has no installation candidate
wget http://ports.ubuntu.com/pool/universe/g/gst-plugins-bad1.0/libgstreamer-plugins-bad1.0-0_1.16.2-2.1ubuntu1_arm64.deb
dpkg --install libgstreamer-plugins-bad1.0-0_1.16.2-2.1ubuntu1_arm64.deb