# iVar
iVar - DataBase of Genomics Variants

## INSTALL ##

### Prerequisites: ###

#### Create user web2py ####
```
adduser web2py
```
Following instructions

#### Install python 2.7 ####

#### Install web2py (for python 2.7): ####
```
cd /home/web2py/
```
   http://web2py.com/

Give permissions
```
chown -R web2py: web2py
```

#### Install VCF Python Library PyVCF: ####
   See: https://pyvcf.readthedocs.io/en/latest/
```
   cd ~
   sudo apt install python-pip
   sudo pip install setuptools
   sudo git clone https://github.com/jamescasbon/PyVCF.git
   sudo cd PyVCF/
   sudo python setup.py install
```

#### Certificati ####
Generare o utilizzare dei certificati per il proprio server 

#### Connect to web2py console: ####

Start web2py


Go to admin console

Upload the latest web2py.app.iVar.w2p file from the app folder


Create first app config: (we assume you called the application "iVar") I
```
   cp iVar/private/appconfig.ini.example iVar/private/appconfig.ini
```
And edit it changing PASSWORD with the previusly chosen MariaDB "very secure password"  :)
```
   ; db configuration
   [db]
   uri       = mysql://ivar:PASSWORD@localhost/ivar
```

### Install MariaDB: ###
```
   sudo apt -y install mariadb-server mariadb-client
```
Create database iVar in mariadb using the provided sql schema from the scripts folder:

```
   mysql -u root -p < ivar-init-db.sql
```

NOTA: ottengo il seguente errore
   -> ERROR 1146 (42S02) at line 490: Table 'ivar.SAMPLE_VARIANT_old' doesn't exist -> Eliminare le suddette righe dall'sql di init

   ERROR 1071 (42000) at line 502: Specified key was too long; max key length is 767 bytes

Grant permissions to the ivar user, substituting PASSWORD with a
"very secure password"
```
   mysql -u root (-p, if needed)
   grant all on ivar.* to 'ivar'@'localhost' identified by 'PASSWORD';
   flush privileges;
```

#### Initial iVar Credentials: ####

Username: `admin@example.com`

Password: `admin`
