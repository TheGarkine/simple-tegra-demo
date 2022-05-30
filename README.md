# Simple Tegra Demo

Note that all commands are written and tested on Ubuntu 20.04.
If you want to experiment on another Platform, it is best to containerize your build environment.

## Agenda
- Introduction
- About ARM Linux in General
    - Low Energy Devices
    - Higher Computational Effort than micro controllers

- About Edge Computing

- About Tegra
    - Began 2008, timeline follows

- About the problem we want to solve

- Building the solution and flashing it to the board
    - meantime: a brief overview of what Tegra does
    - meantime: a brief history of Tegra
    - meantime(optional): setup

- Analysis
- Demonstration with CUDA
- Outlook
    - Security
    - Alternatives: Ubuntu based, Buildroot, Multistrap, Yocto
    - Nvidia acquires ARM
- Optional: Deep Drone Project

## Requirements

To get started, you will need a few packages (given you are using a normal, non-aarch64 PC):

- qemu
- qemu-user-static
- debootstrap

You will also need to Download the L4T Driver Package (latest version for nano) [here](https://developer.nvidia.com/embedded/linux-tegra-r3271).
Extract it such that the Linux_for_Tegra directory is on the root directory of this repository.

## Building the Rootfs

```bash
# 30 seconds
debootstrap --foreign --arch arm64 --variant=minbase focal ./Linux_for_Tegra/rootfs
cp /usr/bin/qemu-aarch64-static ./Linux_for_Tegra/rootfs/usr/bin/
mount /sys Linux_for_Tegra/rootfs/sys -o bind
mount /proc Linux_for_Tegra/rootfs/proc -o bind
mount /dev Linux_for_Tegra/rootfs/dev -o bind
# 45 seconds
chroot ./Linux_for_Tegra/rootfs /debootstrap/debootstrap --second-stage
```
```bash
cp ./pre_apply_binaries.sh ./Linux_for_Tegra/rootfs/tmp/
# 6min 30
chroot ./Linux_for_Tegra/rootfs /bin/bash /tmp/pre_apply_binaries.sh

cd Linux_for_Tegra
rm rootfs/dev/random
rm rootfs/dev/urandom
sed -i 's/dpkg -i/dpkg -i --force-overwrite/g' nv_tegra/nv-apply-debs.sh
./apply_binaries.sh 
```

# cleanup
```bash
umount Linux_for_Tegra/rootfs/sys
umount Linux_for_Tegra/rootfs/proc 
umount Linux_for_Tegra/rootfs/dev
```

# no cuda
chroot rootfs apt-get install libgl1
chroot rootfs python3 -m pip install opencv-python

# end

chroot rootfs python3 -m pip install fastapi uvicorn websockets
chroot rootfs useradd netlight --create-home --shell /bin/bash
echo "netlight:password" | chroot rootfs chpasswd
chroot rootfs usermod -aG sudo netlight
cp ../web_cam_server_cpu.py rootfs/

# flash
```bash
# basic 7min 2
./nvautoflash.sh
```