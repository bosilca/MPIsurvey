#!/bin/sh

TMPDIR=../templates
CHAPDIR=./chaps

slist="1 2 3 5 6 9 13 15 16 18 20 29"

DEBUG=0

mkdir -p ${CHAPDIR}

function create_template() {
    template=${TMPDIR}/$1
    tmpfile=${TMPDIR}/$2.tex;
    texfile=${CHAPDIR}/$2.tex;
    sed s/QX/${q}/ < $template > ${tmpfile};
    if [ -f $texfile ] ; then
	echo "$texfile exists. Copy $tmpfile file, if needed.";
    else 
	if [ ${DEBUG} -gt 0 ] ; then
	    echo "cp $tmpfile $texfile";
	else 
	    cp $tmpfile $texfile;
	fi
    fi
}

for qno in ${slist}; do
    q=Q${qno}
    create_template SIMPLE.template $q
done

olist="4 7 8 10 11 12 14 17 19 21 22 23 24 25 26 27 28"

for qno in ${olist}; do
    q=Q${qno}
    create_template OTHER.template $q
done

slist="1 2 3 5 6 9 13 15 20 21 23 25 28 29"
mlist="4 7 8 10 11 12 14 16 17 18 19 22 24 26 27"

for s0 in ${slist}; do
    for s1 in $(seq 1 29); do
	if [ ${s1} -gt ${s0} ] ; then 
	    q=Q${s0}-Q${s1};
	    create_template CROSS.template $q;
	fi
    done
done

for s0 in ${mlist}; do
    for s1 in ${slist}; do
	if [ ${s1} -gt ${s0} ] ; then 
	    q=Q${s0}-Q${s1};
	    if [ ${s1} -gt ${s0} ] ; then 
		create_template CROSS.template $q;
	    fi
	fi
    done
done
 
