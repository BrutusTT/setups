#!/bin/bash

# OS Detection
platform='unknown'
unamestr=`uname`

if [[ "$unamestr" == 'Linux' ]]; then
	platform='linux'


elif [[ "$unamestr" == 'Darwin' ]]; then
	platform='osx'
	
	$platform/brew.sh
fi

# Environment Setup
source $platform/bash_env
./base_posix.sh

# third party tools
thirdparty_git.sh

# Yarp & iCub stuff
$platform/ycm.sh
$platform/yarp.sh
$platform/icub_main.sh
$platform/icub_contrib_common.sh


# own stuff
brutustt.sh
