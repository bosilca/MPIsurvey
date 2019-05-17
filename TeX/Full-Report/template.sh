#!/bin/sh

OUTDIR=../inputs

slist="1 2 3 5 6 9 13 15 16 18 20 29"

DEBUG=0

for qno in ${slist}; do
    q=Q${qno}
    if [ ${DEBUG} -gt 0 ] ; then
	echo ${q};
    else
	if [ -f ${q}.tex ] ; then
	    mv ${q}.tex ${q}.tex.org
	fi
	sed s/QX/${q}/ < SIMPLE.template > ${OUTDIR}/${q}.tex
    fi
done

olist="4 7 8 10 11 12 14 17 19 21 22 23 24 25 26 27 28"

for qno in ${olist}; do
    q=Q${qno}
    if [ -f ${q}.tex ]; then
	mv ${q}.tex ${q}.tex.org
    fi
    sed s/QX/${q}/ < OTHER.template > ${OUTDIR}/${q}.tex
done

slist="1 2 3 5 6 9 13 15 20 21 23 25 28 29"
mlist="4 7 8 10 11 12 14 16 17 18 19 22 24 26 27"

for s0 in ${slist}; do
    for s1 in $(seq 1 29); do
	if [ ${s1} -gt ${s0} ] ; then 
	    q=Q${s0}-Q${s1};
	    if [ ${DEBUG} -gt 0 ] ; then
		echo ${q};
	    else
		if [ -f ${q}.tex ] ; then
		    mv ${q}.tex ${q}.tex.org
		fi
		sed s/QX/${q}/ < CROSS.template > ${OUTDIR}/${q}.tex
	    fi
	fi
    done
done

for s0 in ${mlist}; do
    for s1 in ${slist}; do
	if [ ${s1} -gt ${s0} ] ; then 
	    q=Q${s0}-Q${s1};
	    if [ ${DEBUG} -gt 0 ] ; then
		echo ${q};
	    else
		if [ -f ${q}.tex ] ; then
		    mv ${q}.tex ${q}.tex.org
		fi
		sed s/QX/${q}/ < CROSS.template > ${OUTDIR}/${q}.tex
	    fi
	fi
    done
done
 