#!/bin/bash

# save current directory
CUR_PWD=`pwd`

export GIT_YARP=$SOFTWARE/git/yarp

# Clone Yarp if it does not exist yet
if [ ! -e "$GIT_YARP" ]; then
	cd $SOFTWARE/git
	git clone https://github.com/robotology/yarp.git
fi

# update yarp
cd $GIT_YARP
git pull

# set some environment variables for compiling
export C_INCLUDE_PATH=$C_INCLUDE_PATH:$(brew --prefix gettext)/include/
export PATH=$PATH:/usr/local/bin
export PYTHONLIB=$(brew --prefix python)/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib

# Doxygen
if [ ! -e "Doxyfile" ]; then
	ln -s $SOFTWARE/docs/yarp.doxyfile Doxyfile
fi

# remove old build directory
if [ -d "build" ]; then
  rm -rf build
fi

# move and remove yarp include directory from previous runs
if [ -d "/usr/local/include/yarp" ]; then
  rm -rf /usr/local/include/yarp_prev
  mv /usr/local/include/yarp /usr/local/include/yarp_prev
fi

# create build directory and switch to it
mkdir build
cd build

# set the compile flags
export FLAGS="
-DCMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk
-DALLOW_IDL_GENERATION=OFF
-DCMAKE_BUILD_TYPE=RELEASE 
-DCREATE_DEVICE_LIBRARY_MODULES=TRUE 
-DCREATE_GUIS=TRUE 
-DCREATE_JAVA=TRUE 
-DCREATE_LIB_MATH=TRUE
-DCREATE_LUA=TRUE 
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
-DENABLE_yarpmod_OpenNI2DeviceClient=TRUE
-DENABLE_yarpmod_OpenNI2DeviceServer=TRUE
-DENABLE_yarpmod_portaudio=TRUE 
-DENABLE_yarpmod_opencv_grabber=TRUE 
-DPREPARE_CLASS_FILES=TRUE  
-DPYTHON_LIBRARY=$PYTHONLIB 
-DYARP_COMPILE_BINDINGS=TRUE 
-DYARP_COMPILE_TESTS=TRUE 
-DYARP_USE_PYTHON_VERSION=2.7 
-DYARP_USE_QCUSTOMPLOT=OFF
"

# run CMAKE
cmake -Wno-dev .. $FLAGS 

# compile and install
make -j 8 && make install

# build java bindings
cd generated_src
mv java yarp
cd yarp
javac *.java
cd ..
echo Main-Class: yarpJNI > manifest.txt
jar cvfm jyarp-linux.jar manifest.txt yarp
cd ..
cp ./lib/libjyarp.jnilib ./generated_src

# go back to the initial current directory
cd $CUR_PWD
