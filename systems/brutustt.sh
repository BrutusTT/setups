####################################################################################################
# BrutusTT Packages
####################################################################################################
#!/bin/bash

# save current directory
CUR_PWD=`pwd`

# SPY Package
cd $SOFTWARE_GIT/spy
python setup.py install --user

# pyJD Package
cd $SOFTWARE_GIT/pyJD
python setup.py install --user

# pyNAO Package
cd $SOFTWARE_GIT/pyNAO
python setup.py install --user


# go back to the initial current directory
cd $CUR_PWD
