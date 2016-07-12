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
$platform/yarp.sh
$platform/icub_main.sh

# own stuff
brutustt.sh
