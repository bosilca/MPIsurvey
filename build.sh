#!/bin/sh

PROG=analyze.py
IN=${PROG}.in

python=`which python3`

cat - ${IN} <<EOF > ${PROG}
#!$python
EOF

chmod +x ${PROG}
