#!/bin/bash
  
/bin/su - web2py -c "/usr/bin/python \
        ./web2py/web2py.py \
        -i 0.0.0.0 -p 9000 \
        -a pippo \
        -c ./iVar/private/ivar-cert.pem \
        -k ./iVar/private/ivar-privkey.pem \
        2>&1 >> log/web2py.log-$(/bin/date +%Y%m%d-%H%M%S) 2>&1 &"
