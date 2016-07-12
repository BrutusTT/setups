#!/bin/bash

# Environment Setup
./base_posix.sh

# OS Detection
platform='unknown'
unamestr=`uname`

if [[ "$unamestr" == 'Linux' ]]; then
	platform='linux'


elif [[ "$unamestr" == 'Darwin' ]]; then
	platform='osx'
	
	$platform/brew.sh
fi

# third party tools
thirdparty_git.sh

# Yarp & iCub stuff
$platform/yarp.sh
$platform/icub_main.sh

# own stuff
brutustt.sh
