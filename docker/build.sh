#!/bin/bash

#> See: Verify the version of ubuntu running in a Docker container,
#> at https://stackoverflow.com/questions/38003194/verify-the-version-of-ubuntu-running-in-a-docker-container;

#It's simple variables that are shell script friendly, so you can run

echo "------------------->"
echo "------------------->"
echo "----start building docker image ..."

UBUNTU_VERSION=22.04
NVIDIA_CUDA_VERSION=12.3.1
#UBUNTU_VERSION=20.04
#NVIDIA_CUDA_VERSION=11.4.3

USER_NAME=${1:-'ccj'}
VER=${2:-0.1}
DOCKER_TAG=${USER_NAME}/orbslam3-v091-dev:$VER

echo "Will build docker container $DOCKER_TAG ..."
#exit
pwd

#if [ -d "build" ]; then rm -r build; fi
#mkdir -p build
#exit

## if you want to use the same username as the host machine;
#    --build-arg USER_NAME=$(id -un) \

docker build --tag $DOCKER_TAG \
    --force-rm \
    --build-arg UBUNTU_VERSION=$UBUNTU_VERSION \
    --build-arg NVIDIA_CUDA_VERSION=$NVIDIA_CUDA_VERSION \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) \
    --build-arg USER_NAME=$USER_NAME \
    --build-arg GROUP_NAME=$(id -gn) \
    .

# could add:
# --no-cache \
#--force-rm \
