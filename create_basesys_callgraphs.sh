#!/bin/sh

libs=`find /var/build/bkidney/obj/usr/home/bkidney/projects/cadets/freebsd/amd64.amd64 -name "*.bc" |grep --invert-match "/tests/" |grep --invert-match "full" |grep "so"`
# usrlibs=`find /var/build/bkidney/obj/usr/home/bkidney/projects/cadets/freebsd/amd64.amd64/usr/lib -name "*.bc" |grep --invert-match "/tests/" |grep --invert-match "full" |grep "so"`

for i in ${libs}
do
	base=`basename $i`
	`opt -dot-callgraph $i > /dev/null`
	`python2 translate_dot.py callgraph.dot > ${base}.dot`
done

# for i in ${usrlibs}
# do
# 	base=`basename $i`
# 	`opt -dot-callgraph -o ${base}.dot $i`
# done
