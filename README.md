# iVar
iVar - DataBase of Genomics Variants

## INSTALL ##

### Prerequisites: ###

#### Install web2py: ####
   http://web2py.com/

#### Install VCF Python Library PyVCF: ####
   See: https://pyvcf.readthedocs.io/en/latest/
```
   apt install python-pip
   pip install setuptools
   git clone https://github.com/jamescasbon/PyVCF.git
   cd PyVCF/
   python setup.py install
```

Install MariaDB:
```
   apt -y install mariadb-server mariadb-client
```
Create database iVar in mariadb using the provided sql schema from the scripts folder:
```
   mysql -u root -p < ivar-init-db.sql
```

Grant permissions to the ivar user, substituting PASSWORD with a
"very secure password"
```
   mysql -u root (-p, if needed)
   grant all on ivar.* to 'ivar'@'localhost' identified by 'PASSWORD';
   flush privileges;
```
#### Connecto to web2py console: ####

Start web2py

Go to admin console

Upload the latest web2py.app.iVar.w2p file from the app folder


Create first app config: (we assume you called the application "iVar") I
```
   cp iVar/private/appconfig.ini.example iVar/private/appconfig.ini`
```
And edit it changing PASSWORD with the previusly chosen MariaDB "very secure password"  :)
```
   ; db configuration
   [db]
   uri       = mysql://ivar:PASSWORD@localhost/ivar
```
#### Initial iVar Credentials: ####

Username: `admin@example.com`

Password: `admin`
