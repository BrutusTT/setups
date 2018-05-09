#!/bin/bash

# save current directory
CUR_PWD=`pwd`

cd $ICUB_ROOT

# set some environment variables for compiling
export C_INCLUDE_PATH=$C_INCLUDE_PATH:/usr/local/include/coin

# Doxygen
if [ ! -e "Doxyfile" ]; then
    ln -s $SOFTWARE/docs/icub_main.doxyfile Doxyfile
fi

# remove old build directory
if [ -d "$ICUB_DIR" ]; then
  rm -rf $ICUB_DIR
fi

# create build directory and switch to it
mkdir $ICUB_DIR
cd $ICUB_DIR

# set the compile flags
export FLAGS="
-DCMAKE_BUILD_TYPE=RELEASE 
-DENABLE_icubmod_cartesiancontrollerclient=TRUE
-DENABLE_icubmod_cartesiancontrollerserver=TRUE
-DENABLE_icubmod_gazecontrollerclient=TRUE 
-DICUB_USE_IPP=TRUE
-DICUB_SHARED_LIBRARY=TRUE 
"

# run CMAKE
cmake -Wno-dev $FLAGS $ICUB_ROOT

# compile and install
make -j 8 install

# go back to the initial current directory
cd $CUR_PWD
