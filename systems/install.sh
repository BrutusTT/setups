#!/bin/bash

# Environment Setup
source bash_exports
source bash_aliases
source $platform/bash_env

# Install System Packages


if [[ "$platform" == 'linux' ]]; then
    $platform/apt.sh

elif [[ "$platform" == 'osx' ]]; then
    $platform/brew.sh
fi


./base_posix.sh

echo "fetch all GitHub sources"

# go to git dir and remember where we are coming from
CUR_PWD=`pwd`
cd $SOFTWARE_GIT

# for all repos in the github_repos.txt
while read src; do	

	# clone it into the git directory, ignore failure as it might already have been cloned
	if git clone https://github.com/$src > /dev/null 2>&1; then
		echo "fetched ${src}"
	else
		echo "already exists ${src}"
	fi
done < github_repos.txt

# go back where we were coming from
cd $CUR_PWD

# iterate over all repos and update them
echo "update all GitHub sources"
for dir in $SOFTWARE_GIT/*; do 
	(cd "$dir" && echo "$dir" && git pull);
done


# third party tools
thirdparty_git.sh

# Yarp & iCub stuff
$platform/ycm.sh
$platform/yarp.sh
$platform/icub_main.sh
$platform/icub_contrib_common.sh

# own stuff
brutustt.sh


echo "Don't forget to add the bash_exports and bash_aliases to the .bashrc"