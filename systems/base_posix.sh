#!/bin/bash

echo "Setup Environment"

if [ ! -d "$SOFTWARE" ]; then
    echo "create main software directory"
    mkdir $SOFTWARE
fi

if [ ! -d "$SOFTWARE_BIN" ]; then
    echo "create bin directory"
    mkdir $SOFTWARE_BIN
fi

if [ ! -d "$SOFTWARE_BUILD" ]; then
    echo "create build directory"
    mkdir $SOFTWARE_BUILD
fi

if [ ! -d "$SOFTWARE_GIT" ]; then
    echo "create git directory"
    mkdir $SOFTWARE_GIT
fi

if [ ! -d "$SOFTWARE_ENV" ]; then
    echo "create environments directory"
    mkdir $SOFTWARE_ENV
fi


# Python Packages

echo "Setup Python Packages via pip"

pip install virtualenv --user
pip install SpeechRecognition --user
pip install numpy --user