#!/bin/bash

echo "Setup Environment"

if [ ! -d "~/software" ]; then
	echo "create main software directory"
	mkdir ~/software
fi

if [ ! -d "~/software/bin" ]; then
	echo "create bin directory"
		mkdir ~/software/bin
fi

if [ ! -d "~/software/build" ]; then
	echo "create build directory"
		mkdir ~/software/build
fi

if [ ! -d "~/software/git" ]; then
	echo "create git directory"
		mkdir ~/software/git
fi

