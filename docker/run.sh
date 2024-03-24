#!/bin/bash
echo "Current user is : ${USER}"

#hostname=$1
echo "Need your input to define `hostname`"
read hostname
#hostname='orbslam3'
echo "Got it hostname=$hostname"


## Run as root
#docker exec -it -u 0 d89c34efb04a bash
## Run as regular user
#docker exec -it d89c34efb04a bash
## After the pip installation, save the container to an image:
#docker commit 328d10dbc60b ccj/mobile-stereo-pt:1.10-v2
#docker commit 67f1b7521d9d ccj/mobile-stereo-pt:1.12-v1
#exit

USER_NAME=${1:-'ccj'}
GROUP=$(id -gn)
VER=${2:-0.1}
DOCKER_IMAGE=${USER_NAME}/orbslam3-v091-dev:$VER

#root_dir='/nfs/STG/SemanticDenseMapping/changjiang'
#root_dir=${2:-'/nfs/STG/SemanticDenseMapping/changjiang'}
root_dir=${3:-'/nfs/home/us000182/code'}
u=$(id -un)
g=$(id -gn)
echo $u $g
echo "DOCKER_IMAGE=$DOCKER_IMAGE"
echo "root_dir=$root_dir"

# with --rm, will delete the container and hence the lib you installed 
#            using pip when you are in the container;
# without --rm, to save the container;
#    -u $u:$g \
#    -v "/home/$u:/home/$u" \

CURRENT_FILE_PATH=$(dirname $(dirname "$PWD")) 
docker run --gpus all --ipc=host \
    -e DISPLAY=$DISPLAY \
    -e HOSTNAME=${hostname} \
    -e ROOT_DIR=${root_dir} \
    -e NVIDIA_DRIVER_CAPABILITIES=all \
    -u $USER_NAME:$GROUP \
    --privileged \
    --net=host \
    -v "/nfs:/nfs/" \
    -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -it $DOCKER_IMAGE /bin/bash

exit

# no gpus
docker run --ipc=host \
    -e DISPLAY=$DISPLAY \
    -e HOSTNAME=${hostname} \
    -e ROOT_DIR=${root_dir} \
    -u $USER_NAME:$GROUP \
    --net=host \
    -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -it $DOCKER_IMAGE /bin/bash

exit

