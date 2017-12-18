#!/bin/bash

echo "Setup Environment"

if [ ! -d "${HOME}/software" ]; then
	echo "create main software directory"
	mkdir ${HOME}/software
fi

if [ ! -d "${HOME}/software/bin" ]; then
	echo "create bin directory"
	mkdir ${HOME}/software/bin
fi

if [ ! -d "${HOME}/software/build" ]; then
	echo "create build directory"
	mkdir ${HOME}/software/build
fi

if [ ! -d "${HOME}/software/git" ]; then
	echo "create git directory"
	mkdir ${HOME}/software/git
fi

if [ ! -d "${HOME}/software/environments" ]; then
	echo "create environments directory"
	mkdir ${HOME}/software/environments
fi


# Python Packages

echo "Setup Python Packages via pip"

pip install virtualenv --user
pip install SpeechRecognition --user
pip install numpy --user