#!/bin/sh

PROG=analyze.py
IN=${PROG}.in

python=`which python3`

cat - ${IN} <<EOF > ${PROG}
#!$python

#############################################################
### DO NOT EDIT THIS FILE.  EDIT '$PROG.in' INSTEAD. ###
#############################################################
EOF

chmod +x ${PROG}
