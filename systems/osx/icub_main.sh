# save current directory
CUR_PWD=`pwd`

export GIT_ICUB_MAIN=$SOFTWARE/git/icub-main

# Clone Yarp if it does not exist yet
if [ ! -e "$GIT_ICUB_MAIN" ]; then
	cd $SOFTWARE/git
	git clone https://github.com/robotology/icub-main.git
fi

# update icub-main
cd $GIT_ICUB_MAIN
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
if [ -d "build" ]; then
  rm -rf build
fi

# create build directory and switch to it
mkdir build
cd build

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
cmake -Wno-dev .. $FLAGS

# compile and install
make -j 8 && make install

# go back to the initial current directory
cd $CUR_PWD
