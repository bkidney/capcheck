#!/bin/sh -x

for i in ${1}
do
	base=`basename $i`
	`python2 translate_dot.py $i > $i.tr`
done

# for i in ${usrlibs}
# do
# 	base=`basename $i`
# 	`opt -dot-callgraph -o ${base}.dot $i`
# done
