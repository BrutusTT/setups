#!/bin/bash

# save current directory
CUR_PWD=`pwd`

# Clone Yarp if it does not exist yet
if [ ! -e "$ICUB_ROOT" ]; then
    cd $ROBOT_CODE
    git clone https://github.com/robotology/icub-main.git
fi

# update icub-main
cd $ICUB_ROOT
git pull

# set some environment variables for compiling
export PATH=$(brew --prefix qt5)/bin:$PATH
export GCC_PATH=$(brew --prefix gcc)/lib/gcc/5
export C_INCLUDE_PATH=$C_INCLUDE_PATH:/usr/local/include/coin

export LDFLAGS="-L$(brew --prefix cairo)/lib $LDFLAGS"
export CPPFLAGS="-I$(brew --prefix cairo)/include -I/usr/local/include/coin $CPPFLAGS"
export PKG_CONFIG_PATH=$(brew --prefix cairo)/lib/pkgconfig:$(brew --prefix pixman)/lib/pkgconfig:$(brew --prefix fontconfig)/lib/pkgconfig:$PKG_CONFIG_PATH

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
cmake -Wno-dev  $FLAGS $ICUB_ROOT

# compile and install
make -j 8 install

# go back to the initial current directory
cd $CUR_PWD
