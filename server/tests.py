# from django.test import TestCase
import commands
import os
import time
##################################
COMPILE_WORK_PATH = r"/home/projects/nw-packer/"
LOGO_PATH = COMPILE_WORK_PATH + "logo/"


##################################

def local_packing(conp_name):
    if os.getcwd() != r"/home/projects/nw-packer/":
        os.getcwd()
        print os.getcwd()
        if os.chdir(r"/home/projects/nw-packer/"):
            # return HttpResponse("A error arise : can't change direction to /home/projects/nw-packer")
            return "A error arise : can't change direction to /home/projects/nw-packer/"
    err, status1 = commands.getstatusoutput(r'python /home/projects/nw-packer/replace_logo.py ' + conp_name)
    if err != 0:
        # return HttpResponse("A error arise when place logo : " + status1)
        return "A error arise when place logo : " + status1
    else:
        err, status2 = commands.getstatusoutput(r"grunt | grep 'Done' ")
        if err != 0:
            # return HttpResponse("A error arise when compile: ", err)
            return "A error arise when compile: ", err
        err, status3 = commands.getstatusoutput(
            r"zip -r /home/projects/bary/release/Zadmin.zip /home/projects/nw-packer/build/releases/Zadmin/win/Zadmin/")
        if err != 0:
            # return HttpResponse("A error arise when packing: " + status3)
            return "A error arise when packing: " + status3
        return 0


def getimage(dir_list):
    if os.getcwd() != r"/root/mysite/_images":
        os.chdir(r"/root/mysite/_images")
        if os.getcwd() != r"/root/mysite/_images":
            return "Can change direction to the '_images'."
    for comp in dir_list:
        err, status = commands.getstatusoutput(r"cp -i /home/projects/nw-packer/" + comp + r"/logo.png " + comp + r".png")
        if err != 0:
            return "A error arise when copping image : " + status
    return 0


def git_tag_list():
    if os.getcwd() != r"/home/projects/zadmin":
        os.chdir(r"/home/projects/zadmin")
    if os.getcwd() != r"/home/projects/zadmin":
        return r"Can't change direction to '/home/projects/zadmin'"
    err, statu1 = commands.getstatusoutput(r"git tag -l")
    if err != 0:
        return r"A error arise when get tag list: "+statu1
    l = statu1.split("\n")
    return 0, l


def git_checkout(list, num):
    if os.getcwd() != r"/home/projects/zadmin":
        os.chdir(r"/home/projects/zadmin")
    if os.getcwd() != r"/home/projects/zadmin":
        return 1, r"Can't change direction to '/home/projects/zadmin'"
    try:
        list[num]
    except IndexError:
        return 2, r"A error arise: list index out of range."
    print r"git checkout "+"\""+list[num]+"\""
    err1, statu1 = commands.getstatusoutput(r"git checkout "+"\""+list[num]+"\"")
    if err1 != 0:
        return 3, r"A error arise when change branch: "+statu1
    return 0, "OK"


def log(string):
    sync_time()
    tm = time.asctime()
    fp = open(r"/root/mysite/server/log.txt")
    fp.write(tm, string, " \n")
    fp.close()


def sync_time():
    #print os.system("ntpdate 202.118.1.47")
    if os.system("ntpdate 202.118.1.47"):
        return "Can't get time from ntp server."
    #print os.system("hwclock -w")
    if os.system("hwclock -w"):
        return "Can't update time in BIOS."
    print time.asctime()
    print commands.getstatusoutput("date")
    return 0

if __name__ == '__main__':
    # print local_packing(r'zexabox')
    # err, li = commands.getstatusoutput('ls /home/projects/nw-packer/logo')
    # getimage(li.split('\n'))
    err, list_version = git_tag_list()
    # print err, list
    """err1, statu = git_checkout(list_version, 4)
    print err, statu
    os.system(r"cd /home/projects/zadmin && git branch")
    err, list_version = git_tag_list()
    # print err, list
    err1, statu = git_checkout(list_version, 3)
    print err, statu
    os.system(r"cd /home/projects/zadmin && git branch")
    err, list_version = git_tag_list()
    # print err, list
    err1, statu = git_checkout(list_version, 2)
    print err, statu
    os.system(r"cd /home/projects/zadmin && git branch")
    err, list_version = git_tag_list()
    # print err, list
    err1, statu = git_checkout(list_version, 1)
    print err, statu
    os.system(r"cd /home/projects/zadmin && git branch")
    err, list_version = git_tag_list()
    # print err, list
    err1, statu = git_checkout(list_version, 0)
    print err, statu
    os.system(r"cd /home/projects/zadmin && git branch")
    err, list_version = git_tag_list()
    # print err, list
    err1, statu = git_checkout(list_version, 5)
    print err1, statu
    os.system(r"cd /home/projects/zadmin && git branch")
    """
    print sync_time()


