#!/bin/bash

./base_posix.sh

platform='unknown'
unamestr=`uname`

if [[ "$unamestr" == 'Linux' ]]; then
	platform='ubuntu'


elif [[ "$unamestr" == 'Darwin' ]]; then
	platform='osx'
	
	$platform/brew.sh
fi

$platform/yarp.sh
$platform/icub_main.sh
brutustt.sh