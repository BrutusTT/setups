####################################################################################################
# Thirdparty Packages
####################################################################################################
#!/bin/bash

# save current directory
CUR_PWD=`pwd`

# MaryTTS
if [ ! -d "$SOFTWARE_GIT/marytts-installer" ]; then
	cd $SOFTWARE_GIT
	git clone https://github.com/marytts/marytts-installer.git
fi

cd $SOFTWARE_GIT/marytts-installer
git pull


# Python AR Markers
if [ ! -d "$SOFTWARE_GIT/python-ar-markers" ]; then
	cd $SOFTWARE_GIT
	git clone https://github.com/DebVortex/python-ar-markers.git
fi

cd $SOFTWARE_GIT/python-ar-markers
git pull
python setup.py install --user

# go back to the initial current directory
cd $CUR_PWD
