# save current directory
CUR_PWD=`pwd`

####################################################################################################
# Thirdparty Packages
####################################################################################################

# SPY Package
if [ ! -d "$SOFTWARE_GIT/python-ar-markers" ]; then
	cd $SOFTWARE_GIT
	git clone https://github.com/DebVortex/python-ar-markers.git
fi

cd $SOFTWARE_GIT/python-ar-markers
git pull
python setup.py install

####################################################################################################
# BrutusTT Packages
####################################################################################################

# SPY Package
if [ ! -d "$SOFTWARE_GIT/spy" ]; then
	cd $SOFTWARE_GIT
	git clone https://github.com/BrutusTT/spy.git
fi

cd $SOFTWARE_GIT/spy
git pull
python setup.py install

# pyJD Package
if [ ! -d "$SOFTWARE_GIT/pyJD" ]; then
	cd $SOFTWARE_GIT
	git clone https://github.com/BrutusTT/pyJD.git
fi

cd $SOFTWARE_GIT/pyJD
git pull
python setup.py install

# pyNAO Package
if [ ! -d "$SOFTWARE_GIT/pyNAO" ]; then
	cd $SOFTWARE_GIT
	git clone https://github.com/BrutusTT/pyNAO.git
fi

cd $SOFTWARE_GIT/pyNAO
git pull
python setup.py install


# go back to the initial current directory
cd $CUR_PWD
