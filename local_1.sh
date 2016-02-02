#!/bin/bash
#!Program:
#	This program to achieve the packing and compilation
#date		author		edition
#2015/11/23	bary		1.0
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

cd /home/projects/nw-packer
cp=$(pwd | grep "/home/projects/nw-packer")
if [ "$cp" = "" ];then
    echo "A error arise when change direction to '/home/projects/nw-packer'"
    exit 1
fi    
first=$(/home/projects/nw-packer/replace_logo.py $1 )
first_d=$(echo $first | grep 'success')
if [ "$first_d" = "" ]; then
	echo "A error arise when replace_logo : " $first
	exit 1
else 
    second_d=$(grunt)
	second=$(echo $second_d | grep 'Done')
	if [ "$second" = "" ]; then
		echo "Some error appear when compiling : " $second_d
		exit 1
	else
        cd /home/projects/nw-packer/build/releases/Zadmin/win/
        cp1=$(pwd | grep "/home/projects/nw-packer/build/releases/Zadmin/win")
        if [ "$cp1" = "" ];then
            echo "A err arise when change direction to '/home/projects/nw-packer/build/releases/Zadmin/win'"
            exit 1
        fi
        zip -r /home/projects/bary/release/Zadmin.zip ./Zadmin/ &> /dev/null
        cp2=$(file /home/projects/bary/release/Zadmin.zip | grep "archive data" )
        if [ "$cp2" = "" ];then
            echo "A err arise when packing : zip fail"
            exit 1
        fi
    fi
fi	
	
