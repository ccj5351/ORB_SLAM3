ARG UBUNTU_VERSION=22.04
ARG NVIDIA_CUDA_VERSION=12.3.1
#FROM nvidia/cuda:${NVIDIA_CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION} as builder
FROM nvidia/cuda:${NVIDIA_CUDA_VERSION}-runtime-ubuntu${UBUNTU_VERSION}

## > see: https://hub.docker.com/r/nvidia/cuda/tags?page=1&name=11.4.3
#FROM nvidia/cuda:11.4.3-cudnn8-devel-ubuntu20.04 as builder

# nvidia/cuda:11.4.3-cudnn8-devel-ubuntu20.04
# nvidia/cuda:11.4.3-cudnn8-runtime-ubuntu20.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ARG CMAKE_INSTALL_PREFIX=/usr/local

# During CMake configuration specify CMAKE_CUDA_ARCHITECTURES as 
# 1) “native”, if you want to run COLMAP on your current machine only, 
# 2) “all”/”all-major” to be able to distribute to other machines, 
# 3) or a specific CUDA architecture like “75”, etc.
ARG CUDA_ARCHITECTURES=native

# Prevent stop building ubuntu at time zone selection.
ENV DEBIAN_FRONTEND=noninteractive

## > see this Dockerfile example at https://github.com/TRI-ML/dgp/blob/master/Dockerfile;
ARG python=3.10

ENV PYTHON_VERSION=${python}

# Prepare and empty machine for building.
RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        git \
        cmake \
        g++ \
        wget \
        unzip \
        ninja-build \
        build-essential \
        pkg-config \
        libeigen3-dev \
        libssl-dev \
        # OpenCV dependencies
        libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
        libxvidcore-dev libx264-dev \ 
        libjpeg-dev libpng-dev libtiff-dev libwebp-dev \
        gfortran libatlas-base-dev \
        python3-dev python3-numpy \
        libtbb2 libtbb-dev libopenexr-dev \
        libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev \
        libgtk-3-dev \
        # Pangolin dependencies
        libgl1-mesa-dev \
        libglew-dev \
        libpython3-dev \
        libeigen3-dev \
        apt-transport-https \
        ca-certificates \
        software-properties-common \
        ## optional ones added by CCJ:
        libpng-dev \
        libjpeg-dev \
        libpng++-dev \
        vim tmux \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-dev \
        python${PYTHON_VERSION}-distutils \
        python3-pip \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

## optional ones added by CCJ:
RUN ln -sf /usr/bin/python${PYTHON_VERSION} /usr/bin/python3
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN pip install pybind11

# Build and install OPENCV.
ENV OPENCV_VERSION=4.5.4
RUN cd /tmp && git clone -v --progress https://github.com/opencv/opencv.git && cd opencv && \
    git checkout tags/${OPENCV_VERSION} -b v${OPENCV_VERSION} && \
    mkdir -p build &&  \
    cd build && \
    cmake .. -GNinja -D CMAKE_BUILD_TYPE=Release -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_GENERATE_PKGCONFIG=ON -D CMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} -D BUILD_EXAMPLES=OFF && \
    #make -j$nproc && make install && \
    ninja && ninja install && \
    cd / && rm -rf /tmp/opencv

# Build and install Pangolin
ENV PANGOLIN_VERSION=0.9.1
RUN apt update && apt install -y  libgl1-mesa-dev libglew-dev libboost-all-dev
RUN cd /tmp && git clone -v --progress --recursive https://github.com/stevenlovegrove/Pangolin.git && \
    cd Pangolin && \
    git checkout tags/v${PANGOLIN_VERSION} -b v${PANGOLIN_VERSION} && \
    mkdir build && \
    cd build && \
    cmake .. -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS=-std=c++14 -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} && \
    ninja && \
    ninja install && \
    cd /tmp && rm -rf Pangolin


##------------------------------------------------
###### ----- Added by CCJ -------#################
##------------------------------------------------
# Create a non-root user and switch to it
ARG USER_ID=1000
ARG GROUP_ID=1000

ARG USER_NAME='dummy'
ARG GROUP_NAME='dummy'

##--- Or, change those to first_run.sh
RUN addgroup --gid $GROUP_ID $GROUP_NAME
# Create a user 'appuser' under 'xyzgroup'
RUN useradd -rm -d /home/$USER_NAME --shell /bin/bash  --uid $USER_ID --gid $GROUP_ID -G $GROUP_NAME $USER_NAME 

#COPY files/* /tmp/
#RUN /bin/bash /tmp/first_run.sh $USER_ID $USER_NAME $GROUP_ID $GROUP_NAME

EXPOSE 22
USER $USER_NAME:$GROUP_NAME

WORKDIR /home/$USER_NAME
#RUN mkdir /ORB_SLAM3
#WORKDIR /ORB_SLAM3

##################################################
###  Personalized System initialization commands/installations (Optional)
##################################################
### Create softlinks ###
#RUN ln -s /nfs/home/us000182/code /home/${USER_NAME}/code
#RUN ln -s /nfs/home/us000182/Downloads /home/${USER_NAME}/Downloads

##################################################
###  Environment variable setup
##################################################
ENV PATH=/home/$USER_NAME/.local/bin:$PATH
ENV PATH=/home/$USER_NAME/bin:$PATH

### color prompt ###
ENV TERM='xterm-color'

##################################################
###  Bashrc
##################################################
### bashrc ###
COPY bashrc_extra /home/$USER_NAME/.bashrc_extra
RUN echo "source ~/.bashrc_extra" >> ~/.bashrc
