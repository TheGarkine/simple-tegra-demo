apt-get dist-upgrade -y --autoremove
apt-get install -y \
    build-essential \
    cmake \
    git \
    gfortran \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libavresample-dev \
    libcanberra-gtk3-module \
    libdc1394-22-dev \
    libeigen3-dev \
    libglew-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-good1.0-dev \
    libgstreamer1.0-dev \
    libgtk-3-dev \
    libjpeg-dev \
    libjpeg8-dev \
    libjpeg-turbo8-dev \
    liblapack-dev \
    liblapacke-dev \
    libopenblas-dev \
    libpng-dev \
    libpostproc-dev \
    libswscale-dev \
    libtbb-dev \
    libtbb2 \
    libtesseract-dev \
    libtiff-dev \
    libv4l-dev \
    libxine2-dev \
    libxvidcore-dev \
    libx264-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-matplotlib \
    qv4l2 \
    v4l-utils \
    zlib1g-dev

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/sbsa/cuda-ubuntu1804.pin
mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget http://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda-repo-ubuntu1804-11-0-local_11.0.2-450.51.05-1_arm64.deb
dpkg -i cuda-repo-ubuntu1804-11-0-local_11.0.2-450.51.05-1_arm64.deb
apt-key add /var/cuda-repo-ubuntu1804-11-0-local/7fa2af80.pub
apt-get update

apt-get install -y cuda-toolkit-11-0 libcudnn8 libcudnn8-dev


cd /tmp
git clone --depth 1 --branch "4.4.0" https://github.com/opencv/opencv.git
git clone --depth 1 --branch "4.4.0" https://github.com/opencv/opencv_contrib.git

cd opencv
mkdir build 
cd build

export CMAKEFLAGS="-D BUILD_EXAMPLES=OFF
        -D BUILD_opencv_python2=OFF
        -D BUILD_opencv_python3=ON
        -D CMAKE_BUILD_TYPE=RELEASE
        -D CMAKE_INSTALL_PREFIX=/usr/local
        -D CUDA_ARCH_BIN=5.3,6.2,7.2
        -D CUDA_ARCH_PTX=
        -D CUDA_FAST_MATH=ON
        -D CUDNN_VERSION='8.0'
        -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 
        -D ENABLE_NEON=ON
        -D OPENCV_DNN_CUDA=ON
        -D OPENCV_ENABLE_NONFREE=ON
        -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib/modules
        -D OPENCV_GENERATE_PKGCONFIG=ON
        -D WITH_CUBLAS=ON
        -D WITH_CUDA=ON
        -D WITH_CUDNN=ON
        -D WITH_GSTREAMER=OFF
        -D WITH_LIBV4L=ON
        -D WITH_OPENGL=ON"

cmake ${CMAKEFLAGS} ..

make -j8
make install