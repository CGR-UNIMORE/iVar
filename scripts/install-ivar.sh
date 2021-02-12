#!/bin/bash

UBUNTU_VERSION=`cut -c1-12 /etc/issue`

if [ "$UBUNTU_VERSION" != "Ubuntu 18.04" ];
then
	echo "Ubuntu 18.04 is needed for this installation.";
	exit 0;
else
	echo "Ubuntu 18.04 found. I'm happy. :)";
fi
echo "Choose a new web2py user password"
echo -n "(will be displayed on screen): ";
# FIXME
#read PASS
PASS="pippo";
echo "";
useradd  -p U$PASS web2py
if [ ! -d /home/web2py ]; then
    mkdir /home/web2py
else
    echo "web2py dir already exists.";
fi
chown web2py: /home/web2py
cd /home/web2py/
wget "https://mdipierro.pythonanywhere.com/examples/static/web2py_src.zip"
if [ $? -gt 0 ]; then
	echo "ERROR: Unable to download the web2py framework.";
	exit 0;
else
	echo "web2py framework downloaded.";
fi

apt update
apt upgrade -y
apt install -y python-minimal
apt install -y python-pip
pip install setuptools
git clone https://github.com/jamescasbon/PyVCF.git
cd PyVCF/
python2 setup.py install
cd -
apt-get install -y unzip
unzip web2py_src.zip
git clone "https://github.com/CGR-UNIMORE/iVar.git" 
apt -y install mariadb-server mariadb-client

echo "Patching original mariadb config"
cd /etc/mysql/mariadb.conf.d/
pwd
patch -p0 < /home/web2py/iVar/scripts/50-server.cnf.patch 
cd -
echo "Restarting mariadb"
systemctl restart mariadb

echo "Creating initial iVar Database";
mysql -u root  < iVar/scripts/ivar-init-db.sql
echo "grant all on ivar.* to 'ivar'@'localhost' identified by 'IV$PASS'; flush privileges;" | mysql -u root 
mysqladmin -u root password "R$PASS"

echo "Creating initial app config"
cp iVar/private/appconfig.ini.example iVar/private/appconfig.ini
sed -i -e "s/ivar:PASSWORD@/ivar:${PASS}@/" iVar/private/appconfig.ini


# FIXME: alla fine ?
chown -R web2py: /home/web2py

