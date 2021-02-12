#!/bin/bash
  
/bin/su - web2py -c "/usr/bin/python \
        ./web2py/web2py.py \
        -i 0.0.0.0 -p 9000 \
        -a pippo \
        -c /home/web2py/iVar/private/ivar-cert.pem \
        -k /home/web2py/iVar/private/ivar-privkey.pem \
        2>&1 >> web2py.log-$(/bin/date +%Y%m%d-%H%M%S) 2>&1 &"
