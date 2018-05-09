#!/bin/bash

# save current directory
CUR_PWD=`pwd`

cd $YARP_ROOT

# Doxygen
if [ ! -e "Doxyfile" ]; then
    ln -s $SOFTWARE/docs/yarp.doxyfile Doxyfile
fi

# remove old build directory
if [ -d "$YARP_DIR" ]; then
    rm -rf $YARP_DIR
fi

# move and remove yarp include directory from previous runs
if [ -d "/usr/local/include/yarp" ]; then
	sudo rm -rf /usr/local/include/yarp_prev
fi

# create build directory and switch to it
mkdir $YARP_DIR
cd $YARP_DIR

# set the compile flags
export FLAGS="
-DALLOW_IDL_GENERATION=OFF
-DCMAKE_BUILD_TYPE=RELEASE 
-DCREATE_DEVICE_LIBRARY_MODULES=TRUE 
-DCREATE_GUIS=TRUE 
-DCREATE_JAVA=FALSE 
-DCREATE_LIB_MATH=TRUE
-DCREATE_LUA=FALSE 
-DCREATE_OPTIONAL_CARRIERS=TRUE 
-DCREATE_PYTHON=TRUE 
-DCREATE_SHARED_LIBRARY=TRUE 
-DCREATE_YARPDATADUMPER=TRUE  
-DCREATE_YARPDATAPLAYER=TRUE  
-DCREATE_YARPMANAGER=TRUE  
-DCREATE_YARPMANAGER_CONSOLE=TRUE  
-DCREATE_YARPVIEW=TRUE  
-DCREATE_YARPSCOPE=FALSE  
-DENABLE_yarpcar_bayer=TRUE  
-DENABLE_yarpcar_mjpeg=TRUE  
-DENABLE_yarpcar_xmlrpc=TRUE  
-DENABLE_yarpcar_depthimage=TRUE  
-DENABLE_yarpmod_OpenNI2DeviceClient=FALSE
-DENABLE_yarpmod_OpenNI2DeviceServer=FALSE
-DENABLE_yarpmod_portaudio=TRUE 
-DENABLE_yarpmod_opencv_grabber=TRUE 
-DPREPARE_CLASS_FILES=TRUE  
-DYARP_COMPILE_BINDINGS=TRUE 
-DYARP_COMPILE_TESTS=TRUE 
-DYARP_USE_PYTHON_VERSION=2.7 
-DYARP_USE_QCUSTOMPLOT=OFF
"

# run CMAKE
cmake -Wno-dev $FLAGS $YARP_ROOT

# compile and install
make -j && sudo make install install

# build java bindings
#cd generated_src
#mv java yarp
#cd yarp
#javac *.java
#cd ..
#echo Main-Class: yarpJNI > manifest.txt
#jar cvfm jyarp-linux.jar manifest.txt yarp
#cd ..
#cp ./lib/libjyarp.jnilib ./generated_src

# go back to the initial current directory
cd $CUR_PWD
