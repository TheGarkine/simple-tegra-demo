FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y qemu qemu-user-static debootstrap
ADD https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/jetson-210_linux_r32.7.1_aarch64.tbz2 /tmp

WORKDIR /tmp
RUN tar -xjvf jetson-210_linux_r32.7.1_aarch64.tbz2