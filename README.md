# iVar
iVar - DataBase of Genomics Variants

== INSTALL==

===Prerequisites:====

==Install web2py:==
   http://web2py.com/

==Install VCF Python Library PyVCF:==
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
Create database iVar in mariadb using the provided sql schema:
```
   mysql -u root -p < $IVAR_DIR/scripts/ivar-init-db.sql
```

Grant permissions to the ivar user, substituting PASSWORD with a
"very secure password"
```
   mysql -u root (-p, if needed)
   grant all on ivar.* to 'ivar'@'localhost' identified by 'PASSWORD';
   flush privileges;
```

Create first app config:
```
   cp iVar/private/appconfig.ini.example iVar/private/appconfig.ini`
```
And edit it changing PASSWORD with the previusly chosen MariaDB "very secure password"  :)
```
   ; db configuration
   [db]
   uri       = mysql://ivar:PASSWORD@localhost/ivar
```
