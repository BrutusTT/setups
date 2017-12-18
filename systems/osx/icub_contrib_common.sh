#!/bin/bash

# save current directory
CUR_PWD=`pwd`

export GIT_ICC=$SOFTWARE/git/icub_contrib_common

# Clone Yarp if it does not exist yet
if [ ! -e "$GIT_ICC" ]; then
	cd $SOFTWARE/git
	git clone https://github.com/robotology/icub-contrib-common.git
fi

# update icub-main
cd $GIT_ICC
git pull

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
