# from django.test import TestCase
import commands
import os
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
        err, status = commands.getstatusoutput(r"cp -i " + LOGO_PATH + comp + r"/logo.png " + comp + r".png")
        if err != 0:
            return "A error arise when copping image : " + status
    return 0


if __name__ == '__main__':
    print local_packing(r'zexabox')
