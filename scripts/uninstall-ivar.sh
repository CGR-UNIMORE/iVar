#!/bin/bash

echo "Run as root. *MAY* damage your server.";
echo -n "Do you want to proceed ? crl-C to abort, Enter to continue";
read ANSWER;
deluser web2py; 
rm -rf /home/web2py 
apt remove --purge -y python-minimal
apt remove --purge -y python-pip
apt remove --purge -y unzip
dpkg --purge mariadb-client mariadb-common mariadb-client-core-10.1 mariadb-client-10.1 mariadb-server-core-10.1 mariadb-server-10.1 mariadb-server
apt autoremove -y
