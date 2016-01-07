#!/bin/bash
cd /home/projects/nw-packer
a=$(grunt 1> /dev/null)
if [ "$a" = "" ];then
    exit 0
else
    echo $a
    exit 1    
fi
