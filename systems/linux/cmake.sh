#!/bin/bash

# save current directory
CUR_PWD=`pwd`

cd $SOFTWARE_BUILD
wget https://cmake.org/files/v3.11/cmake-3.11.1.tar.gz
tar -xf cmake-3.11.1.tar.gz
rm cmake-3.11.1.tar.gz

cd cmake-3.11.1
./bootstrap
make -j 8
sudo make install

cd $CUR_PWD
