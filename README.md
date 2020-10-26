# iVar
iVar - DataBase of Genomics Variants

** INSTALL **

Install MariaDB:
	`apt -y install mariadb-server mariadb-client`

Create empty database iVar in mariadb, substituting PASSWORD with a
"very secure password"
```
   mysql -u root (-p, if needed)
   create database ivar;
   grant all on ivar.* to 'ivar'@'localhost' identified by 'PASSWORD';
   flush privileges;
```

Install web2py:
   http://web2py.com/

Install VCF Python Library PyVCF: 
   See: https://pyvcf.readthedocs.io/en/latest/
```
   apt install python-pip
   pip install setuptools
   git clone https://github.com/jamescasbon/PyVCF.git
   cd PyVCF/
   python setup.py install
```
Create first app config:
   `cp iVar/private/appconfig.ini.example iVar/private/appconfig.ini`

   And edit it changing PASSWORD with the previusly chosen MariaDB "very secure password"  :)
   ```
  ; db configuration
  [db]
  uri       = mysql://ivar:PASSWORD@localhost/ivar
```
