#!/bin/bash

# save current directory
CUR_PWD=`pwd`

export GIT_ICC=$SOFTWARE/git/icub_contrib_common

# update icub-main
cd $GIT_ICC

# remove old build directory
if [ -d "build" ]; then
  rm -rf build
fi

# create build directory and switch to it
mkdir build
cd build

# set the compile flags
export FLAGS="
-DCMAKE_BUILD_TYPE=RELEASE 
"

# run CMAKE
cmake -Wno-dev .. $FLAGS

# compile and install
make -j 8 && make install

# go back to the initial current directory
cd $CUR_PWD
