#!/bin/bash

FLAG=true
FLAG=false
if [ $FLAG == 'true' ]; then
    echo "Configuring and building Thirdparty/DBoW2 ..."
    cd Thirdparty/DBoW2
    mkdir build
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release
    make -j8  
    
    echo "Configuring and building Thirdparty/g2o ..."
    cd ../../g2o
    #cd Thirdparty/g2o
    mkdir build
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release
    make -j8
    #exit

    #cd Thirdparty/Sophus
    cd ../../Sophus
    echo "Configuring and building Thirdparty/Sophus ..."

    mkdir build
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release
    make -j8
    exit
fi



FLAG=true
FLAG=false
if [ $FLAG == 'true' ]; then
    echo "Uncompress vocabulary ..."
    cd Vocabulary
    tar -xf ORBvoc.txt.tar.gz
    exit
fi


FLAG=true
#FLAG=false
if [ $FLAG == 'true' ]; then
    echo "Configuring and building ORB_SLAM3 ..."
    mkdir build
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release
    make -j8
    exit
fi
