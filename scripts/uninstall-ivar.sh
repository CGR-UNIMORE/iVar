#!/bin/bash

PASS="pippo";

deluser web2py; 
rm -rf /home/web2py 
apt remove --purge -y python-minimal
apt remove --purge -y python-pip
apt remove --purge -y unzip
echo "revoke all privileges, grant option from 'ivar'@'localhost'; flush privileges;" | mysql -u root -pR$PASS
echo "drop database ivar;" | mysql -u root -pR$PASS
dpkg --purge mariadb-common mariadb-client-core-10.1 mariadb-client-10.1 mariadb-server-core-10.1 mariadb-server-10.1
# apt remove --purge -y mariadb-server mariadb-client
apt autoremove -y

