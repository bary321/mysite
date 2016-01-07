# coding:utf-8
import os
from os.path import join, getsize
__author__ = 'bary'


def getdirsize(dire):
    size = 0L
    for root, dirs, files in os.walk(dire):
        print "ROOT", root
        print "DIRS", dirs
        print "files", files
        size += sum([getsize(join(root, name)) for name in files])
    return size



filesize = getdirsize(r"C:\windows")
print "There are %.3f " % (filesize/1024/1024), "Mbytes in c:\\widows"

















































































