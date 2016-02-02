#!/bin/bash
#!Program:
#	This program to achieve the packing and compilation
#date		author		edition
#2015/11/23	bary		1.0
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

cd /home/projects/nw-packer
echo "Replacing logo"
first=$(/home/projects/nw-packer/replace_logo.py $1 )
first_d=$(echo $first | grep 'success')
if [ "$first_d" == "" ]; then
	echo "company not found"
	exit 1
else 
	echo "Now compiling"
	second=$(grunt | grep 'Done')
	if [ "$second" == "" ]; then
		echo "Some error appear when compiling"
		exit 1
	else
		echo "Now Packing"
		tar -jpc -f /home/projects/bary/release/Zadmin.tar.bz2 /home/projects/nw-packer/build/releases/Zadmin/win/Zadmin/ &> tmp
	fi
fi	
		

