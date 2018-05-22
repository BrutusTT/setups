sudo mv /var/cache/app-info/xapian/default /var/cache/app-info/xapian/default_old
sudo mv /var/cache/app-info/xapian/default_old /var/cache/app-info/xapian/default
sudo apt update
sudo apt upgrade -y
sudo apt install coinor-libipopt-dev doxygen graphviz-dev libace-dev libatlas-base-dev libeigen3-dev libgsl-dev libgstreamer0.10-dev libode-dev libopencv-dev libopencv-contrib-dev libqwt-qt5-dev libsdl1.2-dev lua5.3 mc mesa-common-dev portaudio19-dev pyqt5-dev-tools python-pip python-pyaudio swig  -y
