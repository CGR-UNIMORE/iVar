# iVar
iVar - DataBase of Genomics Variants

## INSTALL ##

### Prerequisites: ###

iVar has been tested on **Ubuntu 18.04.05 live server** for the amd64 (x86_64, or 64 bits) architecture.

If you use a different distribution, your mileage may vary.

Once the Ubuntu installation is complete, you may use the **[install-ivar.sh](https://raw.githubusercontent.com/CGR-UNIMORE/iVar/main/scripts/install-ivar.sh "script to install iVar")** script (right click to download).

We strongly suggest to use a **dedicated Ubuntu** (virtual or phisical) for iVar.

A Docker version _MAY_ arrive in the future. (we're looking into it)

#### Web2py Frameworks ####

web2py iVar is installed with a self-signed certificate, that allows connection 
without warnings only from:

http://localhost:9000/

http://ivar.local:9000/

http://127.0.0.1:9000/

You may use another URL similar to those, but you will get a certificate
warning or error. It is safe to ignore it if you are on the same secure 
local network as the iVar server.

Initial admin password is the one you provided during the installation.

#### iVar Application ####

URLs:

http://localhost:9000/iVar/

http://ivar.local:9000/iVar/

http://127.0.0.1:9000/iVar/

#### Initial iVar Credentials: ####

Username: `admin@example.com`

Password: `admin`

we suggest to change it as soon as possible in the user `admin` menu
